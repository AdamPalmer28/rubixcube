"Class for the 3D rubix model - depnds on object3D"

import numpy as np
from .object3D import *
import collections


class rubix_cube():
    """
    3D object of a rubix cube
    n - int :  number 
    """
    def __init__(self, render, n: int):
        ""
        self.n = n
        self.n_cubes = 2* n**2  +  4*(n-2)*(n-1) # number of cubes needed 

        self.render = render
        self.camera = render.camera

        # interval between cube squares
        self.block_interval_size = 0.25
        self.block_distances = 1 + self.block_interval_size

        # Create cube objects
        self.outter_edge = self.n / 2 + (self.n - 1) / 2 * self.block_interval_size
        self.outter_center = self.outter_edge - 0.5 # assuming 0.5 = block size / 2
        
        # 6 faces centers 
        self.face_centers = np.array([(self.outter_center, 0, 0, 1), (-self.outter_center, 0, 0, 1),
                                        (0, self.outter_center, 0, 1), (0, -self.outter_center, 0, 1),
                                        (0, 0, self.outter_center, 1), (0, 0, -self.outter_center, 1),
                                    ])
        self.face_colors = ['blue','green','white','yellow','#eb6207','red']

        self.cam_dist = [0,0,0,0,0,0]
        
        self.intialise() # intialise cube blocs postions and colours


    # this isnt working right!!!
    def model_cube_layers(self):
        "Segments into cube into layers" 
        self.blocks_xy = [[] for _ in range(self.n)] # segments cube blocks into xy rows
        self.blocks_xz = [[] for _ in range(self.n)] # segments cube blocks into xz rows
        self.blocks_yz = [[] for _ in range(self.n)] # segments cube blocks into yz rows
        self.layers = [self.blocks_yz, self.blocks_xz, self.blocks_xy] # all layers

        for cube in self.cube_blocks:
            pos = cube.get_center() # update current postion

            for ind, i in enumerate(pos[:3]):
                layer = self.layers[ind] # relevant postion layer

                layer_ind = int((i + self.outter_center) // self.block_distances) # postion in layer
                
                layer[layer_ind].append(cube) # appends cube to relevant layers

        # face blocs
        self.face_blocs = [[],[],[],[],[],[]] # intialise faces bloc var 

        self.face_blocs[0], self.face_blocs[1] = self.blocks_yz[-1], self.blocks_yz[0] # blue, green
        self.face_blocs[2], self.face_blocs[3] = self.blocks_xz[-1], self.blocks_xz[0] # white, yellow
        self.face_blocs[4], self.face_blocs[5] = self.blocks_xy[-1], self.blocks_xy[0] # orange, red

            

    def calc_vis_faces(self):
        "Calculates the visable faces - depending on the camera position"
        visable_faces_ind = []
        for ind, cord in enumerate(self.camera.postion[:3]):

            face_ind = (2 * ind + 1 if cord < 0 else 2 * ind)
            visable_faces_ind.append(face_ind)
        visable_faces_ind = np.array(visable_faces_ind)

        # distances to faces - calcs
        vis_face_cen = self.face_centers[visable_faces_ind]
        cam_dist = []
        cam_pos = self.camera.postion
        for ind, face in enumerate(vis_face_cen):
            dif = (cam_pos - face) # vector between camera and centre

            cam_dist.append(np.sqrt( (dif**2).sum() ) )# Efficient distance/norm calc 
        
        # distance_order
        face_order = np.argsort(cam_dist)
        self.visable_faces_ind = visable_faces_ind[face_order[::-1]]

    def draw(self):
        # draws cube to screen
        # self.model_cube_layers() # only necessary after rubix movement

        self.calc_vis_faces() # only necessary after camera movement

        # visable_blocs
        self.vis_cubes = []
        for face_ind in self.visable_faces_ind:
            self.vis_cubes += self.face_blocs[face_ind]


        # calc dist
        self.d_cubes = {}
        for cube in self.vis_cubes:

            self.d_cubes[cube.distance()] = cube

        sorted_cubes_keys = sorted(self.d_cubes.keys(), reverse=True)
        self.vis_d_cubes =  {k: self.d_cubes[k] for k in  sorted_cubes_keys} 
        
        # draw cubes
        for dist, cube in self.vis_d_cubes.items():
            cube.draw(faces = False)


    # Rotation of the cube
    # ====================
    def model_rotate_xy(self, ind: int):
        "rotation xy for the cube model"

        layer = self.blocks_xy[ind] # cubes to be rotated
        layer = self.layers[2][ind]
        for cube in layer:
            cube.rotate_xy(np.pi/2)

        self.model_cube_layers() # recalc cube layers
 
    def model_rotate_xz(self, ind: int):
        "rotation xz for the cube model"

        layer = self.blocks_xz[ind] # cubes to be rotated
        for cube in layer:
            cube.rotate_xz(np.pi/2)

        self.model_cube_layers() # recalc cube layers    
    
    def model_rotate_yz(self, ind: int):
        "rotation yz for the cube model"

        layer = self.blocks_yz[ind] # cubes to be rotated
        for cube in layer:
            cube.rotate_yz(np.pi/2)

        self.model_cube_layers() # recalc cube layers


    # only run at the start of the model
    def intialise(self):
        "Intialise the cube postions in the rubix cube along with the associated colours"

        self.cube_blocks = [] # all cube blocks

        # bottom / top of rubix cube
        bottom = np.array([-self.outter_center, -self.outter_center, -self.outter_center])
        top = np.array([-self.outter_center, self.outter_center, -self.outter_center])
        
        for i in range(self.n):
            increment_i = np.array([i * (1 + self.block_interval_size), 0, 0])

            for j in range(self.n):
                increment_j = np.array([0, 0, j * (1 + self.block_interval_size) ])

                tran_vec_b = bottom + increment_i + increment_j
                tran_vec_t = top + increment_i + increment_j

                # top
                temp = cube_block(self.render)
                temp.translate(tran_vec_t)
                self.cube_blocks.append(temp)

                # bottom
                temp = cube_block(self.render)
                temp.translate(tran_vec_b)
                self.cube_blocks.append(temp)


        self.render.camera.postion

        
        # middle rubix cube

        start = bottom + np.array([0, (1 + self.block_interval_size), 0]) 
        for row in range(self.n - 2):
            # rows 
            increment_k = row*(1 + self.block_interval_size)
            y = start[1] + increment_k
            for side in range(4):
                # circuit

                # corners
                side_starts = [(-self.outter_center, -self.outter_center), (self.outter_center, self.outter_center),
                                (self.outter_center, -self.outter_center), (-self.outter_center, self.outter_center)] 

                x , z = side_starts[side]
                tran_vec = np.array([x, y, z])

                place_dir = [(1,0), (-1,0), (0,1), (0,-1)]
                dir_x, dir_z = place_dir[side]

                for i in range(self.n - 1):
                    
                    # translation vector - move cube block to correct postion
                    tran_vec += np.array([dir_x * (1 + self.block_interval_size), 0, dir_z * (1 + self.block_interval_size)])

                    temp = cube_block(self.render)
                    temp.translate(tran_vec)
                    self.cube_blocks.append(temp)


        for cube in self.cube_blocks:
            cube.get_center()


        self.model_cube_layers() # gets segments blocs

        # set up colours
        for ind, face in enumerate(self.face_blocs):
            for bloc in face:
                bloc.colors[ind] = self.face_colors[ind]

                bloc.new_colors()
     

if __name__ == '__main__':
    cube = rubix_cube(3)