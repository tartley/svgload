#!/usr/bin/env python

from distutils.core import setup
from os.path import dirname, join

from svgbatch import __version__

readme = join(dirname(__file__), 'docs', 'README.rst')
long_description = open(readme).read()

setup(
    name='svgbatch',
    version=__version__,
    description=
      'Loads SVG files into pyglet Batch objects for OpenGL rendering.',
    long_description=long_description,
    url='http://code.google.com/p/svgload/',
    license='BSD',
    author='Jonathan Hartley',
    author_email='tartley@tartley.com',
    provides=['svgbatch'],
    packages=['svgbatch', 'svgbatch.tests', 'svgbatch.mock'],
)

