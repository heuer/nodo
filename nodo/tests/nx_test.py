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
Abstract NetworkX tests.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from nose.tools import ok_, eq_, raises
from nodo import constants, XSD, nxutils

class AbstractNXTest(object):

    def setUp(self):
        self.graph = self.create_empty_graph()

    def tearDown(self):
        self.delete_graph(self.graph)

    def create_empty_graph(self):
        """\
        Returns a new empty, modifiable `IGraph` instance.
        """
        raise NotImplementedError()

    def delete_graph(self, graph):
        """\
        Deletes a graph.
        """
        raise NotImplementedError()

    def test_not2uniform(self):
        g = self.graph
        v1, v2, v3 = g.create_vertex(), g.create_vertex(), g.create_vertex()
        e = g.create_edge(v1, v2, v3)
        try:
            nxutils.to_nx(g)
            self.fail('The graph is not 2-uniform. Expected a ValueError')
        except ValueError:
            pass

    def test_convert(self):
        g = self.graph
        v1, v2, v3, v4 = g.create_vertex(), g.create_vertex(), g.create_vertex(), g.create_vertex()
        e1 = g.create_edge(v1, v2)
        e2 = g.create_edge(v3, v4)
        e3 = g.create_edge(v1, v4)
        nx = nxutils.to_nx(g)
        ok_(nx)
        ok_(4 == nx.number_of_nodes())
        ok_(4 == nx.order())
        for v in (v1, v2, v3, v4):
            ok_(nx.has_node(v))
        ok_(nx.has_edge(v1, v2))
        ok_(nx.has_edge(v3, v4))
        ok_(nx.has_edge(v1, v4))
        ok_(g.degree(v1) == nx.degree(v1))

    def test_convert2(self):
        g = self.graph
        val1 = u'Pitje Puck'
        val2 = 1
        lit1 = val1, XSD.string
        lit2 = str(val2), XSD.integer
        v1, v2, v3, v4 = g.create_vertex(val1), g.create_vertex(), g.create_integer_vertex(val2), g.create_vertex()
        e1 = g.create_edge(v1, v2)
        e2 = g.create_edge(v3, v4)
        e3 = g.create_edge(v1, v4)
        nx = nxutils.to_nx(g)
        ok_(nx)
        ok_(4 == nx.number_of_nodes())
        ok_(4 == nx.order())
        ok_(nx.has_node(lit1))
        ok_(nx.has_node(v2))
        ok_(nx.has_node(lit2))
        ok_(nx.has_node(v4))
        ok_(nx.has_edge(lit1, v2))
        ok_(nx.has_edge(lit2, v4))
        ok_(nx.has_edge(lit1, v4))
        ok_(g.degree(v1) == nx.degree(lit1))
