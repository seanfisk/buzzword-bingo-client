#!/usr/bin/env python

# Buzzword Bingo Client distutils setup script

import os
from buzzword_bingo_client import metadata
from distutils.core import setup

# credit: <http://packages.python.org/an_example_pypi_project/setuptools.html>
# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name=metadata.title,
      version=metadata.version,
      author=metadata.authors[0],
      author_email=metadata.emails[0],
      maintainer=metadata.authors[0],
      maintainer_email=metadata.emails[0],
      url=metadata.url,
      description=metadata.description,
      long_description=read('README.rst'),
      download_url=metadata.url,
      classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Environment :: MacOS X :: Cocoa',
            'Environment :: Win32 (MS Windows)',
            'Environment :: X11 Applications :: Qt',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: ISC License (ISCL)',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Topic :: Games/Entertainment :: Board Games'
            ],
      packages=['buzzword_bingo_client'],
      scripts=['scripts/buzzword_bingo']
      )
