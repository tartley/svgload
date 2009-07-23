#!/usr/bin/env python

from distutils.core import setup


# prevent setuptools including all files from subversion in sdist
# from setuptools.command import sdist
# del sdist.finders[:]


# prevent setuptools caching file manifest from previous runs
# from os import remove
# from os.path import join
# remove(join('svgbatch.egg-info', 'SOURCES.txt'))


long_description = '''
SvgBatch parses a subset of SVG to extract closed, straight-edged paths. Paths
that are filled with a plain color are tessellated using GLU functions, and
added to a pyglet Batch object using indexed vertices. The Batch aggregates all
such paths into a single OpenGL GL_TRIANGLES primitive. Paths are also exposed
by their 'id' attributes (eg. for use as collision detection boundaries.)
'''[1:-1].replace('\n', ' ')

setup(
    name='svgbatch',
    version='0.1.0',
    description=
      'Loads SVG into pyglet Batch objects of OpenGL GL_TRIANGLE primitives.',
    long_description=long_description,
    url='http://code.google.com/p/svgload/',
    author='Jonathan Hartley',
    author_email='tartley@tartley.com',
    provides=['svnbatch'],
    install_requires=['pyglet'],
    scripts=['demo.py'],
    packages=['svgbatch'],
)

