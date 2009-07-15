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


class SvgFiles(object):

    def __init__(self):
        self.filenames = self.get_filenames('testdata')
        self.number = -1
        self.current = None
        self.next()

    def get_filenames(self, path):
        return [
            join(path, filename)
            for filename in listdir(path)
            if filename.endswith('.svg')
        ]

    def next(self):
        self.number = (self.number + 1) % len(self.filenames)
        print
        print self.filenames[self.number]
        self.current = svg2batch(self.filenames[self.number])



class PygletApp(object):

    def __init__(self):
        self.window = Window(visible=False, fullscreen=False)
        self.window.on_resize = self.on_resize
        self.window.on_draw = self.on_draw
        self.window.on_key_press = self.on_key_press

        self.files = SvgFiles()

        glClearColor(0.4, 0.6, 0.0, 0.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(
            0.0, 0.0, 1.0,
            0.0, 0.0, -1.0,
            0.0, 1.0, 0.0)


    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        self.files.current.draw()


    def on_resize(self, width, height):
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


    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.window.close()
            return
        self.files.next()


    def run(self):
        self.window.set_visible()
        app.run()



def main():
    app = PygletApp()
    app.run()


if __name__ == '__main__':
    main()

