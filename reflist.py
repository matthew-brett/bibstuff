#! /usr/bin/env python
# File: reflist.py
"""
Script to produces a list of reference keys from a .bbl file created by bibtex.

The output is useful for then feeding to bibsearch.py to create a
custom database for a particular latex document. This avoids the
necessity of sending a huge bibtex database along with a manuscript
when submitting to a journal.

:author: Dylan Schwilk
:contact:http://www.pricklysoft.org
:author: Alan G Isaac (small changes)
:copyright: 2006 by Dylan Schwilk
:license: MIT (see `license.txt`_)
:date: 2006-08-01

.. _license.txt: ./license.txt
"""

__docformat__ = "restructuredtext en"
__authors__  =    ["Dylan W. Schwilk", "Alan G. Isaac"]
__needs__ = '2.4'

__version__ =    '$Revision$'
# $Source$

###################  IMPORTS  ##################################################
#import from standard library
import sys
import logging
logging.basicConfig(format='\n%(levelname)s:\n%(message)s\n')
reflist_logger = logging.getLogger('bibstuff_logger')
################################################################################


if __name__ == '__main__':
	"""Command-line tool"""
        
	from optparse import OptionParser
	
	usage = """usage: %prog FILE
	
	For example, to create a stripped down database
	for a particular latex document:
	python %prog FILE.bbl | python bibsearch.py DB.bib -l > NEW_DB.bib
	"""

	parser = OptionParser(usage=usage, version ="%prog " + __version__)
	parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False,
					  help="Print INFO messages to stdout, default=%default")
	parser.add_option("-V", "--very_verbose", action="store_true", dest="very_verbose", default=False,
					  help="Print DEBUG messages to stdout, default=%default")
	   
	(options, args) = parser.parse_args()
	if options.verbose:
		reflist_logger.setLevel(logging.INFO)
	if options.very_verbose:
		reflist_logger.setLevel(logging.DEBUG)
	reflist_logger.info("Script running.\nargs=%s"%(args))

	try :
		src = open(args[0]).read()
	except :
		src = sys.stdin.read()

	items = src.split('\n\n')
	for i in items :
		i = i.strip()
		if i[:8] == '\\bibitem':
			s = i.find(']')
			e = i.find('}', s)
			print i[s+2:e]

