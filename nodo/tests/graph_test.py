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
from nose.tools import ok_, eq_, raises
from nodo import constants, XSD
from abstract_test import AbstractTest

class AbstractGraphTest(AbstractTest):

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

    def test_kind_literal(self):
        g = self.graph
        v = g.create_vertex(u'Pitje Puck')
        self.assert_(g.is_literal(v))
        self.assert_(g.is_vertex(v))
        self.assert_(constants.KIND_LITERAL == g.kind(v))

    def test_create_vertex(self):
        g = self.graph
        v = g.create_vertex()
        self.assert_(v)
        self.assert_(v in g)
        self.assert_(v in g.vertices())

    def test_create_string_vertex(self):
        g = self.graph
        v1 = g.find_vertex(u'hello')
        self.assert_(not v1)
        v1 = g.create_vertex(u'hello')
        self.assert_(v1)
        self.assert_(v1 in g)
        self.assert_(v1 in g.vertices())
        v2 = g.create_vertex(u'hello')
        self.assert_(v2)
        self.assert_(v1 == v2)
        self.assert_(v1 == g.find_vertex(u'hello'))
        self.assert_(g.literal(v1) == (u'hello', XSD.string))

    def test_create_integer_vertex(self):
        g = self.graph
        v1 = g.find_integer_vertex(1)
        self.assert_(not v1)
        v1 = g.create_integer_vertex(1)
        self.assert_(v1)
        self.assert_(v1 in g)
        self.assert_(v1 in g.vertices())
        v2 = g.create_integer_vertex(1)
        self.assert_(v2)
        self.assert_(v1 == v2)
        self.assert_(v1 == g.find_integer_vertex(1))
        self.assert_(g.literal(v1) == (str(1), XSD.integer))

    def test_create_integer_vertex2(self):
        g = self.graph
        v1 = g.find_integer_vertex(666)
        self.assert_(not v1)
        v1 = g.create_integer_vertex(666)
        self.assert_(v1)
        self.assert_(v1 in g)
        self.assert_(v1 in g.vertices())
        v2 = g.create_integer_vertex(666)
        self.assert_(v2)
        self.assert_(v1 == v2)
        self.assert_(v1 == g.find_integer_vertex(666))
        self.assert_(g.literal(v1) == (str(666), XSD.integer))

    def test_create_edge(self):
        g = self.graph
        v1 = g.create_vertex()
        v2 = g.create_vertex()
        self.assert_(v1)
        self.assert_(v2)
        self.assert_(v1 in g)
        self.assert_(v2 in g)
        self.assert_(v1 in g.vertices())
        self.assert_(v2 in g.vertices())

        e = g.create_edge(v1, v2)
        self.assert_(e)
        self.assert_(e in g)
        self.assert_(e in g.edges())

    def test_rank_card(self):
        g = self.graph
        v1, v2, v3 = g.create_vertex(), g.create_vertex(), g.create_vertex()
        self.assert_(0 == g.rank())
        self.assert_(0 == g.corank())
        e1 = g.create_edge(v1, v2)
        self.assert_(2 == g.card(e1))
        self.assert_(2 == g.rank())
        self.assert_(2 == g.corank())
        e2 = g.create_edge(v1, v2, v3)
        self.assert_(3 == g.card(e2))
        self.assert_(3 == g.rank())
        self.assert_(2 == g.corank())

    def test_indegree(self):
        g = self.graph
        v1, v2, v3 = g.create_vertex(), g.create_vertex(), g.create_vertex()
        self.assert_(0 == g.indegree(v1))
        self.assert_(0 == g.indegree(v2))
        self.assert_(0 == g.indegree(v3))
        e1 = g.create_edge(v1, v2)
        self.assert_(0 == g.indegree(v1))
        self.assert_(1 == g.indegree(v2))
        e2 = g.create_edge(v1, v2, v3)
        self.assert_(2 == g.indegree(v2))
        self.assert_(1 == g.indegree(v3))

    def test_outdegree(self):
        g = self.graph
        v1, v2, v3 = g.create_vertex(), g.create_vertex(), g.create_vertex()
        self.assert_(0 == g.outdegree(v1))
        self.assert_(0 == g.outdegree(v2))
        self.assert_(0 == g.outdegree(v3))
        e1 = g.create_edge(v1, v2)
        self.assert_(1 == g.outdegree(v1))
        self.assert_(0 == g.outdegree(v2))
        e2 = g.create_edge(v1, v2, v3)
        self.assert_(2 == g.outdegree(v1))
        self.assert_(0 == g.outdegree(v2))
        self.assert_(0 == g.outdegree(v3))

    def test_edge_incidents(self):
        g = self.graph
        v1, v2, v3 = g.create_vertex(), g.create_vertex(), g.create_vertex()
        edge = g.create_edge(v1, v2)
        self.assert_(v1 in g.edge_incidents(edge))
        self.assert_(v2 in g.edge_incidents(edge))
        self.assert_(v3 not in g.edge_incidents(edge))

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
        self.assert_(e2 not in g)
        self.assert_(g.is_uniform())
        self.assert_(g.is_uniform(2))
        self.assert_(not g.is_uniform(3))
        e3 = g.create_edge(v1, v3, v4)
        g.delete_edge(e1)
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
        self.assert_(g.is_neighbour(v2, v1))
        self.assert_(v1 in g.neighbours(v2))
        self.assert_(v2 in g.neighbours(v1))

    def test_neighbour2(self):
        g = self.graph
        v1, v2, v3 = g.create_vertex(), g.create_vertex(), g.create_vertex()
        ok_(not g.is_neighbour(v1, v2))
        ok_(not g.is_neighbour(v1, v3))
        ok_(not g.is_neighbour(v2, v3))
        ok_(not g.is_neighbour(v2, v1))
        g.create_edge(v1, v2, v3)
        ok_(g.is_neighbour(v1, v2))
        ok_(g.is_neighbour(v2, v1))
        ok_(g.is_neighbour(v3, v1))
        ok_(g.is_neighbour(v1, v3))
        ok_(not g.is_neighbour(v1, v1))
        ok_(v1 not in g.neighbours(v1))
        ok_(v2 in g.neighbours(v1))
        ok_(v3 in g.neighbours(v1))
        ok_(v1 in g.neighbours(v2))
        ok_(v2 not in g.neighbours(v2))
        ok_(v3 not in g.neighbours(v2))
        ok_(v1 in g.neighbours(v3))
        ok_(v2 not in g.neighbours(v3))
        ok_(v3 not in g.neighbours(v3))

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

    def test_successors(self):
        g = self.graph
        v1, v2, v3, v4 = g.create_vertex(), g.create_vertex(), g.create_vertex(), g.create_vertex()
        for v in [v1, v2, v3, v4]:
            self.assert_(() == tuple(g.successors(v)))
        e1 = g.create_edge(v1, v2)
        self.assert_(v2 in g.successors(v1))
        e2 = g.create_edge(v2, v3, v4)
        self.assert_(v1 not in g.successors(v2))
        self.assert_(v2 not in g.successors(v2))
        self.assert_(v3 in g.successors(v2))
        self.assert_(v4 in g.successors(v2))

    def test_create_egde_illegal(self):
        g = self.graph
        v1, v2 = g.create_vertex(), g.create_vertex()
        e = g.create_edge(v1, v2)
        self.assert_(e)
        try:
            g.create_edge(e, v1)
            self.fail('An edge cannot be used as head/source. Expected a TypeError')
        except TypeError:
            pass

    def test_create_egde_illegal2(self):
        g = self.graph
        v1, v2 = g.create_vertex(), g.create_vertex()
        e = g.create_edge(v1, v2)
        self.assert_(e)
        try:
            g.create_edge(None, v2)
            self.fail('None is not allowed as head')
        except TypeError:
            pass

    def test_create_egde_illegal3(self):
        g = self.graph
        v1, v2 = g.create_vertex(), g.create_vertex()
        e = g.create_edge(v1, v2)
        self.assert_(e)
        try:
            g.create_edge(v1, None)
            self.fail('None is not allowed as tail')
        except TypeError:
            pass

    def test_lit_c14n(self):
        g = self.graph
        v1 = g.find_vertex('00001', XSD.integer)
        self.assert_(not v1)
        v1 = g.create_vertex('00001', XSD.integer)
        self.assert_(v1)
        self.assert_(u'1', g.literal(v1)[0])

    def test_lit_boolean(self):
        g = self.graph
        v1 = g.find_vertex('1', XSD.boolean)
        self.assert_(not v1)
        v1 = g.create_vertex('1', XSD.boolean)
        self.assert_(v1)
        self.assert_(u'true', g.literal(v1)[0])

    def test_lit_boolean2(self):
        g = self.graph
        v1 = g.find_vertex('true', XSD.boolean)
        self.assert_(not v1)
        v1 = g.create_vertex('true', XSD.boolean)
        self.assert_(v1)
        self.assert_(u'true', g.literal(v1)[0])

    def test_lit_boolean3(self):
        g = self.graph
        v1 = g.find_vertex('0', XSD.boolean)
        self.assert_(not v1)
        v1 = g.create_vertex('0', XSD.boolean)
        self.assert_(v1)
        self.assert_(u'false', g.literal(v1)[0])

    def test_lit_boolean4(self):
        g = self.graph
        v1 = g.find_vertex('false', XSD.boolean)
        self.assert_(not v1)
        v1 = g.create_vertex('false', XSD.boolean)
        self.assert_(v1)
        self.assert_(u'false', g.literal(v1)[0])

    def test_lit_edges(self):
        g = self.graph
        v1 = g.create_vertex(u'Pumuckl')
        v2 = g.create_vertex(u'Meister Eder')
        self.assert_(len(tuple(g.outgoing_edges(v1))) == 0)
        self.assert_(len(tuple(g.ingoing_edges(v2))) == 0)
        e = g.create_edge(v1, v2)
        self.assert_(e in g.outgoing_edges(v1))
        self.assert_(e in g.ingoing_edges(v2))

        g2 = self.create_empty_graph()
        g2v1 = g2.create_vertex(u'Pumuckl')
        g2v2 = g2.create_vertex(u'Meister Eder')
        self.assert_(len(tuple(g2.outgoing_edges(g2v1))) == 0)
        self.assert_(len(tuple(g2.ingoing_edges(g2v2))) == 0)
        g2e = g.create_edge(g2v1, g2v2)
        self.assert_(g2e in g2.outgoing_edges(g2v1))
        self.assert_(g2e in g2.ingoing_edges(g2v2))

        self.delete_graph(g2)

    def test_edge_edges(self):
        g = self.graph
        v1, v2, v3, v4 = g.create_vertex(), g.create_vertex(), g.create_vertex(), g.create_vertex()
        e1 = g.create_edge(v1, v2)
        e2 = g.create_edge(v1, e1)
        self.assert_(e1 in g.outgoing_edges(v1))
        self.assert_(e1 in g.ingoing_edges(v2))
        self.assert_(e2 in g.ingoing_edges(e1))

    def test_literal(self):
        g = self.graph
        value = u'Pumuckl'
        v = g.create_vertex(value)
        self.assert_((value, XSD.string) == g.literal(v))

    def test_literal2(self):
        g = self.graph
        v = g.create_vertex()
        self.assert_(None is g.literal(v))

    def test_value(self):
        g = self.graph
        value = u'Pumuckl'
        v = g.create_vertex(value)
        self.assert_(value == g.value(v))

    def test_value2(self):
        g = self.graph
        v = g.create_vertex()
        self.assert_(None is g.value(v))

    def test_datatype(self):
        g = self.graph
        value = u'Pumuckl'
        v = g.create_vertex(value)
        self.assert_(XSD.string == g.datatype(v))

    def test_datatype2(self):
        g = self.graph
        v = g.create_vertex()
        self.assert_(None is g.datatype(v))

    def test_delete_vertex(self):
        g = self.graph
        v = g.create_vertex()
        self.assert_(v in g)
        self.assert_(v in g.vertices())
        self.assert_((v,) == tuple(g.vertices()))
        g.delete_vertex(v)
        self.assert_(v not in g)
        self.assert_(v not in g.vertices())
        self.assert_(tuple() == tuple(g.vertices()))

    def test_delete_vertex2(self):
        g = self.graph
        v = g.create_vertex('Pumuckl')
        self.assert_(v in g)
        self.assert_(v in g.vertices())
        self.assert_((v,) == tuple(g.vertices()))
        g.delete_vertex(v)
        self.assert_(v not in g)
        self.assert_(v not in g.vertices())
        self.assert_(tuple() == tuple(g.vertices()))

    def test_delete_vertex3(self):
        g = self.graph
        v1, v2 = g.create_vertex(), g.create_vertex()
        self.assert_(v1 in g)
        self.assert_(v1 in g.vertices())
        self.assert_(v2 in g)
        self.assert_(v2 in g.vertices())
        e = g.create_edge(v1, v2)
        self.assert_(e in g)
        g.delete_vertex(v1)
        self.assert_(v1 not in g)
        self.assert_(v1 not in g.vertices())
        self.assert_(e not in g)

    def test_delete_vertex4(self):
        g = self.graph
        v = g.create_vertex()
        self.assert_(v in g)
        self.assert_(v in g.vertices())
        self.assert_((v,) == tuple(g.vertices()))
        g.delete(v)
        self.assert_(v not in g)
        self.assert_(v not in g.vertices())
        self.assert_(tuple() == tuple(g.vertices()))

    def test_delete_vertex5(self):
        g = self.graph
        v = g.create_vertex()
        self.assert_(v in g)
        self.assert_(v in g.vertices())
        self.assert_((v,) == tuple(g.vertices()))
        del g[v]
        self.assert_(v not in g)
        self.assert_(v not in g.vertices())
        self.assert_(tuple() == tuple(g.vertices()))

    def test_add_tail(self):
        g = self.graph
        v1, v2, v3 = g.create_vertex(), g.create_vertex(), g.create_vertex()
        e = g.create_edge(v1, v2)
        self.assert_(v2 in g.tail(e))
        self.assert_(v3 not in g.tail(e))
        g.add_tail(e, v3)
        self.assert_(v2 in g.tail(e))
        self.assert_(v3 in g.tail(e))

    def test_add_tail2(self):
        g = self.graph
        v1, v2, v3, v4 = g.create_vertex(), g.create_vertex(), g.create_vertex(), g.create_vertex()
        e = g.create_edge(v1, v2)
        self.assert_(v2 in g.tail(e))
        self.assert_(v3 not in g.tail(e))
        self.assert_(v4 not in g.tail(e))
        g.add_tail(e, v3, v4)
        self.assert_(v2 in g.tail(e))
        self.assert_(v3 in g.tail(e))
        self.assert_(v4 in g.tail(e))

    def test_remove_tail(self):
        g = self.graph
        v1, v2, v3 = g.create_vertex(), g.create_vertex(), g.create_vertex()
        e = g.create_edge(v1, v2, v3)
        self.assert_(v2 in g.tail(e))
        self.assert_(v3 in g.tail(e))
        g.remove_tail(e, v3)
        self.assert_(v2 in g.tail(e))
        self.assert_(v3 not in g.tail(e))

    def test_remove_tail2(self):
        g = self.graph
        v1, v2, v3, v4 = g.create_vertex(), g.create_vertex(), g.create_vertex(), g.create_vertex()
        e = g.create_edge(v1, v2, v3, v4)
        self.assert_(v2 in g.tail(e))
        self.assert_(v3 in g.tail(e))
        self.assert_(v4 in g.tail(e))
        g.remove_tail(e, v3, v4)
        self.assert_(v2 in g.tail(e))
        self.assert_(v3 not in g.tail(e))
        self.assert_(v4 not in g.tail(e))

    def test_remove_tail3(self):
        g = self.graph
        v1, v2, v3, v4 = g.create_vertex(), g.create_vertex(), g.create_vertex(), g.create_vertex()
        e = g.create_edge(v1, v2, v3, v4)
        self.assert_(v2 in g.tail(e))
        self.assert_(v3 in g.tail(e))
        self.assert_(v4 in g.tail(e))
        try:
            g.remove_tail(e, v1)
            self.fail("Expected a ValueError for removing the edge's head")
        except ValueError:
            pass

    def test_remove_tail4(self):
        g = self.graph
        v1, v2, v3, v4 = g.create_vertex(), g.create_vertex(), g.create_vertex(), g.create_vertex()
        e = g.create_edge(v1, v2, v3, v4)
        self.assert_(v2 in g.tail(e))
        self.assert_(v3 in g.tail(e))
        self.assert_(v4 in g.tail(e))
        try:
            g.remove_tail(e, v2, v1)
            self.fail("Expected a ValueError for removing the edge's head")
        except ValueError:
            pass

    def test_replace_tail(self):
        g = self.graph
        v1, v2, v3 = g.create_vertex(), g.create_vertex(), g.create_vertex()
        e = g.create_edge(v1, v2)
        self.assert_(v1 == g.head(e))
        self.assert_((v2,) == tuple(g.tail(e)))
        e = g.replace_tail(e, v3)
        self.assert_(v1 == g.head(e))
        self.assert_((v3,) == tuple(g.tail(e)))

    def test_loop(self):
        g = self.graph
        v = g.create_vertex()
        e = g.create_edge(v, v)
        eq_(1, g.indegree(v))
        eq_(1, g.outdegree(v))
        eq_(2, g.degree(v))
        ok_(e in g.ingoing_edges(v))
        ok_(e in g.outgoing_edges(v))
        ok_(1 == g.card(e))
        ok_(v == g.head(e))
        ok_((v,) == tuple(g.tail(e)))
        ok_(v in g.predecessors(v))
        ok_(v in g.successors(v))
        ok_(v in g.neighbours(v))
        ok_(g.is_neighbour(v, v))

    def test_clear(self):
        g = self.graph
        v1, v2, v3 = g.create_vertex(), g.create_vertex(), g.create_vertex()
        e1 = g.create_edge(v1, v2)
        e2 = g.create_edge(v1, v3)
        e3 = g.create_edge(v1, v2, v3)
        ok_(v1 in g)
        ok_(v2 in g)
        ok_(v3 in g)
        ok_(e1 in g)
        ok_(e2 in g)
        ok_(e3 in g)
        g.clear()
        ok_(v1 not in g)
        ok_(v2 not in g)
        ok_(v3 not in g)
        ok_(e1 not in g)
        ok_(e2 not in g)
        ok_(e3 not in g)

    def test_edge_between(self):
        g = self.graph
        v1, v2, v3 = g.create_vertex(), g.create_vertex(), g.create_vertex()
        e = g.create_edge(v1, v2)
        ok_(e == g.edge_between(v1, v2))
        ok_(g.edge_between(v2, v1) is None)
        ok_(g.edge_between(v1, v3) is None)
        ok_(g.edge_between(v3, v1) is None)

    def test_merge_vertices_simple(self):
        g = self.graph
        v1, v2 = g.create_vertex(), g.create_vertex()
        ok_(2 == len(g))
        v3 = g.merge_vertices(v1, v2)
        ok_(1 == len(g))

    def test_merge_same_vertix(self):
        g = self.graph
        v = g.create_vertex()
        eq_(1, len(g))
        merged = g.merge_vertices(v, v)
        eq_(1, len(g))
        eq_(v, merged)

    def test_merge_vertices(self):
        g = self.graph
        v1, v2 = g.create_vertex(), g.create_vertex()
        e = g.create_edge(v1, v2)
        eq_(1, g.outdegree(v1))
        eq_(0, g.indegree(v1))
        eq_(0, g.outdegree(v2))
        eq_(1, g.indegree(v2))
        eq_(2, len(g))
        v3 = g.merge_vertices(v1, v2)
        eq_(1, len(g))
        eq_(0, g.indegree(v3))
        eq_(0, g.outdegree(v3))

    def test_merge_vertices2(self):
        g = self.graph
        v1, v2, v3, v4 = g.create_vertex(), g.create_vertex(), g.create_vertex(), g.create_vertex()
        e1 = g.create_edge(v1, v2)
        e2 = g.create_edge(v2, v3)
        e3 = g.create_edge(v4, v2)
        eq_(4, len(g))
        vm = g.merge_vertices(v1, v2)
        eq_(3, len(g))
        ok_(v3 in g.successors(vm))
        ok_(v4 in g.predecessors(vm))
        eq_(1, g.indegree(vm))
        eq_(1, g.outdegree(vm))
        
    def test_merge_vertices3(self):
        g = self.graph
        v1, v2 = g.create_vertex(u'Hello'), g.create_vertex()
        eq_(2, len(g))
        v3 = g.merge_vertices(v1, v2)
        eq_(1, len(g))
        ok_(u'Hello' == g.value(v3))
        ok_(XSD.string == g.datatype(v3))

    def test_merge_vertices4(self):
        g = self.graph
        v1, v2 = g.create_vertex(), g.create_vertex(u'Hello')
        eq_(2, len(g))
        v3 = g.merge_vertices(v1, v2)
        eq_(1, len(g))
        ok_(u'Hello' == g.value(v3))
        ok_(XSD.string == g.datatype(v3))

    def test_merge_vertices_illegal(self):
        g = self.graph
        v1, v2 = g.create_vertex(u'Hello'), g.create_vertex(u'there')
        try:
            g.merge_vertices(v1, v2)
            self.fail('Expecting a TypeError')
        except TypeError:
            pass
        ok_(2 == len(g))
