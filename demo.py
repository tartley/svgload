from __future__ import division

from os import listdir
from os.path import isfile, join
import sys

from pyglet import app
from pyglet.window import key, Window
from pyglet.gl import (
    glClear, glClearColor, glLoadIdentity, glMatrixMode, gluLookAt,
    GL_COLOR_BUFFER_BIT, GL_MODELVIEW, GL_PROJECTION, GL_TRIANGLES
)
from pyglet.gl.glu import gluOrtho2D

from svgload.svgload import svg2batch


window = None
filenames = []
current = -1
drawables = [None]


def get_filenames():
    for filename in listdir('testdata'):
        if filename.endswith('.svg'):
            filenames.append(join('testdata', filename))


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

def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    for drawable in drawables:
        drawable.draw()
    return


def on_key_press(symbol, modifiers):
    if symbol == key.ESCAPE:
        window.close()
    parse_next_file()


def init_window():
    global window
    window = Window(visible=False, fullscreen=False)
    glClearColor(0.4, 0.6, 0.0, 0.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(
        0.0, 0.0, 1.0,
        0.0, 0.0, -1.0,
        0.0, 1.0, 0.0)
    window.on_resize = on_resize
    window.on_draw = on_draw
    window.on_key_press = on_key_press
    window.set_visible()


def parse_next_file():
    global current
    current = (current + 1) % len(filenames)
    print filenames[current]
    drawables[0] = svg2batch(filenames[current])


def main():
    get_filenames()
    parse_next_file()
    init_window()
    app.run()


if __name__ == '__main__':
    main()

