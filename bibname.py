#!usr/bin/python
#File: bibname.py
"""
Parses bibtex-formatted author/editor names lists and provides
formatting functions (often via bibstyles/shared.NamesFormatter).

:author: Dylan W. Schwilk
:contact: http://www.pricklysoft.org
:author: Alan G. Isaac
:contact: http://www.american.edu/cas/econ/faculty/isaac/isaac1.htm
:copyright: 2006 by Dylan Schwilk and Alan G Isaac
:license: MIT (see `license.txt`_)
:date: $Date: 2006/08/29 15:48:05 $

:TODO: Change the EBNF description to allow for strings within a name.
       For example, the name {\AA}s currently fails.  The current version
       (2006-08-30) allows strings if they include a whole name part, so
       '{{\AA}s}' works, but only in vl,f format (this second issue is a
       problem with BibName.parse_raw_names_parts and populating the
       names_groups structure.

       Partially fixed by dschwilk: (but a bit of a hack) Was not
       working on capitalized vons parts such as 'Von der Burg, S.'
       This capitalized von part was not being captured into the
       names_groups structure, so I did an extra check for it.  This
       could still be cleaned up.

.. _license.txt: ./license.txt
"""
__docformat__ = "restructuredtext en"
__authors__  =    ["Dylan W. Schwilk", "Alan G. Isaac"]
__version__ =    '1.9'
__needs__ = '2.4'


################ IMPORTS #############################
# import from standard library
from itertools import groupby
import logging
logging.basicConfig(format='\n%(levelname)s:\n%(message)s\n')
bibname_logger = logging.getLogger('bibstuff_logger')

# import dependencies
import simpleparse

# BibStuff imports
import bibstyles, bibfile, bibgrammar
######################################################


################## Global Variables ##################

# The EBNF description of a bibtex name list (such as author names)

ebnf_bibname = r"""
name            := ( (sp, _and_, sp) / part / comma / break )+
_and_            := 'and' / 'AND' / 'And'
part           :=   capitalized /  two_part / lowercase / string
comma                := ','
<string>              := ('{' , braces_string, '}') 
<capitalized>         := [A-Z]  , [a-zA-Z~'-]* 
<lowercase>          := [a-z~'-]+ 
<two_part>           := [a-zA-Z~'-], [A-Z~'-]+ , [a-zA-Z~'-]+
<braces_string>      := (-[{}]+ / nested_string)+
<nested_string>      := ('{' , braces_string, '}')
<break>             := [ \t\n\r.]
<sp>             := [ \t\n\r]
"""

# old description
##ebnf_bibname = r"""
##name            := ( (tb, _and_) / (tb, part) / (tb , string) / (tb, comma) )+
##_and_            := 'and'
##part           :=   capitalized /  two_part / lowercase
##comma                := ','
##string              := ('{' , braces_string, '}') 
##<capitalized>         := [A-Z] , [a-zA-Z~'-]*
##<lowercase>          := [a-z~'-]+ 
##<two_part>           := [a-zA-Z~'-], [A-Z~'-]+ , [a-zA-Z~'-]+
##<braces_string>      := (-[{}]+ / nested_string)+
##<nested_string>      := ('{' , braces_string, '}')
##<tb>             := [ \t\n\r.]*
##"""

bibname_parser = simpleparse.parser.Parser(ebnf_bibname, 'name')

######################################################

# ----------- Public Functions -----------------#


#KEEP! and keep as separate bibname function
# dschwilk 2006-09-13: can we delete this now?
# still used by bibname.py and bibstyle.py (and tf addrefs.py)
def format_names_parts(names_parts, name_name_sep = (', ',' and '), formatter=None, template = 'v |l,| j,| f{. }.' , initials = True):
	"""Format a list of names:  `format_name_parts` is applied to each name in list
	according to `template`.
	
	Provides the default names formatting. The names are separated according to the tuple
	name_name_sep.  The first string in name_name_sep separates the first through
	penultimate name and the second string separates the penultimate name from
	the last name."""
	bibname_logger.info("bibname.format_name_parts: usually shd use a NamesFormatter instead!")
	if not formatter:
		formatter = bibstyles.shared.NameFormatter(template,initials=initials)
	ls = [format_name_parts(name, formatter=formatter) for name in names_parts]
	if len(ls) > 1 :
		result = name_name_sep[0].join(ls[:-1]) + name_name_sep[1] + ls[-1]
	else :
		result = ls[0]
	return result


