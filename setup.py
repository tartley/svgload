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
SvgBatch loads SVG files and tesselates the resulting polygons using GLU
functions to create a pyglet Batch object using indexed arrays of vertices. The
Batch aggregates all paths from an SVG file into a single OpenGL GL_TRIANGLES
primitive for rendering. Each path is also exposed by its 'id' attributes, so
the application could use them for collision detection, for example.

Currently only a subset of SVG is handled - closed polygons, filled with solid
color. These may comprise multiple loops (disjoint areas or holes), but must be
made up from straight line edges. Arc polygon edges and gradient fills are not
currently handled.

Requires pyglet.
'''[1:-1].replace('\n', ' ')

setup(
    name='svgbatch',
    version=__version__,
    description=
      'Loads SVG into pyglet Batch objects of OpenGL GL_TRIANGLE primitives.',
    long_description=long_description,
    url='http://code.google.com/p/svgload/',
    author='Jonathan Hartley',
    author_email='tartley@tartley.com',
    provides=['svgbatch'],
    install_requires=['pyglet'],
    scripts=['demo.py', 'bin\run_tests.bat'],
    packages=['svgbatch'],
)

