import numpy as np

class rubix:
    """
    Handles rubix cube logic arround rotations 

    Colours:
        0 - White
        1 - Red
        2 - Green
        3 - Blue
        4 - Orange
        5 - Yellow

    Completed cube net:
        (for visualisation)
        -   -   -   -
        -   4   -   -
        2 . 0 . 3 . 5
        -   1   -   -
        -   -   -   -

    Cube rotations:
        xy - rotation parallel to 0 / 5 (white / yellow)
        xz - rotation parallel to 2 / 3 (green / blue)
        yz - rotation parallel to 1 / 4 (red / orange)

    """

    def __init__(self, n: int):

        self.n = n 

        self.sides = []
        for i in range(6):
            self.sides.append( np.repeat(i, self.n**2 ).reshape( self.n, self.n) )

        self.test_array = np.array( [[1, 2, 3],
                                     [4, 5, 6],
                                     [7, 8, 9]]
                                    )


    # rotation functions:
        # 'ind' refers to rubix cube layer to rotate 
        #  ind: int, 0 <=  ind  < n 

    def rotate_xy(self, ind: int):
        "Rubix cube rotation on xy"
        pass

    def rotate_xz(self, ind: int):
        "Rubix cube rotation on xz"
        pass

    def rotate_yz(self, ind: int):
        "Rubix cube rotation on yz"
        pass


    def rotate_array(self, array: nd.array, k: rot):
        "Rotates matrix arrays"
        return np.rot90(array, k = rot, axes = 90)


    

if __name__ == "__main__":
    cube_test = rubix(3)
    #print(cube_test.sides)


