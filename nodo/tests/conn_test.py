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
Abstract connection tests.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from nose.tools import ok_, eq_


class AbstractConnectionTest(object):

    def setUp(self):
        self.ident = 'pumuckl'
        self.conn = self.get_connection()

    def tearDown(self):
        self.conn.delete_graph(self.ident)
        self.conn.close()

    def get_connection(self):
        """\
        Returns an connection.
        """
        raise NotImplementedError()

    def test_create_graph(self):
        conn = self.conn
        ident = self.ident
        ok_(ident not in conn)
        ok_(conn.get(ident) is None)
        default = (1,2,3)
        eq_(default, conn.get(ident, default))
        try:
            graph = conn[ident]
            self.fail('Expected KeyError for unknown graph identifier')
        except KeyError:
            pass
        graph = conn.create_graph(ident)
        ok_(graph is not None)
        eq_(ident, graph.identifier)
        ok_(ident in conn)
        eq_(graph, conn.get(ident))
        eq_(graph, conn[ident])

    def test_create_graph_duplicate(self):
        conn = self.conn
        ident = self.ident
        ok_(ident not in conn)
        graph = conn.create_graph(ident)
        ok_(graph is not None)
        try:
            g = conn.create_graph(ident)
            self.fail('Expected a KeyError for attempt to create graph with existing identifier')
        except KeyError:
            pass

