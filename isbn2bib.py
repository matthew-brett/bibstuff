#! /usr/bin/env python
# -*- coding: latin-1 -*-
# File: isbn2bib.py
"""
:requires: pyaws v.0.3+
:requires: free Amazon web services key http://www.amazon.com/gp/browse.html?node=3435361

Installing pyAWS
----------------

You can get a tarball from:http://svn2.assembla.com
If you use SVN, I'll assume you want the latest version.
(Otherwise, get the tagged version rather than the trunk.)

- Decide where you want your pyaws build directory, say in ``mysvn/pyaws``.
- In a command shell, change to the ``mysvn`` directory.
- Issue the command: svn checkout http://svn2.assembla.com/svn/pyaws/trunk/ pyaws
- Change to your new ``pyaws`` directory.
- Use your python to execute: setup.py install

:license: MIT
:contact: alan dot isaac at gmail dot com 
"""
import difflib
from pyaws import ecs
OUTPUT_TYPE = "bibtex"

html_start = """
<html>
<head>
<style type="text/css">
dt.getbook {padding-top:15px; font-weight:bold;}
</style>
</head>
<body>
<dl>
"""

html_end = """
</dl>
</body>
</html>
"""
 
html_item = """
<dt class="getbook">%(title)s</dt>
<dd>
	<img src="%(url_mediumimage)s" />
	<ul>
		<li>ISBN/ASIN: %(isbn)s/%(asin)s</li>
		<li>Author: %(author)s</li>
		<li>Publisher: %(publisher)s</li>
		<li>Publication Year: %(year)s</li>
	</ul>
</dd>
"""

text_item = """
Title: %(title)s
ISBN/ASIN: %(isbn)s/%(asin)s
Author: %(author)s
Publisher: %(publisher)s
Publication Year: %(year)s
"""

#need an AWS key to proceed (see above)
fh = open('data/aws_key.txt','r')
for line in fh:
	line = line.strip()
	if line:
		key = line
fh.close()
try:
	ecs.setLicenseKey(key)
except AWSException:
	print "failed to set key; missing key?"

print key

#unfortunately, addresses not in bookinfo
# hope it's in my list ...
publisher_addresses = dict()
fh = open('data/publisher_addresses.txt','r')
for line in fh:
	if line.startswith('#') or not line.strip():
		break
	info = line.split('|')
	name = info[0].strip()
	address = info[2].strip()
	publisher_addresses[name] = address
fh.close()

def make_entry(isbn):
	"""
	:todo: this is reusing too much add2bib code
	:author: Alan G. Isaac
	:date: 2008-08-31
	"""
	import add2bib, bibfile
	entry = bibfile.BibEntry()
	entry.entry_type = 'book'
	try:
		bkinfo = ecs.ItemLookup(ItemId=isbn, IdType='ISBN',
			SearchIndex="Books", ResponseGroup="Medium")
	except ecs.AWSException:
		print "ItemLookup failed"
		raise
	bkdict = make_bookdict(bkinfo)
	entry.citekey = bkdict['citekey']
	del bkdict['citekey']  #leaving only real field
	#entry.update(bkdict) #TODO: why does this not work?
	for key in bkdict:
		entry[key] = bkdict[key]
	return entry


def make_bookdict(bkinfo):
	from collections import defaultdict
	bd = defaultdict(str)
	try:
		author = bkinfo.Author.strip()
		author_last = author.split()[-1].lower()
	except AttributeError:
		author = "unknown"
		author_last = "unknown"
	try:
		date = bkinfo.PublicationDate.strip().split()[-1]
		year = date.strip().split('-')[0]
	except AttributeError:
		date = "unknown"
		year = "unknown"
	bd['citekey'] = "%s-%s"%(author_last,date)
	bd['author'] = author
	bd['date'] = date
	bd['year'] = year
	bd['title'] = bkinfo.Title
	bd['isbn'] = bkinfo.ISBN
	publisher = bkinfo.Manufacturer.strip() #?att name??
	bd['publisher'] = publisher
	import difflib
	#thanks to Greg for nicer address matching:
	best_pub_matches = difflib.get_close_matches(publisher,publisher_addresses.keys(),1)
	if best_pub_matches:
		bd['address'] = publisher_addresses[best_pub_matches[0]]	   
	return bd


def print_bkinfo(bkinfo):
	bkdict = make_bookdict(bkinfo)
	if OUTPUT_TYPE.lower() == 'html':
		print html_item % bkdict
	elif OUTPUT_TYPE.lower() == 'bibtex':
		print bkinfo2bibtex(bkdict)
	else:
		print text_item%bkdict

if OUTPUT_TYPE.lower() == 'html':
	print html_start


if OUTPUT_TYPE=='html':
	print html_end

#Greg's test ISBNs:
testISBNS = "9780596513986 0310205824 9780596529321 0231071949"

for isbn in testISBNS.split():
	entry = make_entry(isbn)
	print entry

