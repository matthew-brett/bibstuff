#! /usr/bin/env python
# File: bibgrammar.py

"""
Provides an EBNF description of the bibtex bibliography format.
The grammar draws largely from
the grammar description in Nelson Beebe's `Lex/Yacc parser`_
and also from
Greg Ward's btOOL_ documentation.

:author: Dylan Schwilk
:contact: http://www.schwilk.org
:author: Alan G Isaac (minor edits)
:copyright: 2006 by Dylan Schwilk
:license: MIT (see `license.txt`_)
:date: 2006-08-03


.. _license.txt: ./license.txt
.. _`Lex/Yacc parser`: http://www.math.utah.edu/~beebe/
.. _btooL: http://www.tug.org/tex-archive/biblio/bibtex/utils/btOOL/
"""
__docformat__ = "restructuredtext en"
__needs__ = '2.4'
__version__ = "1.6"
__author__  =    '''Dylan W. Schwilk'''


###################  IMPORTS  ##################################################
#import from standard library
# (some if  run as main; see below)

#import dependencies
from simpleparse.parser import Parser
from simpleparse.common import numbers, strings, chartypes

#local imports
################################################################################


# EBNF description of a bibtex file
dec = r"""
bibfile              := entry_or_junk*
>entry_or_junk<      := (tb, object) / (tb, junk)
>object<               := entry / macro / preamble / comment_entry
entry                := '@', type , tb,  ( '{' , tb, contents, tb, '}' ) / ( '(' , tb, contents, tb, ')' )
macro                := '@', type, tb,  ( '{' , tb, macro_contents, tb, '}' ) / ( '(' , tb, macro_contents, tb, ')' )
preamble             := '@', type, tb,  ( '{' , tb, preamble_contents, tb, '}' ) / ( '(' , tb, preamble_contents, tb, ')' )
comment_entry        := '@', type, tb, string
>contents<           := key , ',' , fields
>macro_contents<     := fields
>preamble_contents<  := value
type                 := name
key                  := number / name
fields               := tb, field_comma+ , field?
>field_comma<        := field , tb, ','
field                := tb, name, tb, '=' , tb, value
value                := simple_value , (tb,'#', tb, simple_value)*
>simple_value<       := string / number / name
name                 := []-[a-z_A-Z!$&+./:;<>?^`|] , []-[a-z_A-Z0-9!$&+./:;<>?^`|]*
number               :=  [0-9]+
string               := ('{' , braces_string?, '}') / ('"' , quotes_string?, '"')
<braces_string>      := (-[{}"]+ / nested_string)+
<quotes_string>      := (-["{}]+ / nested_string)+
<nested_string>      := ('{' , braces_string, '}') / ('"' , quotes_string, '"')
<junk>               := -[ \t\r\n]+
<tb>                 := (comment / ws)*
<ws>                 := [ \t\n\r]
<comment>            := '%' , -[\n]*, '\n'
"""

## The parsers
parser = Parser(dec,'bibfile')
entry_parser = Parser(dec,'entry')

## or a default parse function
def Parse(src, processor = None) :
    '''Parse the bibtex string in src, process with processor.'''    
    return parser.parse(src,  processor =  processor)


## self-test
if __name__ =="__main__":
	import sys, pprint
	if len(sys.argv) > 1 :
		src = open(sys.argv[1]).read()
		taglist = Parse(src)
		pprint.pprint(taglist)
