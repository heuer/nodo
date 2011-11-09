# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 - 2011 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
#     * Neither the project name nor the names of the contributors may be 
#       used to endorse or promote products derived from this software 
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
"""\
Graph `Redis <http://redis.io/>`_ store.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import absolute_import
import hashlib
import redis
from ..interfaces import IConnection, IImmutableGraph, IGraph, implements
from .. import XSD, constants as consts
from ..c14n import canonicalize
from ..base import BaseImmutableGraph, BaseGraph, BaseConnection

_PREFIX_EDGE = u'e:'
_PREFIX_VERTEX = u'v:'
_PREFIX_LITERAL = u'l:'
_KEY_GRAPHS = u'__graphs__'
_KEY_CONSTRUCT_COUNTER = u'__construct_id__'

_PREFIX2KIND = {
    _PREFIX_EDGE: consts.KIND_EDGE,
    _PREFIX_VERTEX: consts.KIND_VERTEX,
    _PREFIX_LITERAL: consts.KIND_LITERAL,
}

def connect():
    """\

    """
    return Connection(redis.Redis())


class Connection(BaseConnection):
    """\

    """
    implements(IConnection)

    def __init__(self, connection=None, readonly=False):
        """\

        `connection`
            A Redis connection.
        """
        self._conn = connection or redis.Redis()
        self._readonly = readonly
        self._graph_class = Graph if not readonly else ImmutableGraph

    def get(self, identifier, default=None):
        if self._conn.sismember(_KEY_GRAPHS, identifier):
            return self._graph_class(self._conn, identifier)
        return default

    def kind(self, identifier):
        return _PREFIX2KIND.get(identifier[:2], consts.KIND_UNKNOWN)

    def create_graph(self, identifier=None):
        if identifier and identifier in self.identifiers:
            raise KeyError()
        ident = identifier or _create_id(self._conn)
        self._conn.sadd(_KEY_GRAPHS, ident)
        return self.get(ident)

    def delete_graph(self, identifier):
        g = self.get(identifier)
        if g:
            self._conn.srem(_KEY_GRAPHS, identifier)
            g._delete()

    @property
    def identifiers(self):
        return self._conn.smembers(_KEY_GRAPHS)


class ImmutableGraph(BaseImmutableGraph):
    """\

    """
    implements(IImmutableGraph)
    
    def __init__(self, connection, identifier):
        """\

        `connection`
            A Redis connection.
        `identifier`
            The graph identifier.
        """
        self._conn = connection
        self._identifier = identifier
        self._v_key = u'g:%s:vertices' % self._identifier
        self._e_key = u'g:%s:edges' % self._identifier

    def find_vertex(self, value, datatype=None):
        dt = datatype or XSD.string
        lid = _literalid(canonicalize(value, dt), dt) + u':%s' % self._identifier
        return lid if self._conn.sismember(self._v_key, lid) else None

    def literal(self, identifier):
        glid = identifier[:identifier.rfind(':')]
        val = self._conn.get(glid)
        if val is None:
            return None
        dt = _id2datatype(identifier[2:glid.find(u':', 2)])
        return val, dt

    def ingoing_edges(self, *identifiers):
        return self._conn.sunion(['%s:ie' % ident for ident in identifiers])

    def outgoing_edges(self, *identifiers):
        return self._conn.sunion(['%s:oe' % ident for ident in identifiers])

    def head(self, edge):
        r = self._conn.zrange(edge, 0, 0)
        return r[0] if r else None

    def tail(self, edge):
        # zrange(edge, 1, -1) returns [] iff the edge represents a loop
        return self._conn.zrange(edge, 1, -1) or [self.head(edge)]

    def card(self, edge):
        return self._conn.zcount(edge, 0, 1)

    def edge_incidents(self, edge):
        return self._conn.zrange(edge, 0, -1)

    def kind(self, identifier):
        prefix = identifier[:2]
        if prefix == u'e:':
            return consts.KIND_EDGE
        elif prefix == u'l:':
            return consts.KIND_LITERAL
        return consts.KIND_VERTEX

    @property
    def vertices(self):
        return self._conn.smembers(self._v_key)

    @property
    def edges(self):
        return self._conn.smembers(self._e_key)

    @property
    def identifier(self):
        return self._identifier


class Graph(ImmutableGraph, BaseGraph):
    """\

    """
    implements(IGraph)

    def __init__(self, connection, identifier):
        super(Graph, self).__init__(connection, identifier)

    def create_vertex(self, value=None, datatype=None):
        if value:
            return self._create_literal_vertex(value, datatype or XSD.string)
        ident = _create_id(self._conn)
        self._conn.sadd(self._v_key, ident)
        return ident

    def _create_literal_vertex(self, value, datatype):
        glid = _literalid(canonicalize(value, datatype), datatype)
        lid = glid + u':%s' % self._identifier
        pipe = self._conn.pipeline()
        pipe.setnx(glid, value)\
            .sadd(self._v_key, lid)\
            .execute()
        return lid

    def create_edge(self, head, *tail):
        if not self.is_vertex(head):
            raise TypeError('The head must be a vertex')
        d = {head: 0}
        for i in tail:
            if not i:
                raise TypeError('Illegal vertex/edge: %r' % i)
            d[i] = 1
        edge = u'e:' + _create_id(self._conn)
        pipe = self._conn.pipeline()
        pipe.zadd(edge, **d)
        set_add = pipe.sadd
        set_add('%s:oe' % head, edge)
        for i in tail:
            set_add('%s:ie' % i, edge)
        set_add(self._e_key, edge)
        pipe.execute()
        return edge

    def add_tail(self, edge, *identifiers):
        d = {}
        for i in identifiers:
            if not i:
                raise TypeError('Illegal vertex/edge: %r' % i)
            d[i] = 1
        self._conn.zadd(edge, **d)

    def remove_tail(self, edge, *identifiers):
        self._conn.zrem(edge, *identifiers)

    def delete_vertex(self, vertex):
        outgoing, ingoing = '%s:oe' % vertex, '%s:ie' % vertex
        edges = tuple(self._conn.sunion(ingoing, outgoing))
        for edge in edges:
            self.delete_edge(edge)
        pipe = self._conn.pipeline()
        pipe.delete(vertex, ingoing, outgoing, *edges) \
            .srem(self._v_key, vertex) \
            .execute()

    def delete_edge(self, edge):
        conn = self._conn
        targets = conn.zrange(edge, 0, -1)
        if not targets:
            return
        pipe = self._conn.pipeline()
        set_remove = pipe.srem
        set_remove(self._e_key, edge)
        set_remove('%s:oe' % targets[0], edge)
        for t in targets[1:]:
            set_remove('%s:ie' % t, edge)
        pipe.delete(edge) \
            .execute()

    def _delete(self):
        conn = self._conn
        v_key, e_key = self._v_key, self._e_key
        pipe = self._conn.pipeline()
        pipe.delete(conn.smembers(v_key)) \
            .delete(conn.smembers(e_key)) \
            .delete(e_key, v_key) \
            .execute()


def _create_id(redis_conn):
    return str(redis_conn.incr(_KEY_CONSTRUCT_COUNTER))

def _literalid(value, datatype):
    did = _datatype2id(datatype)
    vh = _valuehash(value)
    return 'l:%d:%s' % (did, vh)

def _id2datatype(i):
    return consts.XSDID2URI.get(int(i))

def _datatype2id(iri):
    return consts.XSDURI2ID.get(iri)

def _valuehash(s):
    return hashlib.sha1(str(s)).hexdigest()

