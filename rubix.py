import numpy as np
import copy

class rubix_logic:
    """
    Handles rubix cube logic - specifically rotations

    Colours:
        0 - White
        1 - Red
        2 - Green
        3 - Blue
        4 - Orange
        5 - Yellow

    Completed cube net:
        (with array direction)
        - -   - -   - -   - -
        - -   4 v   - -   - -
        2 <   0 <   3 <   5 <
        - -   1 ^   - -   - -
        - -   - -   - -   - -  

    Cube rotations:
        xy - rotation parallel to 0 / 5 (white / yellow)
        xz - rotation parallel to 2 / 3 (green / blue)
        yz - rotation parallel to 1 / 4 (red / orange)

    """

    def __init__(self, n: int):

        self.n = n 
        self.max_ind = self.n - 1
        
        self.cube = np.array( [
            np.repeat(0, self.n**2 ).reshape( self.n, self.n ),
            np.repeat(1, self.n**2 ).reshape( self.n, self.n ),
            np.repeat(2, self.n**2 ).reshape( self.n, self.n ),
            np.repeat(3, self.n**2 ).reshape( self.n, self.n ),
            np.repeat(4, self.n**2 ).reshape( self.n, self.n ),
            np.repeat(5, self.n**2 ).reshape( self.n, self.n )
            ] )
        
  
    # rotation functions:
        # 'ind' refers to rubix cube layer to rotate 
        #  ind: int, 0 <=  ind  < n 

    def rotate_xy(self, ind: int):
        "Rubix cube rotation on xy"
        # 1,3,4,2 (rotation order)
            
        # primary rotation
        array_copy = copy.copy(self.cube) # before rotation
        
            # rotate - change array layers (refer to cube neeting)
        self.cube[1][ind] =  array_copy[2][ind]
        self.cube[3][ind] =  array_copy[1][ind]
        self.cube[4][self.max_ind - ind] =  array_copy[3][ind][::-1]  
        self.cube[2][ind] =  array_copy[4][self.max_ind - ind][::-1]  
        
        # rotate sides (parallel sides)
        if ind == 0:
            self.cube[0] = np.rot90(self.cube[0])
        elif ind == self.n - 1:
            self.cube[5] = np.rot90(self.cube[5], k = -1)
            
       

    def rotate_xz(self, ind: int):
        "Rubix cube rotation on xz"
        # 1,0,4,5 (rotation order)
        
        # primary rotation
        array_copy = copy.copy(self.cube) # before rotation
        
            # rotate - change array layers (refer to cube neeting)
        self.cube[1][:,ind] =  array_copy[5][:,ind]
        self.cube[0][:,ind] =  array_copy[1][:,ind]
        self.cube[4][:,ind] =  array_copy[0][:,ind]
        self.cube[5][:,ind] =  array_copy[4][:,ind] 
        
        # rotate sides (parallel sides)
        if ind == 0:
            self.cube[2] = np.rot90(self.cube[2])
        elif ind == self.n - 1:
            self.cube[3] = np.rot90(self.cube[3], k = -1)
        

    def rotate_yz(self, ind: int):
        "Rubix cube rotation on yz"
        # 0,3,5,2 (rotation order)
        
        # primary rotation
        array_copy = copy.copy(self.cube) # before rotation
        
            # rotate - change array layers (refer to cube neeting)
        self.cube[0][ind] =  array_copy[2][:, ind][::-1] 
        self.cube[3][:, self.max_ind - ind] =  array_copy[0][ind] 
        self.cube[5][self.max_ind - ind] =  array_copy[3][:, self.max_ind - ind][::-1] 
        self.cube[2][:,  ind] =  array_copy[5][self.max_ind - ind] 
        
        # rotate sides (parallel sides)
        if ind == 0:
            self.cube[4] = np.rot90(self.cube[4])
        elif ind == self.n - 1:
            self.cube[1] = np.rot90(self.cube[1], k = -1)
            



if __name__ == "__main__":
    cube = rubix_logic(3)
    
    cube.rotate_xz(2)
    cube.rotate_xy(0)
    cube.rotate_yz(2)
    cube.rotate_yz(2)
    print(cube.cube)


