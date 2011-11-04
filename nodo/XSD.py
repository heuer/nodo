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
#     * Neither the name of the project nor the names of the contributors 
#       may be used to endorse or promote products derived from this 
#       software without specific prior written permission.
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
XML Schema Datatypes Part 2 standard PSIs.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
__all__ = () # Avoid to expose something that pollutes the namespace

class _Namespace(unicode):
    """\
    The namespace class.
    """
    __slots__ = ()
    def __new__(cls, value):
        if value is None:
            raise ValueError()
        if isinstance(value, _Namespace):
            return value
        return unicode.__new__(cls, value)
    
    def __getattr__(self, name):
        return self.__getitem__(name)
    
    def __getitem__(self, key):
        return u'%s%s' % (self, key)


XSD = _Namespace('http://www.w3.org/2001/XMLSchema#')

anyType = XSD.anyType
anySimpleType = XSD.anySimpleType

duration = XSD.duration
dateTime = XSD.dateTime
time = XSD.time
date = XSD.date
gYearMonth = XSD.gYearMonth
gYear = XSD.gYear
gMonthDay = XSD.gMonthDay
gDay = XSD.gDay
gMonth = XSD.gMonth
boolean = XSD.boolean
base64Binary = XSD.base64Binary
hexBinary = XSD.hexBinary
float = XSD.float
decimal = XSD.decimal
double = XSD.double
anyURI = XSD.anyURI
QName = XSD.QName
NOTATION = XSD.NOTATION
string = XSD.string
# Things derived from xs:decimal
integer = XSD.integer
nonPositiveInteger = XSD.nonPositiveInteger
long = XSD.long
nonNegativeInteger = XSD.nonNegativeInteger
negativeInteger = XSD.negativeInteger
int = XSD.int
unsignedLong = XSD.unsignedLong
positiveInteger = XSD.positiveInteger
short = XSD.short
unsignedInt = XSD.unsignedInt
byte = XSD.byte
unsignedShort = XSD.unsignedShort
unsignedByte = XSD.unsignedByte
# Things derived from xs:string
normalizedString = XSD.normalizedString
token = XSD.token
language = XSD.language
Name = XSD.Name
NMTOKEN = XSD.NMTOKEN
NCName = XSD.NCName
NMTOKENS = XSD.NMTOKENS
ID = XSD.ID
IDREF = XSD.IDREF
ENTITY = XSD.ENTITY
IDREFS = XSD.IDREFS
ENTITIES = XSD.ENTITIES

