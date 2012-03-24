#!/usr/bin/env python

# bibstuff setup script
# Date: 2009-02-13

from os.path import join as pjoin
import glob

from distutils.core import setup
setup(name="bibstuff",
      version="1.0.0",
      description="Bibtex database utilities",
      author="Dylan W. Schwilk and Alan G. Isaac",
      author_email="point@pricklysoft.org",
      url = "http://www.pricklysoft.org/software/bibstuff.html",
      license = "MIT",
      packages = ["bibstuff",
                  "bibstuff.sphinxext",
                  "bibstuff.bibstyles",
                 ],
      package_data = {'bibstuff':
                      [pjoin('data', '*'),
                       pjoin('examples', '*'),
                      ]},
      scripts=glob.glob(pjoin('scripts', '*')))
