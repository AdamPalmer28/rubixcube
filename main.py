# 3D game engine

import numpy as np
import pygame as pg

from object3D import *
from camera import *
from projection import *

from cube_model import *

class SoftwareRender:

    def __init__(self) -> None:
        self.res = self.width, self.height = 1680, 945 #1200, 800
        self.FPS = 60
        self.screen = pg.display.set_mode(self.res)
        self.clock = pg.time.Clock()

        self.create_objects()

        
    def create_objects(self):
        "Object creation and camera"
        intial_cam = [-1,0.5,-4]
        self.camera = camera3D(self, intial_cam) # intialise camera class

        self.projection = projection(self) # projection calcs

        pg.font.init()
        self.object = Object_3Dspace(self) # create cube object

        translate_val = [1,0.5,0.2]
        self.object.translate(translate_val)
        #self.object.origin()

        # object axes
        self.axes = Axes(self)
        object_axes = [val + 0.5 for val in translate_val]
        self.axes.translate(object_axes)

        # world axes
        self.world_axes = Axes(self)
        self.world_axes.movement_flag = False # World axes cannot move or rotate
        self.world_axes.scale(2.5)
        self.world_axes.translate([0.0001, 0.0001, 0.0001])



    def draw(self):
        # collective draw function
        self.screen.fill(pg.Color('darkgrey')) # background

        self.world_axes.draw() # world axes

        self.axes.draw() # object axes
        self.object.draw() # draw objects

    def run(self):
        "[Driver function] run app/program"
        while True:
            self.draw()
            
            #[exit() for i in pg.event.get() if i.type == pg.QUIT] # exit function
            self.camera.control() # camera controls

            

            pg.display.set_caption(str(self.clock.get_fps())) # display fps in window name
            pg.display.flip() # update screen
            self.clock.tick(self.FPS)



if __name__ == '__main__':
    render = SoftwareRender()
    render.run()
