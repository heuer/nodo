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
This module provides some default implementations of the `interfaces`
module.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import absolute_import
from itertools import chain
from . import XSD, constants as consts
from .interfaces import IImmutableGraph, IGraph, IConnection, implements


class BaseImmutableGraph(object):
    """\
    Provides some default implementations for an `IImmutableGraph`
    implementation.
    """
    def find_integer_vertex(self, value):
        return self.find_vertex(value, XSD.integer)

    def find_iri_vertex(self, value):
        return self.find_vertex(value, XSD.anyURI)

    def is_edge(self, identifier):
        return self.kind(identifier) == consts.KIND_EDGE

    def is_vertex(self, identifier):
        return self.kind(identifier) in (consts.KIND_VERTEX, consts.KIND_LITERAL)

    def is_literal(self, identifier):
        return self.kind(identifier) == consts.KIND_LITERAL

    def neighbours(self, *identifiers):
        return chain(self.predecessors(*identifiers), self.successors(*identifiers))

    def is_neighbour(self, v1, v2):
        return v2 in self.neighbours(v1)

    def value(self, identifier):
        lit = self.literal(identifier)
        return lit[0] if lit else None

    def datatype(self, identifier):
        lit = self.literal(identifier)
        return lit[1] if lit else None

    def predecessors(self, *identifiers):
        head = self.head
        return (head(edge) for edge in self.ingoing_edges(*identifiers))

    def successors(self, *identifiers):
        for edge in self.outgoing_edges(*identifiers):
            for target in self.tail(edge):
                yield target

    def rank(self):
        card = self.card
        try:
            return max((card(e) for e in self.edges()))
        except ValueError:
            return 0

    def corank(self):
        card = self.card
        try:
            return min((card(e) for e in self.edges()))
        except ValueError:
            return 0

    def card(self, edge):
        s = set(self.tail(edge))
        s.add(self.head(edge))
        return len(s)

    def indegree(self, identifier):
        return sum(1 for e in self.ingoing_edges(identifier))

    def outdegree(self, identifier):
        return sum(1 for e in self.outgoing_edges(identifier))

    def degree(self, identifier):
        return self.indegree(identifier) + self.outdegree(identifier)

    def is_uniform(self, k=None):
        card = self.card
        for e in self.edges():
            if not k:
                k = card(e)
                continue
            if k != card(e):
                return False
        return True

    def edge_incidents(self, edge):
        return set(chain([self.head(edge)], self.tail(edge)))

    def edge_contains(self, edge, *identifiers):
        s = set(self.edge_incidents(edge))
        for ident in identifiers:
            if not ident in s:
                return False
        return True

    def edges_between(self, head, tail):
        return set(self.outgoing_edges(head)).intersection(self.ingoing_edges(tail))

    def edge_between(self, head, tail):
        for e in self.edges_between(head, tail):
            return e
        return None

    def __contains__(self, identifier):
        return identifier in chain(self.vertices(), self.edges())

    def __iter__(self):
        return self.vertices()

    def __len__(self):
        return sum(1 for v in self.vertices())


class BaseGraph(BaseImmutableGraph):
    """\
    Provides some default implementations for a `IGraph` implementation.
    """
    def create_iri_vertex(self, value):
        return self.create_vertex(value, XSD.anyURI)

    def create_integer_vertex(self, value):
        return self.create_vertex(value, XSD.integer)

    def replace_tail(self, edge, *identifiers):
        e = self.create_edge(self.head(edge), *identifiers)
        self.delete_edge(edge)
        return e

    def merge_vertices(self, a, b):
        if a == b:
            return a
        a_lit, b_lit = self.is_literal(a), self.is_literal(b)
        if a_lit and b_lit:
            raise TypeError('Cannot merge literal vertices')
        if b_lit:
            a, b = b, a
        for e in chain(tuple(self.edges_between(a, b)), tuple(self.edges_between(b, a))):
            self.delete_edge(e)
        for e in self.ingoing_edges(b):
            tail = set(self.tail(e))
            tail.remove(b)
            tail.add(a)
            self.create_edge(self.head(e), *tail)
        for e in self.outgoing_edges(b):
            self.create_edge(a, *self.tail(e))
        self.delete_vertex(b)
        return a

    def delete(self, identifier):
        if self.is_edge(identifier):
            self.delete_edge(identifier)
        else:
            self.delete_vertex(identifier)

    def __delitem__(self, identifier):
        self.delete(identifier)


class BaseConnection(object):
    """\
    Provides some default implementations for an ``IConnection` implementation.
    """
    def __getitem__(self, key):
        graph = self.get(key)
        if graph is None:
            raise KeyError('The key "%s" does not exist' % key)
        return graph

    def __contains__(self, graph):
        return graph in self.identifiers
