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
Abstract graph tests.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from nodo import constants, XSD

class AbstractGraphTest(object):

    def setUp(self):
        self.graph = self.create_empty_graph()

    def tearDown(self):
        self.delete_graph(self.graph)

    def test_kind_vertex(self):
        g = self.graph
        v = g.create_vertex()
        self.assert_(g.is_vertex(v))
        self.assert_(constants.KIND_VERTEX == g.kind(v))

    def test_kind_edge(self):
        g = self.graph
        v1, v2 = g.create_vertex(), g.create_vertex()
        e = g.create_edge(v1, v2)
        self.assert_(g.is_edge(e))
        self.assert_(constants.KIND_EDGE == g.kind(e))

    def test_create_vertex(self):
        g = self.graph
        v = g.create_vertex()
        self.assert_(v)
        self.assert_(v in g)
        self.assert_(v in g.vertices)

    def test_create_string_vertex(self):
        g = self.graph
        v1 = g.find_string_vertex(u'hello')
        self.assert_(not v1)
        v1 = g.create_string_vertex(u'hello')
        self.assert_(v1)
        v2 = g.create_string_vertex(u'hello')
        self.assert_(v2)
        self.assert_(v1 == v2)
        self.assert_(v1 == g.find_string_vertex(u'hello'))
        self.assert_(g.literal(v1) == (u'hello', XSD.string))

    def test_create_integer_vertex(self):
        g = self.graph
        v1 = g.find_integer_vertex(666)
        self.assert_(not v1)
        v1 = g.create_integer_vertex(666)
        self.assert_(v1)
        v2 = g.create_integer_vertex(666)
        self.assert_(v2)
        self.assert_(v1 == v2)
        self.assert_(v1 == g.find_integer_vertex(666))
        self.assert_(g.literal(v1) == (666, XSD.integer))

    def test_create_edge(self):
        g = self.graph
        v1 = g.create_vertex()
        v2 = g.create_vertex()
        self.assert_(v1)
        self.assert_(v2)
        self.assert_(v1 in g)
        self.assert_(v2 in g)
        self.assert_(v1 in g.vertices)
        self.assert_(v2 in g.vertices)

        e = g.create_edge(v1, v2)
        self.assert_(e)
        self.assert_(e in g)
        self.assert_(e in g.edges)

    def test_rank_card(self):
        g = self.graph
        v1, v2, v3 = g.create_vertex(), g.create_vertex(), g.create_vertex()
        self.assert_(0 == g.rank())
        e1 = g.create_edge(v1, v2)
        self.assert_(2 == g.card(e1))
        self.assert_(2 == g.rank())
        e2 = g.create_edge(v1, v2, v3)
        self.assert_(3 == g.card(e2))
        self.assert_(3 == g.rank())

    def test_degree(self):
        g = self.graph
        v1, v2, v3 = g.create_vertex(), g.create_vertex(), g.create_vertex()
        self.assert_(0 == g.degree(v1))
        self.assert_(0 == g.degree(v2))
        self.assert_(0 == g.degree(v3))
        e1 = g.create_edge(v1, v2)
        self.assert_(0 == g.degree(v1))
        self.assert_(1 == g.degree(v2))
        e2 = g.create_edge(v1, v2, v3)
        self.assert_(2 == g.degree(v2))
        self.assert_(1 == g.degree(v3))

    def test_edge_targets(self):
        g = self.graph
        v1, v2, v3 = g.create_vertex(), g.create_vertex(), g.create_vertex()
        edge = g.create_edge(v1, v2)
        self.assert_(v1 in g.edge_targets(edge))
        self.assert_(v2 in g.edge_targets(edge))
        self.assert_(v3 not in g.edge_targets(edge))

    def test_edge_contains(self):
        g = self.graph
        v1, v2, v3 = g.create_vertex(), g.create_vertex(), g.create_vertex()
        edge = g.create_edge(v1, v2)
        self.assert_(g.edge_contains(edge, v1))
        self.assert_(g.edge_contains(edge, v2))
        self.assert_(g.edge_contains(edge, v1, v2))
        self.assert_(not g.edge_contains(edge, v3))
        self.assert_(not g.edge_contains(edge, v1, v2, v3))

    def test_uniform(self):
        g = self.graph
        v1, v2, v3, v4 = g.create_vertex(), g.create_vertex(), g.create_vertex(), g.create_vertex()
        self.assert_(g.is_uniform())
        e1 = g.create_edge(v1, v2)
        self.assert_(g.is_uniform())
        self.assert_(g.is_uniform(2))
        e2 = g.create_edge(v1, v2, v3)
        self.assert_(not g.is_uniform())
        self.assert_(not g.is_uniform(2))
        self.assert_(not g.is_uniform(3))
        g.delete_edge(e2)
        self.assert_(g.is_uniform())
        self.assert_(not g.is_uniform(2))
        self.assert_(g.is_uniform(3))
        e3 = g.create_edge(v1, v3, v4)
        self.assert_(g.is_uniform())
        self.assert_(not g.is_uniform(2))
        self.assert_(g.is_uniform(3))

    def test_edge_head(self):
        g = self.graph
        v1, v2 = g.create_vertex(), g.create_vertex()
        e = g.create_edge(v1, v2)
        self.assert_(g.head(e) == v1)

    def test_edge_tail(self):
        g = self.graph
        v1, v2 = g.create_vertex(), g.create_vertex()
        e = g.create_edge(v1, v2)
        self.assert_((v2,) == tuple(g.tail(e)))

    def test_edge_tail2(self):
        g = self.graph
        v1, v2, v3, v4 = g.create_vertex(), g.create_vertex(), g.create_vertex(), g.create_vertex()
        e = g.create_edge(v1, v2, v3, v4)
        self.assert_(tuple(sorted([v2, v3, v4])) == tuple(sorted(g.tail(e))))

    def test_neighbour(self):
        g = self.graph
        v1, v2 = g.create_vertex(), g.create_vertex()
        self.assert_(not g.is_neighbour(v1, v2))
        g.create_edge(v1, v2)
        self.assert_(g.is_neighbour(v1, v2))
        self.assert_(v1 in g.neighbours(v2))
        self.assert_(v2 in g.neighbours(v1))

    def test_predecessors(self):
        g = self.graph
        v1, v2, v3, v4 = g.create_vertex(), g.create_vertex(), g.create_vertex(), g.create_vertex()
        for v in [v1, v2, v3, v4]:
            self.assert_(() == tuple(g.predecessors(v)))
        e1 = g.create_edge(v1, v2)
        self.assert_(v1 in g.predecessors(v2))
        e2 = g.create_edge(v1, v3)
        e4 = g.create_edge(v3, v4)
        self.assert_(v1 in g.predecessors(v3))
        self.assert_(v3 in g.predecessors(v4))
        res = tuple(g.predecessors(v3, v4))
        self.assert_(v1 in res and v3 in res)
        

       
