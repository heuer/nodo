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
Nodo interfaces.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import absolute_import
try:
    from zope.interface import Interface, Attribute, implements
except ImportError:
    class Interface(object): 
        def __call__(self, default=None):
            return default
    class Attribute(object):
        def __init__(self, descr): pass
    def implements(i): pass
try:
    from zope.component import adapts
except ImportError:
    def adapts(i): pass


class IImmutableGraph(Interface):
    """\
    Represents an immutable `hypergraph <http://en.wikipedia.org/Hypergraph>`_.
    """
    def find_vertex(value, datatype=None):
        """\
        Returns the vertex identifier for the provided value/datatype tuple
        or ``None`` if no such vertex exists.

        `value`
            The literal's value (a string)
        `datatype`
            An IRI (a string) or ``None`` to indicate that the value has the datatype
            ``xsd:string``.
        """

    def find_integer_vertex(value):
        """\
        Returns the vertex identifier for the provided integer `value` or
        ``None`` if no such vertex exists.
        """

    def find_iri_vertex(value):
        """\
        Returns the vertex identifier for the provided IRI `value` or
        ``None`` if no such vertex exists.
        """

    def literal(identifier):
        """\
        Returns a value/datatype tuple for the provided literal vertex identifier
        or ``None`` if the identifier is unknown.

        `identifier`
            A (literal) vertex identifier.
        """

    def value(identifier):
        """\
        Returns the value part of a literal vertex.

        Does the same as::

            lit = graph.literal(identifier)
            value = None if lit is None else lit[0]

        `identifier`
            A (literal) vertex identifier.
        """

    def head(edge):
        """\
        Returns the head (a vertex or an edge) of the provided `edge`.

        `edge`
            An edge identifier.
        """

    def tail(edge):
        """\
        Returns the tail (an iterable of vertices or edges) of an edge.

        `edge`
            An edge identifier.
        """

    def edge_targets(edge):
        """\
        Returns the head and tail of an edge.

        This method is returns a result equivalent to::

            chain([graph.head(edge)], graph.tail(edge))

        `edges`
            Edge identifier.
        """

    def edge_contains(edge, *identifier):
        """\
        Returns if the provided identifiers are contained in the provided
        `edge`.

        This method returns the same result as::

            s = [head(edge)]
            s.extend(tail(edge))
            for ident in identifiers:
                if ident not in s:
                    return False
            return True
                    
        """

    def outgoing_edges(*identifier):
        """\
        Returns an iterable over all outgoing edges of `identifiers`.

        `identifiers`
            An iterable of vertex identifier.
        """

    def ingoing_edges(*identifier):
        """\
        Returns an iterable over all ingoing edges of `identifiers`.

        `identifiers`
            An iterable of vertex or edge identifiers.
        """

    def neighbours(*identifier):
        """\
        Returns an iterable over all vertices connected to `identifiers`.

        `identifiers`
            An iterable of vertex or edge identifiers.
        """

    def is_neighbour(a, b):
        """\
        Returns if the vertices `a` and `b` are connected or if the edges
        `a` and `b` have a common vertex.
        """

    def predecessors(*identifier):
        """\
        Returns an iterable of vertices which point to the provided
        `identifiers`.

        `identifiers`
            An iterable of vertex identifiers.
        """

    def successors(*identifier):
        """\
        Returns an iterable of vertices to which the provided `identifiers`
        point to.

        `identifiers`
            An iterable of vertex identifiers.
        """

    def kind(identifier):
        """\
        Returns the kind of identifier.

        The kind is either `constants.KIND_VERTEX`, `constants.KIND_EDGE`,
        or `constants.KIND_LITERAL`. If the identifier is unknown, this
        method returns `constants.KIND_UNKNOWN`.
        """

    def is_edge(identifier):
        """\
        Returns if the `identifier` represents an edge.

        `identifier`
            The identifier to check.
        """

    def is_vertex(identifier):
        """\
        Returns if the `identifier` represents a vertex (or a literal vertex).

        `identifier`
            The identifier to check.
        """

    def is_literal(identifier):
        """\
        Returns if the `identifier` represents a literal.

        `identifier`
            The identifier to check.
        """

    def rank():
        """\
        Returns the maximum cardinality of any of the edges.
        """

    def card(edge):
        """\
        Returns the cardinality of the provided edge.

        `edge`
            An edge identifier.
        """

    def degree(identifier):
        """\
        Returns the number of ingoing edges.

        `identifier`
            A vertex or edge identifier.
        """

    def is_uniform(k=None):
        """\
        Returns if the graph is uniform: All edges have the same cardinality `k`.

        `k`
            Optional cardinality to test against.
        """

    def __contains__(identifier):
        """\
        Returns if the `identifier` is contained in this graph.

        `identifier`
            A vertex or edge identifier.
        """

    def __iter__():
        """\
        Returns an iterable over all vertices.
        """

    def __len__():
        """\
        Returns the number of vertices.
        """

    identifier = Attribute("""\
Returns the unique (within a `IImmutableGraphspace`) graph identifier.""")
    vertices = Attribute("""Returns an iterable over all vertix identifiers""")
    edges = Attribute("""Returns an iterable over all edge identifiers""")