# ----------------------------------------------------------
# BibName
# -------
# Parser processor for bibtex names
# ----------------------------------------------------------
class BibName( simpleparse.dispatchprocessor.DispatchProcessor ):
	"""Processes a bibtex names entry (author, editor, etc) and
	stores the resulting raw_names_parts.
	
	:note: a BibName object should be bibstyle independent.
	"""
	def __init__(self,raw_name=None,from_field=None) :  #:note: 2006-07-25 add initialization based on raw name
		"""initialize a BibName instance
		
		:Parameters:
		  `raw_name`: str
		    the raw name (e.g., unparsed author field of a BibEntry instance)
		  `from_field`: str
		    the entry field for the raw name
		:note: 2006-08-02 add `from_field` argument (set by `BibEntry.make_names`)
		"""
		self.from_field = from_field
		self.raw_names_parts = [[[]]] # list of names, a name is a list of up to three lists
		self.names_parts = [] # list of names, a name is a tuple of four lists (f,v,l,j)
		self.names_dicts = []  #:TODO: switch to use of names_dicts  (begun)
		if raw_name:
			bibname_parser.parse(raw_name,  processor =  self)	  
 
	###############  PRODUCTION FUNCTIONS  #######################
	# define function for each production!

	def _and_(self, (tag,start,stop,subtags), buffer ):
		if self.raw_names_parts[-1] :
			self.raw_names_parts.append([[]])
		
##	def string(self, (tag,start,stop,subtags), buffer ):
##		"""Return a string, stripping leading and trailing markers"""
##		self.raw_names_parts[-1][-1].append( buffer[start+1:stop-1])

	def part(self, (tag,start,stop,subtags), buffer ):
		"""Append string to current name-part list."""
		self.raw_names_parts[-1][-1].append( buffer[start:stop])
		
	def comma(self, (tag,start,stop,subtags), buffer ):
		# start new empty list for same name, new piece
		self.raw_names_parts[-1].append([])


	##############  HELPER FUNCTIONS  ######################

	def get_names_parts(self) :  #:note: renamed
		"""
		Return a list of name tuples,
		one tuple per name,
		having the form: (first , von, last, jr).
		"""
		if not self.names_parts:
			self.parse_raw_names_parts()
		return self.names_parts

	def get_names_dicts(self) :  #:note: renamed
		"""
		Return a list of name dicts,
		one dict per name,
		having the fields: first , von, last, jr.
		"""
		if not self.names_dicts:
			self.parse_raw_names_parts()
		return self.names_dicts

	def parse_raw_names_parts(self):
		"""Return None;
		create list of names_parts tuples in form: first , von, last, jr -> self.names_parts;
		create list of names_dicts dict with keys: first , von, last, jr -> self.names_dicts.

		For each name, take a list of raw_name parts and classify the parts by the length of the list.
		Parts are classified as first, von, last, jr.
		The 'von' part is determined by lack of capitalization.

                :todo:
                    the names_groups structure is not being populated
                    correctly for all types of names.  This may need a
                    more detailed function than the nice on-liner
                    used below.
		"""
		tuple_list = []
		for n in self.raw_names_parts :
			f,v,l,j = [],[],[],[]
			try :
                                # DS 2006-08-30: this does not work on all names, it chokes on braces strings, for example
				name_groups = [list(b) for a,b in groupby(n[0],lambda x: x[0].isupper())]
				if len(n) == 1 :  # implies parts are fvl
					if len(name_groups) == 1: #-> no v part
						fl = name_groups[0]
						f,l = fl[:-1], fl[-1:]
					elif len(name_groups) == 3:
						f,v,l = name_groups
					else:
						bibname_logger.warn("Unrecognized name format for "+str(n))

				else:  # vl,f or vl,j,f 
					f = n[-1]  
					if len(name_groups) == 1: #-> no v part
						l = n[0]
					elif len(name_groups) == 2:  # von parts captured correctly
                                                v,l = name_groups
                                        else : # von parts in upper-level list (multi-part last names) --
                                                # should be caught by
                                                # parser, but this hack for now
                                                for g in name_groups[0:-1] : v.extend(g)
                                                l = name_groups[-1]
					if len(n) == 3:
						j = n[1]

				if f == []:
					if l[0] == 'others':
						bibname_logger.debug("found 'others' in "+str(n))
					else:   # changed to info below, many types of names lack a first name
						bibname_logger.info("missing first name for "+str(n))
                                                
			except:
				bibname_logger.error("Unrecognized name format for "+str(n))
 				raise 
			tuple_list.append((f,v,l,j))
		#:TODO: ? move entirely to use of names_dicts ?
		#put parts in name dict, with empty string for missing part
		self.names_dicts = [ dict(first=f,von=v,last=l,jr=j) for (f,v,l,j) in tuple_list]
		self.names_parts = tuple_list

	#ai: method to get last names, which is needed by bibstyle.py and by some style sortkeys
	def get_last_names(self):
		"""Return list of strings, where each string is a last name.
		
		:TODO: graceful handling of missing names parts
		"""
		if not self.names_dicts:
			self.parse_raw_names_parts() #this will make the names_dicts
		result = [' '.join(name_dict['last']) for name_dict in self.names_dicts]
		#bibname_logger.debug("BibName.get_last_names result: "+str(result))
		return result

	#format a BibName object into a string useful for citations
	#ai: called by the BibEntry class in bibfile.py when entry formatting is requested
	def format(self, names_formatter):
		return names_formatter.format_names(self)


