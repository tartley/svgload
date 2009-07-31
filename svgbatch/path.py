
from pyglet.gl import GL_TRIANGLES

from bounds import Bounds
from tesselate import tesselate

class ParseError(Exception):
    pass


class Path(object):
    '''
    id : string, copied from the svg tag's id attribute
    color : triple of unsigned bytes, (r, g, b)
    loops : a list of loops.
        A loop is a list of vertices. A vertex is a pair of floats or ints.
        See 'parse_path'
    A Path corresponds to a single SVG path tag. It may contain many
    independant loops which may represent disjoint polygons or holes.
    '''
    def __init__(self, path_tag):
        self.id = path_tag.attributes['id'].value
        self.bounds = Bounds()

        style_data = path_tag.attributes['style'].value
        self.color = self.parse_style(style_data)

        path_data = path_tag.attributes['d'].value
        self.loops = self.parse_path(path_data)

        self.triangles = None


    def parse_color(self, color):
        '''
        color : string, eg: '#rrggbb' or 'none'
        (where rr, gg, bb are hex digits from 00 to ff)
        returns a triple of unsigned bytes, eg: (0, 128, 255)
        '''
        if color == 'none':
            return None
        return (
            int(color[1:3], 16),
            int(color[3:5], 16),
            int(color[5:7], 16))


    def parse_style(self, style):
        '''
        style : string, eg:
            fill:#ff2a2a;fill-rule:evenodd;stroke:none;stroke-width:1px;
            stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1
        returns color as a triple of unsigned bytes: (r, g, b), or None
        '''
        style_elements = style.split(';')
        while style_elements:
            element = style_elements.pop()
            if element.startswith('fill:'):
                return self.parse_color(element[5:])
        return None


    def parse_coord(self, items):
        '''
        items: list of strings, which may end with either of:
            [..., 'x,y']
            [..., 'y', 'x']
            where x and y look like either ints or floats.
        returns tuple (x, y) as floats.
        Pops consumed values off the list.
        Returned Y co-ord is inverted - SVG Y-axis points down, we use up.
        '''
        first = items.pop()
        comma_separated = first.split(',')
        
        # coords are comma separated
        if len(comma_separated) == 2:
            x = float(comma_separated[0])
            y = -float(comma_separated[1])

        # coords are space separated
        elif len(comma_separated) == 1:
            x = float(first)
            y = -float(items.pop())

        else:
            raise ValueError('parse_coord fail: %s' % first)

        self.bounds.add_point(x, y)
        return (x, y)


    def parse_path(self, path):
        '''
        path: string, eg:
            M 460.6,744.0 L 35.4,120.1 L 531.4,131.8 L 460.6,744.0 z etc...
            (or with space instead of the commas)
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
                current_path = [self.parse_coord(items)]
            elif item == 'L':
                current_path.append(self.parse_coord(items))
            elif item == 'z':
                if current_path[0] == current_path[-1]:
                    current_path = current_path[:-1]
                loops.append(current_path)
                current_path = None
            else:
                raise ParseError('unsupported svg path item: %s' % (item,))
        return loops


    def offset(self, x, y):
        for loop in self.loops:
            for idx, vert in enumerate(loop):
                loop[idx] = (vert[0] + x, vert[1] + y)
        self.bounds.offset(x, y)


    def tessellate(self):
        if self.color:
            self.triangles = tesselate(self.loops)


    def _serialise_verts(self):
        for vert in self.triangles:
            yield vert[0]
            yield vert[1]


    def add_to_batch(self, batch):
        '''
        Adds itself to the given batch, as as single primitive of indexed
        GL_TRIANGLES. Note that Batch will aggregate all such additions into
        a single large primitive.
        '''
        if self.triangles:
            num_verts = len(self.triangles)
            serial_verts = list(self._serialise_verts())
            colors = self.color * num_verts
            indices = range(num_verts)
            batch.add_indexed(
                num_verts,
                GL_TRIANGLES,
                None,
                indices,
                ('v2f/static', serial_verts),
                ('c3B/static', colors),
            )

