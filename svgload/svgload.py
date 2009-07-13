import xml.dom.minidom

from pyglet.graphics import Batch

from path import Path
from tesselate import tesselate


def parse_svg(filename):
    '''
    filename: string, absolute or relative filename of an SVG file
    return: dict of Path objects corresponding to the path tags in the file
    '''
    paths = {}
    doc = xml.dom.minidom.parse(filename)       
    path_tags = doc.getElementsByTagName('path')
    for path_tag in path_tags:
        path = Path(path_tag)
        paths[path.id] = path
    return paths


def create_batch(paths):
    '''
    paths: dict of Path objects
    returns a pyglet Batch object populated with indexed GL_TRIANGLES
    '''
    batch = Batch()
    for path in paths.itervalues():
        batch.add_indexed(*path.to_verts())
    return batch    


def svg2batch(filename):
    '''
    filename: string, absolute or relative filename of an SVG file
    return a pyglet Batch made from the paths in the file
    '''
    paths = parse_svg(filename)
    for path in paths.itervalues():
        tesselate(path.loops)
    return create_batch(paths)