class IGraph(IImmutableGraph):
    """\
    Extends the `ImmutableGraph` about methods to create vertices and edges.
    """
    def create_vertex(value=None, datatype=None):
        """\
        Creates a vertex and returns the identifier of the vertex.

        If `value` and `datatype` is ``None``, a new vertex will be created.
        If a `value` (and optionally a datatype) is provided, an existing vertex with the
        provided `value` (and datatype) is returned or a vertex with the provided arguments
        will be created.

        `value`
            An optional string value
            If `datatype` is ``None``, xsd:string is assumed for the datatype.
        `datatype`
            An optional IRI indicating the datatype of the `value`.
        """

    def create_iri_vertex(value):
        """\
        Creates an IRI vertex and returns the identifier of the vertex.

        Shortcut for::

            graph.create_literal_vertex(value, xsd:anyURI)

        `value`
            The IRI value (a string).
        """

    def create_integer_vertex(value):
        """\
        Creates an integer vertex and returns the identifier of the vertex.

        Shortcut for::

            graph.create_literal_vertex(value, xsd:integer)

        `value`
            The integer value.
        """

    def create_edge(head, *tail):
        """\
        Creates an edge from `head` to the provided `tail` and returns
        the edge identifier.

        `head`
            A vertex identifier.
        `tail`
            An iterable of targets.
        """

    def add_tail(edge, *identifiers):
        """\
        Adds the provided `identifiers` to the `edge`'s tail and returns
        the edge identifier.

        .. note::

            If the backend supports immutable edges only, a new edge may be
            created which replaces the provided edge.


        `edge`
            The edge to add the identifiers to.
        """

    def remove_tail(edge, *identifiers):
        """\
        Removes the provided `identifiers` from the `edge`'s tail and returns
        the edge identifier.

        .. note::

            If the backend supports immutable edges only, a new edge may be
            created which replaces the provided edge.

        .. note::

            If the removal of the provided identifiers result into an empty
            tail, a ``ValueError`` is raised.

        `edge`
            The edge to add the identifiers to.
        """

    def delete_vertex(identifier):
        """\
        Deletes a vertex.

        `identifier`
            A vertex identifier.
        """

    def delete_edge(identifier):
        """\
        Deletes an edge.

        `identifier`
            An edge identifier.
        """

    def delete(identifier):
        """\
        Deletes a vertex or an edge.

        `identifier`
            A vertex or an edge identifier.
        """

    def __delitem__(identifier):
        """\
        Deletes a vertex or an edge.
        """

class IConnection(Interface):
    """\
    Represents a connection to a `IImmutableGraphspace` or `IGraphspace`.
    """
    def commit():
        """\
        This method commits the current transaction.
        """

    def rollback():
        """\
        This method rolls back any changes to the database since the last call
        to `commit()`.
        """

    def close():
        """\
        This closes the connection. Note that this does not automatically call
        `commit()`.

        If you just close your connection without calling `commit()` first,
        your changes will be lost!
        """

    def is_readonly():
        """\
        Returns if this connection represents an immutable connection.
        """

    def get(graph, default=None):
        """\
        Returns the provided `graph` or the `default`.

        `graph`
            A graph identifier
        `default`
            The default return value (by default ``None``)
        """

    def __getitem__(graph):
        """\
        Returns the provided `graph`.

        If the graph does not exist, a KeyError is raised.
        """

    def __contains__(graph):
        """\
        Returns if `graph` is part of this space.

        `graph`
            A graph identifier.
        """

    def create_graph(identifier=None):
        """\
        Creates a graph and returns a `IGraph` instance.

        `identifier`
            A unique identifier for the graph. If the identifier is ``None`` (default),
            a unique identifier will be generated.
        """

    def delete_graph(identifier):
        """\

        """

    def __delitem__(identifier):
        """\

        """

    identifiers = Attribute("""Returns an iterable of identifiers for available graphs""")


class IGraphHandler(Interface):
    """\

    """
    def start():
        """\

        """

    def end():
        """\

        """

    def start_edge():
        """\

        """

    def end_edge():
        """\

        """


