#File: default_templates.py
"""
Provides default templates for style writers.
Used by the default style (default.py).

CITATION TEMPLATE
-----------------

book = '%(year)s. %(title)s.',
article  = '%(year)s. %(title)s. %(journal)s %(volume)s, %(pages)s.',
misc = '%(year)s.  %(title)s.',

`default_type` : str
	provide template for string interpolation (use fields as keys)
	e.g.,  '  %(year)s. %(title)s.'
`name_first` : str
	name template for primary name in citation (see NameFormatter documentation)
`name_other` : str
	name template for remaining names in citation (see NameFormatter documentation)
`name_name_sep` : 2-tuple of str
	first element separates each name from the next,
	second element separates penultimate name from ultimate
`etal` : str
	replacement for name when max_citation_names exceeded (e.g., ', et al.')
`initials` : str
	first letter of first (f), von (v), last (l), jr (j) (e.g., 'f')
`max_citation_names` : int
	maximum number of names to format for a citation definition
`indent_left` : int
	left indent for citation definitions
`citation_sep` : str
	separator between citations (e.g.,  "\n\n")
`names_details_sep` : str
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

__version__ = "$Revision$"
# $Source$

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
techreport  = '(%(year)s) "%(title)s". %(type)s %(number)s. pp. %(institution)s.',
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

