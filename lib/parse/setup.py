#! /usr/bin/env python

from __future__ import with_statement

from setuptools import setup

from parse import __version__, __doc__

with open('README.rst', 'w') as f:
    f.write(__doc__)

# perform the setup action
setup(
    name = "parse",
    version = __version__,
    description = "parse() is the opposite of format()",
    long_description = __doc__,
    author = "Richard Jones",
    author_email = "richard@python.org",
    py_modules = ['parse'],
    url = 'https://github.com/r1chardj0n3s/parse',
    classifiers = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: BSD License',
    ],
)

# vim: set filetype=python ts=4 sw=4 et si
