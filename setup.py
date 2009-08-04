#!/usr/bin/env python

from distutils.core import setup

from svgbatch import __version__

# prevent setuptools including all files from subversion in sdist
# from setuptools.command import sdist
# del sdist.finders[:]

# prevent setuptools caching file manifest from previous runs
# from os import remove
# from os.path import join
# remove(join('svgbatch.egg-info', 'SOURCES.txt'))


long_description = '''
The polygons from the SVG file are tesselated using GLU functions, and used to
create a pyglet Batch object of indexed vertex arrays. The Batch will aggregate
all paths from an SVG file into a single OpenGL GL_TRIANGLES primitive for
rendering. Each path is also exposed in its untessellated form, indexed by 'id'
attribute, so the application could use them for collision detection, for
example.

Currently only a subset of SVG is handled - closed polygons, filled with solid
color. These may comprise multiple loops (disjoint areas or holes), but must be
made up from straight line edges. Arc polygon edges, gradient fills and other
SVG entities (such as rectangles or text) are not currently handled.

Requires pyglet.
'''[1:-1].replace('\n', ' ')

setup(
    name='svgbatch',
    version=__version__,
    description=
      'Loads SVG files into pyglet Batch objects for OpenGL rendering.',
    long_description=long_description,
    url='http://code.google.com/p/svgload/',
    author='Jonathan Hartley',
    author_email='tartley@tartley.com',
    provides=['svgbatch'],
    scripts=['demo.py', 'bin\run_tests.bat'],
    packages=['svgbatch'],
)

