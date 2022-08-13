# 3D game engine

import numpy as np
import pygame as pg


from camera_calcs.camera import camera3D
from camera_calcs.projection import *

from objects.object3D import *
from objects.cube_model import *

from controls import control3D

class SoftwareRender:

    def __init__(self) -> None:
        self.res = self.width, self.height = 1200, 800 #1680, 945 #1200, 800
        self.FPS = 60
        self.screen = pg.display.set_mode(self.res)
        self.clock = pg.time.Clock()

        self.create_objects()

        self.controls = control3D(self)



        
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
        self.rubix = rubix_cube(self, n = 3)

        # test
        # self.test_cube = Object_3Dspace(self)
        # rubix_colours = ['red','#b34c07','white','yellow','blue','green']
        # self.test_cube.colors = rubix_colours
        # self.test_cube.new_colors()

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
            
            self.controls.camera_controls() # camera control
            #self.camera.control() # camera control


            pg.display.set_caption(str(self.clock.get_fps())) # display fps in window name
            pg.display.flip() # update screen
            self.clock.tick(self.FPS)



if __name__ == '__main__':
    render = SoftwareRender()

    
    # == Optermisation ==
    import cProfile
    import pstats

    #render.run()
    cProfile.run("render.run()", "code_analysis/output.dat")
    
    with open("code_analysis/output_time.txt","w") as f:
        p = pstats.Stats("code_analysis/output.dat", stream=f)
        p.sort_stats("time").print_stats()
    
    with open("code_analysis/output_calls.txt","w") as f:
        p = pstats.Stats("code_analysis/output.dat", stream=f)
        p.sort_stats("calls").print_stats()

    with open("code_analysis/output_ctime.txt","w") as f:
        p = pstats.Stats("code_analysis/output.dat", stream=f)
        p.sort_stats("cumulative").print_stats()
