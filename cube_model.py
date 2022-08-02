import numpy as np
from object3D import *
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

        self.face_colors = ['yellow','red','blue','white','green','orange']

        self.intialise() # intialise cube blocks and camera postion

        # 6 faces centers 
        self.face_centers = np.array([(self.outter_center, 0, 0, 1), (-self.outter_center, 0, 0, 1),
                                        (0, self.outter_center, 0, 1), (0, -self.outter_center, 0, 1),
                                        (0, 0, self.outter_center, 1), (0, 0, -self.outter_center, 1),
                                    ])
        
        self.cam_dist = [0,0,0,0,0,0]

        self.face_colors = ['yellow','red','blue','white','green','#b34c07']
        self.side_colors = [2,4,3,0,5,1]

        self.model_cube_faces() # gets camera distances and segments blocs
        for ind, face in enumerate(self.face_blocs):
            for bloc in face:
                color_ind = self.side_colors[ind]
                bloc.colors[color_ind] = self.face_colors[color_ind]
                
                bloc.new_colors()
        
        


    def intialise(self):
        "Intialise the cube postion and camera postion"

        self.cube_blocks = [] # all cube blocks

        # segment cubes into turnable section groups
        self.blocks_xy = [] # segments cube blocks into xy rows
        self.blocks_xz = [] # segments cube blocks into xz rows
        self.blocks_yz = [] # segments cube blocks into yz rows

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

    def model_cube_faces(self):
        "Segements the blocks into cube model faces, with associated distance to each face"

        # face distances
        for ind, face in enumerate(self.face_centers):
            dif = (face - self.camera.postion) # vector between camera and centre
            self.cam_dist[ind] = np.sqrt( (dif ** 2).sum() ) # update distance


        # classify the blocks
        self.face_blocs = [[],[],[],[],[],[]] # intialise faces bloc var 

        for block in self.cube_blocks:
            bloc_pos = block.get_center()
            for ind, cord in enumerate(bloc_pos[:3]):
                # outter block detection
                if abs(cord) == self.outter_center:

                    ind = (2*ind + 1 if cord < 0 else 2*ind) # if negative assign to correct face

                    self.face_blocs[ind].append(block)

                    


    def draw(self):
        # draws cube to screen
        self.model_cube_faces()


        face_dist = self.cam_dist.copy()
        face_dist.sort()
        min3 = face_dist[:3] # min 3 faces

        # visable_blocs
        self.vis_cubes = []
        for val in min3:
            ind = self.cam_dist.index(val)
            self.vis_cubes += self.face_blocs[ind]

        # calc dist
        self.d_cubes = {}
        for cube in self.vis_cubes:

            self.d_cubes[cube.distance()] = cube

        sorted_cubes_keys = sorted(self.d_cubes.keys(), reverse=True)
        self.vis_d_cubes =  {k: self.d_cubes[k] for k in  sorted_cubes_keys} 
        
        # draw cubes
        for dist, cube in self.vis_d_cubes.items():
            cube.draw()

        

