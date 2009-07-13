from __future__ import division

from os.path import isfile
import sys

from pyglet import app
from pyglet.window import Window
from pyglet.gl import (
    glClear, glClearColor, glLoadIdentity, glMatrixMode, gluLookAt,
    GL_COLOR_BUFFER_BIT, GL_MODELVIEW, GL_PROJECTION, GL_TRIANGLES
)
from pyglet.gl.glu import gluOrtho2D

from svgload.svgload import svg2batch


def on_resize(width, height):
    # scale is distance from screen centre to top or bottom, in world coords
    scale = 200 
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect = width / height
    gluOrtho2D(
        -scale * aspect,
        +scale * aspect,
        -scale,
        +scale)


drawables = []

def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    for drawable in drawables:
        drawable.draw()
    return


def init_window():
    window = Window(visible=False, fullscreen=False)
    glClearColor(0.4, 0.6, 1.0, 0.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(
        0.0, 0.0, 1.0,
        0.0, 0.0, -1.0,
        0.0, 1.0, 0.0)
    window.on_resize = on_resize
    window.on_draw = on_draw
    window.set_visible()


def parse_args():
    if len(sys.argv) != 2:
        print 'USAGE: demo <filename>'
        sys.exit(1)

    filename = sys.argv[1]
    if not isfile(filename):
        print 'No such file: %s' % (filename,)
        sys.exit(1)

    return filename


def main():
    filename = parse_args()
    init_window()
    drawables.append(svg2batch(filename))
    app.run()


if __name__ == '__main__':
    main()

