import xml.dom.minidom

from pyglet.graphics import Batch

from path import Path



def svg2batch(filename):
    '''
    filename: string, absolute or relative filename of an SVG file
    return a pyglet Batch made from all the paths in the file
    '''
    loader = SvgLoader(filename)
    return loader.create_batch()



class SvgLoader(object):
    '''
    Maintains an ordered list of paths, each one corresponding to a path tag
    from an SVG file. Adds itself to a single pylget Batch, for rendering as
    a single OpenGL primitive.
    '''
    def __init__(self, filename=None):
        '''
        filename: string, absolute or relative filename of an SVG file
        '''
        self.filename = filename
        self.paths = []


    def parse_svg(self):
        '''
        Populates self.paths from the <path> tags in the svg file.
        '''
        doc = xml.dom.minidom.parse(self.filename)       
        path_tags = doc.getElementsByTagName('path')
        for path_tag in path_tags:
            path = Path(path_tag)
            self.paths.append(path)


    def create_batch(self):
        '''
        returns a new pyglet Batch object populated with indexed GL_TRIANGLES
        '''
        batch = Batch()
        self.parse_svg()
        for path in self.paths:
            path.tessellate()
            path.add_to_batch(batch)
        return batch    

