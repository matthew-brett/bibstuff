#! /usr/bin/env python
# -*- coding: latin-1 -*-
# File: add2bib.py
'''
Add entry/entries to .bib file.
Default format produces citekeys like:
Schwilk+Isaac:2002 and Isaac+Schwilk+etal:2006.
'''
import os
import sys
import shutil
import logging

from bibstuff.bibadd import (bibadd_logger, make_entry, html_format, text_format)


__docformat__ = "restructuredtext en"
__authors__  =    ['Alan G. Isaac']
__version__ =    '0.3.1'
__needs__ = '2.4'


def main():
	"""Command-line tool.
	See bibsearch.py -h for help.
	"""

	output = sys.stdout
	
	from optparse import OptionParser
	
	usage = """
	%prog [options]
	example: %prog -mt article -bo BIB_DATABASE
	"""


	parser = OptionParser(usage=usage, version ="%prog " + __version__)
	parser.add_option("-f", "--format", action="store",
	                  dest="format", default='b',
					  help="set format(s) of output\nb: BibTeX\nh: HTML\nt: text", metavar="FORMAT")
	parser.add_option("-m", "--more_fields", action="store_true",
					  dest="more_fields", default = False, help="input less common fields")
	parser.add_option("-M", "--MORE_FIELDS", action="store_true",
					  dest="MORE_FIELDS", default = False, help="input all relevant fields")
	parser.add_option("-v", "--verbose", action="store_true",
	                  dest="verbose", default=False,
					  help="Print INFO messages to stdout, default=%default")
	parser.add_option("-V", "--very_verbose", action="store_true",
	                  dest="very_verbose", default=False,
					  help="Print DEBUG messages to stdout, default=%default")
	parser.add_option("-t", "--type", action="store",
	                  dest="entry_type", default='',
					  help="set type of entry", metavar="ENTRYTYPE")
	parser.add_option("-o", "--outfile", action="store", type="string", dest="outfile",
					  help="Write formatted references to FILE", metavar="FILE")
	parser.add_option("-n", "--nuke", action="store_true", dest="overwrite", default=False,
					  help="CAUTION! silently overwrite outfile, default=%default")
	parser.add_option("-b", "--backup", action="store_true", dest="backup", default=False,
					  help="backup FILE to FILE.bak, default=%default")

	"""
	#TODO:
	parser.add_option("-I", "--ISBN", action="store", dest="ISBN", default=False,
					  help="use pyaws to add one entry by ISBN, default=%default")
	parser.add_option("-m", "--maxnames", action="store", type="int",
					  dest="maxnames",  default = 2, help="Max names to add to key")
	parser.add_option("-e", "--etal", action="store", type="string", \
					  dest="etal",  default = 'etal',help="What to add after max names")
	parser.add_option("-i", "--infile", action="store", type="string", dest="infile",
					  help="Parse FILE for citation references.", metavar="FILE")
	parser.add_option("-s", "--stylefile", action="store", dest="stylefile", default="default.py",
					  help="Specify user-chosen style file",metavar="FILE")
	"""

	# get options
	(options, args) = parser.parse_args()
	if options.verbose:
		bibadd_logger.setLevel(logging.INFO)
	if options.very_verbose:
		bibadd_logger.setLevel(logging.DEBUG)
	bibadd_logger.info("Script running.\nargs=%s"%(args))

	'''
	#TODO: error check cite keys, insert (v. append), sort
	# get database as text from .bib file(s) or stdin
	if len(args) > 0 :
		try :
		   src = ''.join(open(f).read() for f in args)
		except:
			print 'Error in filelist'
	else :
		src = sys.stdin.read()

	 
	bibfile_name = args[-1]
	if (os.path.splitext(bibfile_name)[-1]).lower() != ".bib":
		bib4txt_logger.warning(bibfile_name + " does not appear to be a .bib file")
	try :
		bibfile_as_string = open(bibfile_name,'r').read()
	except :
		print "Database file not found."
		sys.exit(1)

	# read input file (default: stdin)
	if options.infile:
		try:
			input = open(options.infile,'r')
		except:
			print "Cannot open: "+options.infile
			sys.exit(1)

	# create object to store parsed .bib file
	bibfile_processor = bibfile.BibFile()
	#store parsed .bib file in the bibfile_processor
	#  TODO: allow multiple .bib files
	bibgrammar.Parse(bibfile_as_string, bibfile_processor)

	bfile = bibfile.BibFile()
	bibgrammar.Parse(src, bfile)
	used_citekeys = [] # stores created keys
	'''

	entry = make_entry(options.entry_type, options.more_fields, options.MORE_FIELDS)

	# open output file for writing (default: stdout)
	if options.outfile:
		if options.backup and os.path.exists(options.outfile):
			shutil.copyfile(options.outfile, options.outfile+".bak")
		if options.overwrite or not os.path.exists(options.outfile):
			output = open(options.outfile,'w')
		else:
			bibadd_logger.info("Appending to %s.\n(Use -n option to nuke (overwrite) the old output file.)"
			                     %options.outfile)
			output = open(options.outfile,'a')
	output.write(str(entry))
	#print entry
	if 'h' in options.format:
		output.write( html_format(entry) )
	if 't' in options.format:
		output.write( text_format(entry) )
	output.close()

if __name__ == '__main__':
	main()
