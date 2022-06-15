import numpy as np
from matrix_ops import *
import pygame as pg

class Object_3Dspace():
    
    def __init__(self, render):

        self.render = render
        
        self.cube()

        self.font = pg.font.SysFont('Arial', 24, bold=True)
        self.color_faces = [(pg.Color('orange'), face) for face in self.faces]

        self.movement_flag, self.draw_vertex = True, True
        self.label = ''

    def movement(self):
        "Example rotation"
        if self.movement_flag:
            self.rotate_xz(0.01)
        

    def draw(self):
        "Draws object to screen projection"
        self.screen_projection()
        self.movement()

    def screen_projection(self):
        "translate object cords for projection to the screen"
        vertexes = self.vertex @ self.render.camera.camera_matrix()
        vertexes = vertexes @ self.render.projection.projection_mat

        vertexes /= vertexes[:,-1].reshape(-1,1) # normalises
        #print(vertexes, np.shape(vertexes))

        vertexes[(vertexes > 2) | (vertexes < -2)] = 0 # Object clipping

        vertexes = vertexes @ self.render.projection.to_screen_matrix
        vertexes = vertexes[:,:2]

        # draw faces
        for index, color_face in enumerate(self.color_faces):
            color, face = color_face
            polygon = vertexes[face]

            if not np.any((polygon == self.render.width //2) | (polygon == self.render.height //2)):
                pg.draw.polygon(self.render.screen, color, polygon, 3)
                if self.label:
                    text = self.font.render(self.label[index], True, pg.Color('White'))
                    self.render.screen.blit(text,polygon[-1])
       
        # draw vertices
        if self.draw_vertex:
            for vertex in vertexes:
                if not np.any((vertex == self.render.width //2) | (vertex == self.render.height //2)):
                    pg.draw.circle(self.render.screen, pg.Color('white'), vertex, 6)

    def tran_origin(self):
        "Translates object to the origin [0,0,0,1]"
        self.center = np.mean(self.vertex, axis = 0)
        (x,y,z,w) = self.center
        self.translate((-x,-y,-z))

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
        # Cordinate properties of a cube
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

        self.vertex = np.array([(0,0,0,1), (1,0,0,1), (0,1,0,1), (0,0,1,1)])
        self.faces = np.array([(0,1),(0,2),(0,3)])

        self.colors = [pg.Color('red'), pg.Color('green'), pg.Color('blue')]
        self.color_faces = [(color,face) for color, face in zip(self.colors, self.faces)]
        self.draw_vertex = False
        self.label = 'XYZ'




if __name__ == '__main__':
    cube = Object_3Dspace()