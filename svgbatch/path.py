
from pyglet.gl import GL_TRIANGLES

from bounds import Bounds
from tesselate import tesselate

class ParseError(Exception):
    pass


class PathData(object):

    def __init__(self, data):
        self.data = data
        self.pos = 0
        self.loops = []
        self.bounds = Bounds()


    def get_chars(self, chars):
        start = self.pos
        while self.pos < len(self.data) and self.data[self.pos] in chars:
            self.pos += 1
        return self.data[start:self.pos]


    def get_number(self):
        number = self.get_chars('0123456789.-')
        if '.' in number:
            return float(number)
        else:
            return int(number)


    def to_tuples(self):
        parsed = []
        command = []

        self.pos = 0
        while self.pos < len(self.data):
            indicator = self.data[self.pos]
            if indicator == ' ':
                self.pos += 1
            elif indicator == ',':
                if len(command) >= 2:
                    self.pos += 1
                else:
                    msg = 'invalid comma at %d in %r' % (self.pos, self.data)
                    raise ParseError(msg)
            elif indicator in '0123456789.-':
                if command:
                    command.append(self.get_number())
                else:
                    msg = 'missing command at %d in %r' % (self.pos, self.data)
                    raise ParseError(msg)
            else:
                if command:
                    parsed.append(tuple(command))
                command = [indicator]
                self.pos += 1

        if command:
            parsed.append(tuple(command))
        return parsed


    def get_point(self, command):
        x = command[1]
        y = -command[2]
        self.bounds.add_point(x, y)
        return x, y


    def to_loops(self, commands):
        '''
        commands : list of tuples, as output from to_tuples() method, eg:
            [('M', 1, 2), ('L', 3, 4), ('L', 5, 6), ('z')]
        Interprets the command characters at the start of each tuple to return
        a list of loops, where each loop is a closed list of verts, and each
        vert is a pair of ints or floats, eg:
            [[1, 2, 3, 4, 5, 6]]
        Note that the final point of each loop is eliminated if it is equal to
        the first.
        SVG defines commands:
            M x,y: move, start a new loop
            L x,y: line, draw boundary
            H x: move horizontal
            V y: move vertical
            Z: close current loop - join to start point
        Lower-case command letters (eg 'm') indicate a relative offset.
        See http://www.w3.org/TR/SVG11/paths.html
        '''
        loops = []
        current_path = None

        for command in commands:
            action = command[0]
            if action == 'M':
                self.bounds.reset()
                x, y = self.get_point(command)
                current_path = [(x, y)]
            elif action == 'L':
                x, y = self.get_point(command)
                current_path.append((x, y))
            elif action in 'zZ':
                if current_path[0] == current_path[-1]:
                    current_path = current_path[:-1]
                if len(current_path) < 3:
                    raise ParseError('loop needs 3 or more verts')
                loops.append(current_path)
                current_path = None
            else:
                msg = 'unsupported svg path command: %s' % (action,)
                raise ParseError(msg)
        return loops


    def parse(self):
        '''
        parse(data), where 'data' is a string. The format of 'data' matches the
        'd' attribute of an svg path tag, eg:
            'M 46,74 L 35,12 l 53,13 z'
        returns the same data collected in a list of tuples, eg:
            [ ('M', 46, 74), ('L', 35, 12), ('l', 53, 13), ('z') ],
        The input data may have floats instead of ints, this will be reflected
        in the output. The input may have its whitespace stripped out, or its
        commas replaced by whitespace.
        '''
        parsed = self.to_tuples()
        return self.to_loops(parsed)


class Path(object):

    next_id = 1

    '''
    id : string, copied from the svg tag's id attribute
    color : triple of unsigned bytes, (r, g, b)
    loops : a list of loops.
        A loop is a list of vertices. A vertex is a pair of floats or ints.
    A Path corresponds to a single SVG path tag. It may contain many
    independant loops which may represent disjoint polygons or holes.
    '''
    def __init__(self, tag=None):
        self.loops = []
        self.color = (0, 0, 0)
        self.bounds = Bounds()
        self.triangles = None

        if tag:
            self.parse(tag)


    def get_id(self, attributes):
        if 'id' in attributes.keys():
            return attributes['id'].value
        else:
            self.next_id += 1
            return self.next_id - 1


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


    def parse(self, tag):
        self.id = self.get_id(tag.attributes)
        if 'style' in tag.attributes.keys():
            style_data = tag.attributes['style'].value
            self.color = self.parse_style(style_data)
        
        path_data = PathData(tag.attributes['d'].value)
        self.loops = path_data.parse()
        self.bounds.add_bounds(path_data.bounds)
        print self.loops


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

