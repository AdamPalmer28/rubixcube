import numpy as np
from matrix_ops import *
import pygame as pg
import collections

# improve np.any function
from numba import njit
@njit(fastmath = True)

def any_fn( arr, a, b):
    return np.any((arr == a) | (arr == b))


class Object_3Dspace():
    
    def __init__(self, render):

        self.render = render
        
        self.cube()
        

        self.font = pg.font.SysFont('Arial', 24, bold=True)
        self.color_faces = [(pg.Color('orange'), face) for face in self.faces]

        self.movement_flag, self.draw_vertex = True, True
        self.solid_obj = True # solid polygons
        self.label = ''

        self.calc_visable()
        self.max_vertex = 0

    def movement(self):
        "Example rotation"
        if self.movement_flag:
            #self.rotate_xz(0.01)
            pass

    def draw(self):
        "Draws object to screen projection"
        # calc furthest vertex

        if self.solid_obj:
            self.calc_visable() # calc visable parts of the object 

        self.screen_projection()
        self.movement()

    def screen_projection(self):
        "translate object cords for projection to the screen"
        vertexes = self.vertex @ self.render.camera.camera_matrix()
        vertexes = vertexes @ self.render.projection.projection_mat

        vertexes /= vertexes[:,-1].reshape(-1,1) # normalises

        vertexes[(vertexes > 2) | (vertexes < -2)] = 0 # Object clipping

        vertexes = vertexes @ self.render.projection.to_screen_matrix
        vertexes = vertexes[:,:2]

        if self.solid_obj:

            # draw faces
            for (color, face) in self.visable_faces:

                polygon = vertexes[face]

                if not any_fn(polygon, self.render.width //2, self.render.height //2):
                    # draw faces
                    pg.draw.polygon(self.render.screen, color, polygon, 0)
                    pg.draw.polygon(self.render.screen, 'white', polygon, 1)

        else: # not solid object
            
            for index, color_face in enumerate(self.color_faces):
                color, face = color_face

                polygon = vertexes[face]

                if not any_fn(polygon, self.render.width //2, self.render.height //2):
                    # draw faces
                    pg.draw.polygon(self.render.screen, color, polygon, 2)

                    # label   
                    if self.label:
                        text = self.font.render(self.label[index], True, pg.Color('White'))
                        self.render.screen.blit(text,polygon[-1])
                        pg.draw
       
       
        # draw vertices
        if self.draw_vertex:
            for ind, vertex in enumerate(vertexes):
                # don't draw furthest vertex
                if (self.solid_obj) and (ind == self.max_vertex):
                    continue

                if not any_fn(vertex, self.render.width //2, self.render.height //2):
                    pg.draw.circle(self.render.screen, pg.Color('white'), vertex, 6)


    def calc_visable(self):
        "Calculates visable faces and vertexs"
        camera_postion = self.render.camera.postion

        self.face_distance = {}
        # face distances
        for ind, (colour, face) in enumerate(self.color_faces):
            face_centre = np.mean(self.vertex[face], axis=0)
            dif = (face_centre - camera_postion)
            distance = np.sqrt( (dif ** 2).sum() )
            distance = np.round(distance, 4)

            self.face_distance[distance] = (colour, face)

        closest_faces_keys = sorted(self.face_distance.keys(), reverse=True)[3:]
        self.visable_faces = [(self.face_distance[dist]) for dist in closest_faces_keys]

        # vertex distances
        max_v_dist = 0

        for ind, vertex in enumerate(self.vertex):
            dif = (vertex - camera_postion) # vector between camera and centre
            distance = np.sqrt( (dif ** 2).sum() ) # update distance
            
            if distance > max_v_dist: # check max distance
                max_v_dist = distance
                self.max_vertex = ind
        


    def get_center(self):
        "Get center of object"
        self.center = np.mean(self.vertex, axis = 0)
        return self.center

    def tran_origin(self):
        "Translates object to the origin [0,0,0,1]"
        #self.get_center()
        (x,y,z,w) = self.get_center()
        self.translate((-x,-y,-z))

    def distance(self):
        "Calcs distance to camera"
        #self.get_center() # update center value
        dif = (self.render.camera.postion - self.get_center()) # vector between camera and centre

        self.cam_dist = np.sqrt( (dif**2).sum() ) # Efficient distance/norm calc 

        

    # transformations

    def translate(self, pos):
        (x,y,z) = pos
        self.vertex = self.vertex @ translate(x, y, z)

    def scale(self, scale_con):
        self.vertex = self.vertex @ scale(scale_con)
    
    def rotate_xy(self, angle):
        self.vertex = self.vertex @ rotate_xy(angle)

    def rotate_xz(self, angle):
        self.vertex = self.vertex @ rotate_xz(angle)

    def rotate_yz(self, angle):
        self.vertex = self.vertex @ rotate_yz(angle)




    def cube(self):
        # Cordinates of a 1x1x1 cube
        self.vertex = np.array([(0,0,0,1), (1,0,0,1), (1,0,1,1), (0,0,1,1),
                                (0,1,0,1), (1,1,0,1), (1,1,1,1), (0,1,1,1)])

        self.edges = np.array([(0,1), (0,4), (0,3), (1,5), (1,2), (2,3),
                               (2,6), (3,7), (4,5), (4,7), (5,6), (6,7)])

        self.faces = np.array([(0,1,2,3), (0,1,5,4), (1,2,6,5),
                               (4,5,6,7), (0,4,7,3), (2,3,7,6)])




class Axes(Object_3Dspace):
    "Sub class of object, to draw object and world axes"
    def __init__(self, render):
        super().__init__(render)

        self.solid_obj = False
        self.vertex = np.array([(0,0,0,1), (1,0,0,1), (0,1,0,1), (0,0,1,1)])
        self.faces = np.array([(0,1),(0,2),(0,3)])

        self.colors = [pg.Color('red'), pg.Color('green'), pg.Color('blue')]
        self.color_faces = [(color,face) for color, face in zip(self.colors, self.faces)]
        self.draw_vertex = False
        self.label = 'XYZ'



class cube_block(Object_3Dspace):
    "Sub class - individual cube blocks of the rubix cube"
    def __init__(self, render):
        super().__init__(render)

        self.tran_origin() # starting postion at origin 



if __name__ == '__main__':
    cube = Object_3Dspace()