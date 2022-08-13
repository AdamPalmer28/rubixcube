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

        self.intialise() # intialise cube blocs postions and colours

        # 6 faces centers 
        self.face_centers = np.array([(self.outter_center, 0, 0, 1), (-self.outter_center, 0, 0, 1),
                                        (0, self.outter_center, 0, 1), (0, -self.outter_center, 0, 1),
                                        (0, 0, self.outter_center, 1), (0, 0, -self.outter_center, 1),
                                    ])
        
        self.face_colors = ['blue','green','white','yellow','#b34c07','red']

        self.cam_dist = [0,0,0,0,0,0]

        self.model_cube_layers() # gets segments blocs

        for ind, face in enumerate(self.face_blocs):
            for bloc in face:
                #print(ind, bloc.get_center())
                bloc.colors[ind] = self.face_colors[ind]

                bloc.new_colors()
        

    # will be redundant after cube layers is finished
    def model_cube_faces(self):
        "Segements the blocks into cube model faces"

        # classify the blocks - only necessary after movement
        self.face_blocs = [[],[],[],[],[],[]] # intialise faces bloc var 

        for block in self.cube_blocks:
            bloc_pos = block.get_center()
            for ind, cord in enumerate(bloc_pos[:3]):
                # outter block detection
                if abs(cord) == self.outter_center:

                    ind = (2*ind + 1 if cord < 0 else 2*ind) # if negative assign to correct face
                    
                    self.face_blocs[ind].append(block)

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
                print(pos, i, layer_ind)
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

        # distances - calcs
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
        # self.model_cube_faces() # only necessary after rubix movement
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
            cube.draw(faces = self.visable_faces_ind)

    def rotate(self, axis, ind):
        "rotation for the cube model"
        passgit


    # only run at the start of the model
    def intialise(self):
        "Intialise the cube postions in the rubix cube along with the associated colours"

        self.cube_blocks = [] # all cube blocks

        # each list will have length n - n lists of blocks coresponding to each turnable section


        # Create cube objects
        self.outter_edge = self.n / 2 + (self.n - 1) / 2 * self.block_interval_size
        self.outter_center = self.outter_edge - 0.5 # assuming 0.5 = block size / 2

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
     

if __name__ == '__main__':
    cube = rubix_cube(3)