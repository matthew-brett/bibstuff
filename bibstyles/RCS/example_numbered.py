head	1.3;
access;
symbols;
locks; strict;
comment	@# @;


1.3
date	2006.08.31.21.44.29;	author schwilk;	state Exp;
branches;
next	1.2;

1.2
date	2006.08.03.20.05.14;	author schwilk;	state Exp;
branches;
next	1.1;

1.1
date	2006.08.03.19.58.47;	author schwilk;	state Exp;
branches;
next	;


desc
@@


1.3
log
@Alan's changes.
@
text
@#File: example_numbered.py
"""
Provides an examle of how to easily modify an existing style:
Just import everything from that style, and then override
what you wish to change.  In this case, we import from
default.py, the default style.

This style changes to numbered citation references and citations.
Citation references are numbered like this: (1,2).
Citations are numbered like this:

	1. First Citation Definition
	2. Second Citation Definition

The numbers reflect the order cited (the 'citation_rank').


:author: Alan G Isaac
:contact: http://www.american.edu/cas/econ/faculty/isaac/isaac1.htm
:copyright: 2006 by Alan G Isaac
:license: MIT (see `license.txt`_)
:date: 2006-08-01

.. _license.txt: ./license.txt
"""
__docformat__ = "restructuredtext en"
__author__  =   "Alan G. Isaac"
__version__ = "$Revision 0.5 $"
__needs__ = '2.4'


# import everything from a useful style
from default import *

#####################################################################
############  Override the style choices  ###########################
#####################################################################


######## ADJUST CITATION TEMPLATE FOR NEW STYLE  ###########
CITATION_TEMPLATE.update(dict(
indent_left=0,
name_first = 'f{. }. |v |l|, j',
name_other = 'f{. }. |v |l|, j',
initials = 'f',
name_name_sep = (', ',' and '),
))

# Redefine the CitationManager class, even if "unchanged".
# (This is necessary if you want to change any of the global formatting functions,
#  and usually you change 'format_inline_cite')
class CitationManager(shared.CitationManager):

	################### CITEREF FORMATTING #########################
	def format_inline_cite(self, cite_key_list):
		entry_list = self.find_entries(cite_key_list,discard=False)
		all_keys = self.citeref_processor.all_citekeys
		return format_inline_cite(entry_list,cite_key_list,all_keys)

	################### CITATION FORMATTING ########################
	def get_citation_label(self,entry,template=None):
		return ("%d."%self.get_citation_rank(entry)).ljust(5)

	def sortkey(self,bibentry):
		return self.get_citation_rank(entry)



def format_inline_cite(entries, keys, all_keys) :
	formatted_list = []
	assert(len(entries)==len(keys))
	for i in range(len(entries)):
		if not entries[i]:
			formatted_list.append(keys[i]) #keys appear for missing entries
		else:
			formatted_list.append('%d'%(all_keys.index(keys[i])+1))
	return '(' + ", ".join(formatted_list)+')'

@


1.2
log
@*** empty log message ***
@
text
@a25 1

d28 1
a28 1
__version__ = "$Revision $"
d40 8
a47 1
################### CITEREF FORMATTING ##############################
d49 4
a52 4
# Redefine the CiteRefFormatter class, even if "unchanged".  (This is
# necessary if you want to change any of the global formatting
# functions, and usually you change 'format_inline_cite')
class CiteRefFormatter( shared.CiteRefProcessor ):
d54 4
a57 2
	def format_inline_cite(self, entry_list, cite_key_list):
		all_keys = self.all_cite_keys
d60 8
d74 1
a74 1
			formatted_list.append(keys[i])
a77 19




################### CITATION FORMATTING ##############################
CITATION_TEMPLATE.update(dict(
indent_left=0,
name_formats = ['f |v |l|, j'],
initials = True,
name_name_sep = ('. ','. '),
))

class CitationManager(shared.CitationManager):

	def get_citation_label(self,entry,template=None):
		return ("%d."%self.get_citation_rank(entry)).ljust(5)

	def sortkey(self,bibentry):
		return self.get_citation_rank(entry)
@


1.1
log
@Initial revision
@
text
@d41 1
a41 1
################### CITEREF FORMATTING ##################################
d43 3
a45 3
# Redefine the CiteRefFormatter class, even if "unchanged".
# (This is necessary if you want to change any of the global formatting functions,
#  and usually you change 'format_inline_cite')
d66 1
a66 1
################### CITATION FORMATTING ##################################
@
