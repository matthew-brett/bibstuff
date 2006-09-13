#! /usr/bin/env python

# bibstuff setup script
# Date: 2006-09-13


from distutils.core import setup
setup(name="bibstuff",
      version="0.7.3",  
      description="Bibtex database utilities",
      author="Dylan W. Schwilk and Alan G. Isaac",
      author_email="point@pricklysoft.org",
      url = "http://www.pricklysoft.org/software/bibstuff.html",
      license = "MIT",
      packages = ["bibstyles"],
      py_modules=["bibgrammar", "bibfile", "bibname", "ebnf_sp.py"],
      scripts=["bibsearch.py", "biblabel.py", "bib4txt.py", "jabbrev.py", "reflist.py", "add2bib.py"] )

 
