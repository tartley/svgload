from itertools import chain
import xml.dom.minidom

from pyglet.graphics import Batch
from pyglet.gl import (
    GL_TRIANGLES
)


class ParseError(Exception):
    pass


def parse_coord(coordstr):
    return tuple(map(float, coordstr.split(',')))

def parse_path(pathstr):
    '''
    pathstr : string
    Given pathstr in the format:
        M 460.62992,744.09441 L 35.433071,1240.1574 L 531.49606,1381.8897
        L 460.62992,744.09441 z 
    returns a list of paths, one for each M L L z sequence.
    SVG defines:
        M - move to start a new path
        L - line, draw boundary
        z - close current path - join to start point
    '''
    paths = []
    current_path = None
    items = list(reversed(pathstr.split()))
    while items:
        item = items.pop()
        if item == 'M':
            current_path = [parse_coord(items.pop())]
        elif item == 'L':
            current_path.append(parse_coord(items.pop()))
        elif item == 'z':
            if current_path[0] == current_path[-1]:
                current_path = current_path[:-1]
            paths.append(current_path)
            current_path = None
        else:
            raise ParseError('unsupported svg path item: %s' % (item,))

    return paths


def create_batch(vertslists):
    batch = Batch()
    for verts in vertslists:
        num_verts = len(verts)
        serial_verts = list(chain(*verts))
        colors = (255, 0, 0) * num_verts
        indices = (0, 1, 2)
        batch.add_indexed(
            num_verts, GL_TRIANGLES, None,
            indices,
            ('v2f/static', serial_verts),
            ('c3B/static', colors)) 
    return batch    


def svg2batch(filename):
    '''Return a pyglet Batch made from the given SVG file'''
    doc = xml.dom.minidom.parse(filename)       
    paths = doc.getElementsByTagName('path')
    for path in paths:
        vertexdata = path.attributes['d'].value
        verts = parse_path(vertexdata)
    return create_batch(verts)
    

def cheat():
    num_verts = 4
    verts = (
        -60.0, -65.0,
        20.0, 80.0,
        60.0, -80.0,
        0.0, -60.0,
    )
    colors = (
        255, 000, 000,
        000, 255, 000,
        000, 000, 255,
        255, 000, 255,
    )
    indices = (
        0, 1, 3,
        3, 1, 2,
    )
    batch = Batch()
    batch.add_indexed(
        num_verts, GL_TRIANGLES, None,
        indices,
        ('v2f/static', verts),
        ('c3B/static', colors)) 
    return batch

