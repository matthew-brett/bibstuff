head	1.3;
access;
symbols;
locks; strict;
comment	@# @;


1.3
date	2006.08.31.21.44.03;	author schwilk;	state Exp;
branches;
next	1.2;

1.2
date	2006.08.03.19.58.08;	author schwilk;	state Exp;
branches;
next	1.1;

1.1
date	2006.08.03.19.57.24;	author schwilk;	state Exp;
branches;
next	;


desc
@@


1.3
log
@Alan's changes.
@
text
@#File: default_templates.py
"""
Provides default templates for style writers.
Used by the default style (default.py).

CITATION TEMPLATE
-----------------

book = '%(year)s. %(title)s.',
article  = '%(year)s. %(title)s. %(journal)s %(volume)s, %(pages)s.',
misc = '%(year)s.  %(title)s.',
`default_type`: str
	provide template for string interpolation (use fields as keys)
	e.g.,  '  %(year)s. %(title)s.'
`name_first`: str
	name template for primary name in citation (see NameFormatter documentation)
`name_other`: str
	name template for remaining names in citation (see NameFormatter documentation)
`name_name_sep`: 2-tuple of str
	first element separates each name from the next,
	second element separates penultimate name from ultimate
`etal`: str
	replacement for name when max_citation_names exceeded (e.g., ', et al.')
`initials`: str
	first letter of first (f), von (v), last (l), jr (j) (e.g., 'f')
`max_citation_names`: int
	maximum number of names to format for a citation definition
`indent_left`: int
	left indent for citation definitions
`citation_sep`: str
	separator between citations (e.g.,  "\n\n")
`names_details_sep`: str
	separator between the names and the details in a citation definition (e.g., '. ')

:author: Alan G Isaac
:contact: http://www.american.edu/cas/econ/faculty/isaac/isaac1.htm
:copyright: 2006 by Alan G Isaac
:license: MIT (see `license.txt`_)
:date: 2006-08-19

.. _license.txt: ./license.txt
"""
__docformat__ = "restructuredtext en"
__author__  =   "Alan G. Isaac"
__version__ = "1.1"

DEFAULT_CITEREF_TEMPLATE = dict(
max_cite_names = 2,
citeref_sep = ", ",
)

"""
initials
	string containing none, any, or all of f,v,l,j
"""

DEFAULT_CITATION_TEMPLATE = dict(
book = '%(year)s. %(title)s.',
article  = '%(year)s. %(title)s. %(journal)s %(volume)s, %(pages)s.',
misc = '%(year)s.  %(title)s.',
default_type = '  %(year)s. %(title)s.',
name_first = 'v |l,| j,| f',
name_other = 'f |v |l|, j',
name_name_sep = (', ',', and '),
etal = ', et al.',
initials = '',
max_citation_names = 3,
indent_left = 3,
citation_sep = "\n\n",
names_details_sep = '. ',
)

@


1.2
log
@*** empty log message ***
@
text
@d6 29
d39 1
a39 1
:date: 2006-08-01
a42 1

d45 1
a45 1
__version__ = "$Revision 1$"
d52 5
d63 1
a63 2
#name_other = 'v |l,| j,| f',
name_other = 'f |v |l |, j',
d66 2
a67 2
initials = False,
max_citation_names = 2,
@


1.1
log
@Initial revision
@
text
@d2 1
a2 1
'''
d13 2
a14 1
'''
d17 1
a17 1
__version__ = 0.5
@