def getNames(src) :
	"""Returns list of name tuples.
	`src` is a string is in bibtex name format.
	"""
	try :
		p = BibName(src)  #:note: 2006-07-25 allow initialization w src
		#bibname_parser.parse(src,  processor =  p)	  
		return p.get_names_parts()  #:note: 2006-07-25 renamed
	except :
		bibname_logger.error('Error in name %s' % src)
		raise

# command-line version
if __name__ =="__main__":
	import sys
	from optparse import OptionParser
	
	usage = "usage: %prog [options] filenames"

	parser = OptionParser(usage=usage, version ="%prog " + __version__)
	parser.add_option("-t", "--template", action="store", type="string", \
					  dest="template", default = 'f{.}. |v |l| jr', help="Name format template")
	parser.add_option("-i", "--initials", action="store_true", dest="initials", \
					  default = True, help="Initialize first names")
	parser.add_option("-I", "--no-initials", action="store_false", dest="initials", \
					  default = True, help="do not initialize first names")
	parser.add_option("-l", "--last-names", action="store_true", dest="last_names", \
					  default = False, help="Print last names only.")
	parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False,
					  help="Print INFO messages to stdout, default=%default")

	# get options
	(options, args) = parser.parse_args()
	if options.verbose:
		bibname_logger.setLevel(logging.INFO)
	if options.last_names:
		options.template = 'l'

	if len(args) > 0 :
		try :
		   rfile = lambda f : f.read()
		   src = '\n'.join(map(rfile , map(open,args)))
		except:
			print 'Error in filelist'
	else :
		src = sys.stdin.read()

	bfile = bibfile.BibFile()
	bibgrammar.Parse(src, bfile)

        if options.initials :
                initials = 'f'  # only first names.  Does any style ever use initials for anything else?
        else :
                initials = ''

	names_formatter = bibstyles.shared.NamesFormatter(template_list=[options.template]*2,initials=initials)
	for entry in bfile.entries:
		print
		print entry.format_names(names_formatter)

