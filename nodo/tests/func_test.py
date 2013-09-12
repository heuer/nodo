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
Abstract functional tests

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from nose.tools import ok_
from nodo import XSD, func as f
from abstract_test import AbstractTest


class AbstractFunctionalTest(AbstractTest):

    def test_vertex(self):
        g = self.graph
        v = g.create_vertex()
        ok_((v,) == tuple(f.vertices(g)))

    def test_edges(self):
        g = self.graph
        v1, v2 = g.create_vertex(), g.create_vertex()
        e = g.create_edge(v1, v2)
        ok_((e,) == tuple(f.edges(g)))

    def test_is_neighbour(self):
        g = self.graph
        v1, v2 = g.create_vertex(), g.create_vertex()
        e = g.create_edge(v1, v2)
        ok_(f.is_neighbour(g, v1, v2))

    def test_neighbours(self):
        g = self.graph
        v1, v2, v3 = g.create_vertex(), g.create_vertex(), g.create_vertex()
        e = g.create_edge(v1, v2)
        ok_(v1 in f.neighbours(g, v2))
        ok_(v2 in f.neighbours(g, v1))
        ok_(v3 not in f.neighbours(g, v1))
        ok_(v3 not in f.neighbours(g, v2))

    def test_is_vertex(self):
        g = self.graph
        ok_(f.is_vertex(g, g.create_vertex()))
        ok_(f.is_vertex(g, g.create_vertex('Pumuckl')))
        ok_(f.is_vertex(g, g.create_vertex(1)))
        ok_(f.is_vertex(g, g.create_vertex(1, XSD.decimal)))
        ok_(not f.is_vertex(g, g.create_edge(g.create_vertex(), g.create_vertex())))

    def test_is_edge(self):
        g = self.graph
        ok_(not f.is_edge(g, g.create_vertex()))
        ok_(not f.is_edge(g, g.create_vertex('Pumuckl')))
        ok_(not f.is_edge(g, g.create_vertex(1)))
        ok_(not f.is_edge(g, g.create_vertex(1, XSD.decimal)))
        ok_(f.is_edge(g, g.create_edge(g.create_vertex(), g.create_vertex())))

    def test_is_literal(self):
        g = self.graph
        ok_(not f.is_literal(g, g.create_vertex()))
        ok_(f.is_literal(g, g.create_vertex('Pumuckl')))
        ok_(f.is_literal(g, g.create_vertex(1)))
        ok_(f.is_literal(g, g.create_vertex(1, XSD.decimal)))
        ok_(not f.is_literal(g, g.create_edge(g.create_vertex(), g.create_vertex())))
