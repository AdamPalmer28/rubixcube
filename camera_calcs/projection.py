import numpy as np


class projection:

    def __init__(self,render):

        near = render.camera.near_plane
        far = render.camera.far_plane

        # intermediate calcs
        right = np.tan(render.camera.h_fov / 2)
        left = - right
        top = np.tan(render.camera.v_fov / 2)
        bottom = - top

        # matrix entries
        m00 = 2 / (right - left)
        m11 = 2 / (top - bottom)
        m22 = (far + near) / (far - near)
        m32 = -2 * near * far / (far - near)

        self.projection_mat = np.array([
                            [m00,0,0,0],
                            [0,m11,0,0],
                            [0,0,m22,1],
                            [0,0,m32,0]
                                       ])

        # final calc matrix
        HW, HH = render.width // 2, render.height // 2
        self.to_screen_matrix = np.array([
            [HW,0,0,0],
            [0,-HH,0,0],
            [0,0,1,0],
            [HW,HH,0,1]
            ])