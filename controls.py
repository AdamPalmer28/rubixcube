"""
Handles controls for the 3D space
"""
import pygame as pg
import numpy as np

class control3D:

    def __init__(self, render):

        self.render = render
        self.camera = render.camera

        # camera postion and orientation
        self.postion = self.camera.postion

        self.right = self.camera.right
        self.forward = self.camera.forward


        # camera speeds
        self.moving_speed = 0.07
        self.rotation_speed = 0.014

        self.cin_mode = False

    def camera_controls(self):
        "Handles camera movement from key input"
        # camera postion and orientation
        self.postion = self.camera.postion

        self.right = self.camera.right
        self.forward = self.camera.forward

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
            #self.postion += self.up * self.moving_speed
        if key[pg.K_LCTRL]:
            self.postion -= np.array([0,1,0,1]) * self.moving_speed
            #self.postion -= self.up * self.moving_speed


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


        for event in pg.event.get():
            # single press controls
            if event.type == pg.KEYDOWN:

                if event.key == pg.K_0:
                    # reset camera to origin
                    self.camera.look_origin()

                if event.key == pg.K_9:
                    # toggle cinematic mode
                    self.cin_mode = not self.cin_mode

            elif event.type == pg.QUIT: # exit function
                exit()

        if self.cin_mode:
            self.cinematic_mode()

    def cinematic_mode(self):
        "demo camera mode - single step"
        self.postion += self.right * self.moving_speed
        self.camera.look_origin()