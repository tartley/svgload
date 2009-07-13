from itertools import chain
import xml.dom.minidom

from pyglet.graphics import Batch
from pyglet.gl import (
    GL_TRIANGLES
)


class ParseError(Exception):
    pass


class Path(object):
    '''
    Corresponds to a single SVG path tag. It may contain many independant loops
    which may represent disjoint polygons or holes. All loops share a single
    color.
    '''
    def __init__(self, path_tag):
        self.id = path_tag.attributes['id'].value

        style_data = path_tag.attributes['style'].value
        self.color = self.parse_style(style_data)

        path_data = path_tag.attributes['d'].value
        self.loops = self.parse_path(path_data)


    def parse_color(self, color):
        return (
            int(color[1:3], 16),
            int(color[3:5], 16),
            int(color[5:7], 16))


    def parse_style(self, style):
        '''
        style : string
        returns color as a triple of unsigned bytes: (r, g, b)
        '''
        style_elements = style.split(';')
        while style_elements:
            element = style_elements.pop()
            if element.startswith('fill:'):
                return self.parse_color(element[5:])
        return (0, 0, 0)


    def parse_coord(self, coord):
        '''
        coord : string, eg. '12.345,67.890'
        returns tuple, eg. (12.345, 67.89)
        '''
        return tuple(map(float, coord.split(',')))


    def parse_path(self, path):
        '''
        path: string, eg:
            M 460.62992,744.09441 L 35.433071,1240.1574 L 531.49606,1381.8897
            L 460.62992,744.09441 z 
        returns list of loops, one for each M L L L z sequence, eg. [
            [ 
                [ (460.6,744.0), (35.4, 1240.1), (531.4, 1381.8) ],
                etc...
            ]
        SVG defines:
            M - move to start a new path
            L - line, draw boundary
            z - close current path - join to start point
        Note that the final point is eliminated if it is redundant.
        '''
        loops = []
        current_path = None
        items = list(reversed(path.split()))
        while items:
            item = items.pop()
            if item == 'M':
                current_path = [self.parse_coord(items.pop())]
            elif item == 'L':
                current_path.append(self.parse_coord(items.pop()))
            elif item == 'z':
                if current_path[0] == current_path[-1]:
                    current_path = current_path[:-1]
                loops.append(current_path)
                current_path = None
            else:
                raise ParseError('unsupported svg path item: %s' % (item,))
        return loops


    def to_verts(self):
        '''
        return a tuple representing this path's loops, suitable for passing
        to pyglet's Batch.add_indexed()
        '''
        num_verts = len(self.loops[0])
        indices = range(num_verts)
        serial_verts = list(chain(*self.loops[0]))
        colors = self.color * num_verts
        return (
            num_verts,
            GL_TRIANGLES,
            None,
            indices,
            ('v2f/static', serial_verts),
            ('c3B/static', colors),
        )


def create_batch(paths):
    '''
    svg_paths: dict of Path objects
    returns a pyglet Batch populated with indexed GL_TRIANGLES
    '''
    path = paths.values()[0]
    batch = Batch()
    batch.add_indexed(*path.to_verts())
    return batch    


def svg2batch(filename):
    '''
    filename: string, absolute or relative filename
    return a pyglet Batch made from the given SVG file
    '''
    paths = {}
    doc = xml.dom.minidom.parse(filename)       
    path_tags = doc.getElementsByTagName('path')
    for path_tag in path_tags:
        path = Path(path_tag)
        paths[path.id] = path
    return create_batch(paths)
    
