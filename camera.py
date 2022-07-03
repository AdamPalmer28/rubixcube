import pygame as pg
import numpy as np
from matrix_ops import *

class camera3D:
    "Camera class for the 3D render space"
    def __init__(self, render, position):
        self.postion = np.array([*position, 1.0])
        # directions
        self.forward = np.array([0,0,1,1])
        self.up = np.array([0,1,0,1])
        self.right = np.array([1,0,0,1])

        # FOV
        self.h_fov = np.pi / 3 # horizontal FOV
        self.v_fov = self.h_fov * (render.height)/(render.width) # vertical FOV

        self.near_plane = 0.1
        self.far_plane = 100

        # movement parameters
        self.moving_speed = 0.02
        self.rotation_speed = 0.01

    def control(self):
        "Handles camera movement from key input"
        key = pg.key.get_pressed()

        # left / right
        if key[pg.K_a]:
            self.postion -= self.right * self.moving_speed
        if key[pg.K_d]:
            self.postion += self.right * self.moving_speed

        # forward / backwards
        if key[pg.K_w]:
            self.postion += self.forward * self.moving_speed
        if key[pg.K_s]:
            self.postion -= self.forward * self.moving_speed

        # up / down
        if key[pg.K_SPACE]:
            self.postion += np.array([0,1,0,1]) * self.moving_speed
            #self.postion += self.up * self.moving_speed
        if key[pg.K_LCTRL]:
            self.postion -= np.array([0,1,0,1]) * self.moving_speed
            #self.postion -= self.up * self.moving_speed


        # rotations

        # left / right rotation
        if key[pg.K_LEFT]:
            self.camera_yaw(self.rotation_speed)
        if key[pg.K_RIGHT]:
            self.camera_yaw(-self.rotation_speed)
        # up / down rotation
        if key[pg.K_UP]:
            self.camera_pitch(self.rotation_speed)
        if key[pg.K_DOWN]:
            self.camera_pitch(-self.rotation_speed)


        for event in pg.event.get():
            # single press controls
            if event.type == pg.KEYDOWN:

                if event.key == pg.K_0:
                    # reset camera to origin
                    self.look_origin()

            elif event.type == pg.QUIT: # exit function
                exit()
                
        

    def camera_yaw(self,angle):
        # rotate arround y cord (vertical axis)
        rotate = rotate_xz(angle)

        # rotate directions in accordance of camera rotation
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def camera_pitch(self,angle):
        # rotate camera up and down arround the self.right vector

        # correction
        (x,y,z,w) = self.right
        #
        rotate = np.array([[np.cos(angle) + x**2 *(1-np.cos(angle)), x*y*(1-np.cos(angle)) - z*np.sin(angle), x*z*(1-np.cos(angle)) + y*np.sin(angle), 0],
                    [y*x*(1-np.cos(angle)) + z*np.sin(angle), np.cos(angle) + y**2 *(1-np.cos(angle)), y*z*(1-np.cos(angle)) - x*np.sin(angle),0],
                    [x*z*(1-np.cos(angle)) - y*np.sin(angle), z*y*(1-np.cos(angle)) + x*np.sin(angle), np.cos(angle) + z**2 *(1-np.cos(angle)),0],
                    [0,0,0,1]])
        
        # rotate directions in accordance of camera rotation
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate 
        self.up = self.up @ rotate  

    def look_origin(self):
        "Makes camera look at the origin (i.e. centre of render)"
        def calc_angle(a,b):
            "calcs exact angle"
            if a == 0:
                return (1 if b > 0 else - 1) * np.pi / 2
            return np.arctan(b / a) + (np.pi if a < 0 else 0)

        x, y, z, _ = -self.postion # vector to origin
        fx, fy, fz, _ = self.forward # forward facing vector

        # rotate yaw 
        pos_angle = calc_angle(x, z)
        fwd_angle = calc_angle(fx, fz)
        self.camera_yaw((pos_angle - fwd_angle))

        # rotate pitch
        fx, fy, fz, _ = self.forward # needs to be updated after rotation
        pos_angle2 = np.arctan(y / abs(z))
        fwd_angle2 = np.arctan(fy / abs(fz))
        self.camera_pitch((pos_angle2 - fwd_angle2))


    def translate_mat(self):
        x,y,z,w = self.postion
        return np.array([[1,0,0,0],
                        [0,1,0,0],
                        [0,0,1,0],
                        [-x,-y,-z,1]])

    def rotate_mat(self):
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return np.array([[rx, ux, fx, 0],
                        [ry, uy, fy, 0],
                        [rz, uz, fz, 0],
                        [0, 0, 0, 1]])

    def camera_matrix(self):
        return self.translate_mat() @ self.rotate_mat()
    







