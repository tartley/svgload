import xml.dom.minidom

from pyglet.graphics import Batch

from path import Path
from tesselate import tesselate



def svg2batch(filename):
    '''
    filename: string, absolute or relative filename of an SVG file
    return a pyglet Batch made from all the paths in the file
    '''
    svg_batch = SvgBatch(filename)
    return svg_batch.create_batch()



class SvgBatch(object):
    '''
    Corresponds to all the geometry from an SVG file, which will be rendered
    as a single OpenGL primitive by pyglet Batch.
    '''

    def __init__(self, filename=None):
        self.paths = []
        if filename:
            self.parse_svg(filename)
            self.tessellate()

    def parse_svg(self, filename):
        '''
        filename: string, absolute or relative filename of an SVG file
        Populates self.paths from the <path> tags in the file.
        '''
        doc = xml.dom.minidom.parse(filename)       
        path_tags = doc.getElementsByTagName('path')
        for path_tag in path_tags:
            path = Path(path_tag)
            self.paths.append(path)

    def tessellate(self):
        '''
        For the arbitrary polygons in self.paths, tessellate each one into
        a single array of GL_TRIANGLES.
        '''
        for path in self.paths:
            tesselate(path.loops)


    def create_batch(self):
        '''
        returns a new pyglet Batch object populated with indexed GL_TRIANGLES
        '''
        batch = Batch()
        for path in self.paths:
            path.add_to_batch(batch)
        return batch    

