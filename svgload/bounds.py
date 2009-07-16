
class Bounds(object):

    def __init__(self):
        self.minx = None
        self.maxx = None
        self.miny = None
        self.maxy = None

    def add_point(self, x, y):
        if self.minx is None:
            self.minx = self.maxx = x
            self.miny = self.maxy = y
        else:
            self.minx = min(self.minx, x)
            self.maxx = max(self.maxx, x)
            self.miny = min(self.miny, y)
            self.maxy = max(self.maxy, y)

    def add_bounds(self, other):
        print 'add_bounds', self, other
        if other.minx is None:
            return
        elif self.minx is None:
            self.minx = other.minx
            self.maxx = other.maxx
            self.miny = other.miny
            self.maxy = other.maxy
        else:
            self.minx = min(self.minx, other.minx)
            self.maxx = min(self.maxx, other.maxx)
            self.miny = min(self.miny, other.miny)
            self.maxy = min(self.maxy, other.maxy)

    def get_center(self):
        return (
            (self.minx + self.maxx) / 2,
            (self.miny + self.maxy) / 2,
        )

    def __str__(self):
        if self.minx is None:
            return '<Bounds null>'
        return '<Bounds (%.2f, %.2f) (%.2f, %.2f)>' % (
            self.minx, self.maxx,
            self.miny, self.maxy)
        
