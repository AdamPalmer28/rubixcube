"""
Handles controls for the 3D space
"""
import pygame as pg
import numpy as np

class control3D:

    def __init__(self, render):

        self.render = render
        self.camera = render.camera
        self.rubix = render.rubix

        # camera postion and orientation
        self.postion = self.camera.postion

        self.right = self.camera.right
        self.forward = self.camera.forward

        # camera speeds
        self.moving_speed = 0.07
        self.rotation_speed = 0.014

        self.cin_mode = False # toggle cinematic mode

    def controls(self):
        "Handles camera movement from key input"
        # [update] camera postion and orientation
        self.postion = self.camera.postion

        self.right = self.camera.right
        self.forward = self.camera.forward

        self.basic_cam_controls() # camera controls

        for event in pg.event.get():
            # single press controls
            if event.type == pg.KEYDOWN:

                if event.key == pg.K_x:
                    # reset camera to origin
                    self.camera.look_origin()

                if event.key == pg.K_c:
                    # toggle cinematic mode
                    self.cin_mode = not self.cin_mode

                if event.key == pg.K_r:
                    # reset rubix cube
                    self.rubix.intialise()

                # =====================================
                # Rotations
                # =====================================
                # rotate xy
                if event.key == pg.K_1:
                    self.rubix.model_rotate_xy(ind = 0)
                if event.key == pg.K_2:
                    self.rubix.model_rotate_xy(ind = 1)                
                if event.key == pg.K_3:
                    self.rubix.model_rotate_xy(ind = 2)   
                # rotate xz
                if event.key == pg.K_4:
                    self.rubix.model_rotate_xz(ind = 0)
                if event.key == pg.K_5:
                    self.rubix.model_rotate_xz(ind = 1)                
                if event.key == pg.K_6:
                    self.rubix.model_rotate_xz(ind = 2)
                # rotate yz
                if event.key == pg.K_7:
                    self.rubix.model_rotate_yz(ind = 0)
                if event.key == pg.K_8:
                    self.rubix.model_rotate_yz(ind = 1)                
                if event.key == pg.K_9:
                    self.rubix.model_rotate_yz(ind = 2)               


            elif event.type == pg.QUIT: # exit function
                exit()

        if self.cin_mode:
            self.cinematic_mode()

    def cinematic_mode(self):
        "cinematic camera mode - single step"
        self.postion += self.right * self.moving_speed # moves right
        self.camera.look_origin() # camera looks origin

    def basic_cam_controls(self):
        key = pg.key.get_pressed()

         # --===<[ Movement ]>===--

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
        if key[pg.K_LCTRL]:
            self.postion -= np.array([0,1,0,1]) * self.moving_speed


        # --===<[ Rotations ]>===--

        # left / right rotation
        if key[pg.K_LEFT]:
            self.camera.camera_yaw(self.rotation_speed)
        if key[pg.K_RIGHT]:
            self.camera.camera_yaw(-self.rotation_speed)
        # up / down rotation
        if key[pg.K_UP]:
            self.camera.camera_pitch(self.rotation_speed)
        if key[pg.K_DOWN]:
            self.camera.camera_pitch(-self.rotation_speed)


        