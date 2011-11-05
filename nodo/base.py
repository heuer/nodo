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
from itertools import chain
from . import XSD, constants as consts
from .interfaces import IImmutableGraph, IGraph, IConnection, implements

class BaseImmutableGraph(object):
    """\
    Provides some default implementations for an `IImmutableGraph`
    implementation.
    """
    def find_string_vertex(self, value):
        return self.find_literal_vertex(value, XSD.string)

    def find_integer_vertex(self, value):
        return self.find_literal_vertex(value, XSD.integer)

    def find_iri_vertex(self, value):
        return self.find_literal_vertex(value, XSD.anyURI)

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
            return max((card(e) for e in self.edges))
        except ValueError:
            return 0

    def card(self, edge):
        return len(self.tail(edge)) + 1

    def degree(self, vertex):
        return sum(1 for e in self.ingoing_edges(vertex))

    def is_uniform(self, k=None):
        card = self.card
        for e in self.edges:
            if not k:
                k = card(e)
                continue
            if k != card(e):
                return False
        return True

    def edge_targets(self, edge):
        return chain([self.head(edge)], self.tail(edge))

    def edge_contains(self, edge, *identifiers):
        s = set(self.edge_targets(edge))
        for ident in identifiers:
            if not ident in s:
                return False
        return True

    def __contains__(self, identifier):
        return identifier in chain(self.vertices, self.edges)

    def __iter__(self):
        return self.vertices

    def __len__(self):
        return len(self.vertices)


class BaseGraph(BaseImmutableGraph):
    """\
    Provides some default implementations for a `IGraph` implementation.
    """
    def create_iri_vertex(self, value):
        return self.create_vertex(value, XSD.anyURI)

    def create_integer_vertex(self, value):
        return self.create_vertex(value, XSD.integer)

    def delete(self, identifier):
        if is_edge(identifier):
            self.delete_edge(identifier)
        else:
            self.delete_vertex(identifier)


class BaseConnection(object):
    """\
    Provides some default implementations for an ``IConnection` implementation.
    """
    def __getitem__(self, key):
        graph = self.get(key)
        if graph is None:
            raise KeyError('The key "%s" does not exist' % key)
        return graph

    def __contains__(self, key):
        return graph in self.identifiers
