import pygame as pg
import numpy as np
from camera_calcs.matrix_ops import *

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


    def camera_yaw(self,angle):
        # rotate arround y cord (vertical axis)
        rotate = rotate_xz(angle)

        # rotate directions in accordance of camera rotation
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def camera_pitch(self,angle):
        # rotate camera up and down around the self.right vector

        # correction
        (x,y,z,w) = self.right
        
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
            if abs(a) <= 0.0001:
                return (1 if b > 0 else - 1) * np.pi / 2
            return np.arctan(b / a) + (np.pi if a < 0 else 0)

        x, y, z, _ = -self.postion # vector to origin
        fx, fy, fz, _ = self.forward # forward facing vector

        # rotate yaw (left and right)
        pos_angle = calc_angle(x, z)
        fwd_angle = calc_angle(fx, fz)
        self.camera_yaw((pos_angle - fwd_angle)) 

        # rotate pitch (up and down)
        fx, fy, fz, _ = self.forward # needs to be updated after rotation

        dist = np.sqrt(x**2 + z**2) 
        fdist = np.sqrt(fx**2 + fz**2)

        pos_angle2 = np.arctan(y / dist)
        fwd_angle2 = np.arctan(fy / fdist)
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
    







