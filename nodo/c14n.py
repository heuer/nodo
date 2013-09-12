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
This module provides canonicalization of literal values.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import absolute_import
import re
from decimal import Decimal, InvalidOperation
from nodo import XSD
from nodo._urlutils import normalize as normalize_url

_TRAILING_ZEROS_PATTERN = re.compile(r'[0-9](0+)$')


def canonicalize(value, datatype):
    """\
    Canonicalizes the `value` according to the provided `datatype`.

    >>> canonicalize('0001', XSD.integer)
    (u'1', u'http://www.w3.org/2001/XMLSchema#integer')
    >>> canonicalize('0001', 'http://psi.example.org/datatype')
    ('0001', 'http://psi.example.org/datatype')
    >>> canonicalize('1', XSD.boolean)
    (u'true', u'http://www.w3.org/2001/XMLSchema#boolean')
    >>> canonicalize('.001', XSD.decimal)
    (u'0.001', u'http://www.w3.org/2001/XMLSchema#decimal')

    `value`
        The value to normalize.
    `datatype`
        The datatype of the value.
    """
    normalizer = _DATATYPE2NORMALIZER.get(datatype)
    if normalizer:
        return normalizer(unicode(value)), datatype
    return value, datatype


def normalize_decimal(val):
    """\
    Returns the canonical representation of a xsd:decimal value.
    
    >>> normalize_decimal('-.03')
    u'-0.03'
    >>> normalize_decimal('+.03')
    u'0.03'
    >>> normalize_decimal('+.0')
    u'0.0'
    >>> normalize_decimal('-.0')
    u'0.0'
    >>> normalize_decimal('0')
    u'0.0'
    >>> normalize_decimal('.0')
    u'0.0'
    >>> normalize_decimal('0.')
    u'0.0'
    >>> normalize_decimal('0001.')
    u'1.0'
    >>> normalize_decimal('0001')
    u'1.0'
    >>> normalize_decimal('-001')
    u'-1.0'
    >>> normalize_decimal('1.00000')
    u'1.0'
    >>> normalize_decimal('123.4')
    u'123.4'
    >>> normalize_decimal('123.400000000')
    u'123.4'
    >>> normalize_decimal('123.000000400000000')
    u'123.0000004'
    >>> normalize_decimal('0000123.4')
    u'123.4'
    >>> normalize_decimal('0000.0')
    u'0.0'
    >>> normalize_decimal('+0000.0')
    u'0.0'
    >>> normalize_decimal('-0000.0')
    u'0.0'
    >>> normalize_decimal('-123.4')
    u'-123.4'
    >>> normalize_decimal(' -123.4    ')
    u'-123.4'
    >>> normalize_decimal('-123.A')
    Traceback (most recent call last):
    ...
    ValueError: Illegal xsd:decimal: "-123.A"
    >>> normalize_decimal('A')
    Traceback (most recent call last):
    ...
    ValueError: Illegal xsd:decimal: "A"
    >>> normalize_decimal('A.b')
    Traceback (most recent call last):
    ...
    ValueError: Illegal xsd:decimal: "A.b"
    """
    try:
        res = unicode(Decimal(val.strip()))
    except InvalidOperation:
        raise ValueError('Illegal xsd:decimal: "%s"' % val)
    dot_idx = res.find(u'.')
    if dot_idx == -1:
        res += u'.0'
    else:
        int_part, frac_part = res.split(u'.')
        m = _TRAILING_ZEROS_PATTERN.search(frac_part)
        if m:
            res = int_part + u'.' + frac_part[:m.start(1)]
    if res == u'-0.0':
        res = u'0.0'
    return res


def normalize_boolean(val):
    """\
    Returns the canonical representation of a xsd:boolean value.
    
    >>> normalize_boolean('0')
    u'false'
    >>> normalize_boolean('1')
    u'true'
    >>> normalize_boolean('true')
    u'true'
    >>> normalize_boolean('    true    ')
    u'true'
    >>> normalize_boolean('false')
    u'false'
    >>> normalize_boolean('')
    Traceback (most recent call last):
    ...
    ValueError: Illegal xsd:boolean: ""
    >>> normalize_boolean('2')
    Traceback (most recent call last):
    ...
    ValueError: Illegal xsd:boolean: "2"
    """
    v = val.strip()
    if v in (u'0', u'false'):
        return u'false'
    if v in (u'1', u'true'):
        return u'true'
    raise ValueError('Illegal xsd:boolean: "%s"' % val)


def normalize_integer(val):
    """\
    Returns the canonical representation of a xsd:integer value.
    
    >>> normalize_integer('-0')
    u'0'
    >>> normalize_integer('00000')
    u'0'
    >>> normalize_integer('+0')
    u'0'
    >>> normalize_integer('-000100')
    u'-100'
    >>> normalize_integer('+000100')
    u'100'
    >>> normalize_integer(' +000100 ')
    u'100'
    >>> normalize_integer('100')
    u'100'
    >>> normalize_integer('')
    Traceback (most recent call last):
    ...
    ValueError: Illegal xsd:integer: ""
    """
    try:
        return unicode(int(val))
    except ValueError:
        raise ValueError('Illegal xsd:integer: "%s"' % val)

_DATATYPE2NORMALIZER = {
    XSD.decimal: normalize_decimal,
    XSD.integer: normalize_integer,
    XSD.boolean: normalize_boolean,
    XSD.anyURI: normalize_url,
}

if __name__ == '__main__':
    import doctest
    doctest.testmod()
