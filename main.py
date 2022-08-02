# 3D game engine

import numpy as np
import pygame as pg

from object3D import *
from camera import *
from projection import *

from cube_model import *

class SoftwareRender:

    def __init__(self, camera_control = False) -> None:
        self.res = self.width, self.height = 1680, 945 #1200, 800
        self.FPS = 60
        self.screen = pg.display.set_mode(self.res)
        self.clock = pg.time.Clock()

        self.create_objects()

        self.camera_control = camera_control
        self.fix_cam = False

        
    def create_objects(self):
        "Object creation and camera"
        intial_cam = [0.1,4,-10]
        self.camera = camera3D(self, intial_cam) # intialise camera class
        self.camera.look_origin()

        self.projection = projection(self) # projection calcs

        pg.font.init()

        # world axes
        self.world_axes = Axes(self)
        self.world_axes.movement_flag = False # World axes cannot move or rotate
        self.world_axes.scale(2.5)
        #self.world_axes.translate([0.0001, 0.0001, 0.0001])

        # rubix cube
        self.rubix = rubix_cube(self, n = 8)

        # test
        #self.test_cube = Object_3Dspace(self)
        #rubix_colours = ['yellow','red','blue','white','green','orange']
        #self.test_cube.color = rubix_colours

    def draw(self):
        # collective draw function
        self.screen.fill(pg.Color('darkgrey')) # background

        self.rubix.draw()
        
        
        # self.world_axes.draw() # world axes

        # test cube
        #self.test_cube.draw()
    

    def run(self):
        "[Driver function] run app/program"
        while True:
            self.draw()
            
            #if self.camera_control:

            self.camera.control() # camera control

            

            pg.display.set_caption(str(self.clock.get_fps())) # display fps in window name
            pg.display.flip() # update screen
            self.clock.tick(self.FPS)



if __name__ == '__main__':
    render = SoftwareRender(camera_control=True)

    render.run()
