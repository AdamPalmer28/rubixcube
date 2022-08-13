"""
Matrices operations for the objects in our 3D space
"""
import numpy as np

def rotate_xy(angle: float=0) -> np.array:
    "Rotation of angle in x-y plane, 3rd entry remains the same"
    return np.array([
                [np.cos(angle),np.sin(angle),0,0],
                [-np.sin(angle),np.cos(angle),0,0],
                [0,0,1,0],
                [0,0,0,1]
                    ]) 

def rotate_xz(angle: float=0) -> np.array:
    "Rotation of angle in x-z plane, 2nd entry remains the same"
    return np.array([
                [np.cos(angle),0,np.sin(angle),0],
                [0,1,0,0],
                [-np.sin(angle),0,np.cos(angle),0],
                [0,0,0,1]
                    ]) 

def rotate_yz(angle: float=0) -> np.array:
    "Rotation of angle in y-z plane, 1st entry remains the same"
    return np.array([
                [1,0,0,0],
                [0,np.cos(angle),np.sin(angle),0],
                [0,-np.sin(angle),np.cos(angle),0],
                [0,0,0,1]
                    ])

def scale(n: float=1) -> np.array:
    "Scalar matrix"
    return np.array([
                [n,0,0,0],
                [0,n,0,0],
                [0,0,n,0],
                [0,0,0,1]
                    ])

def translate(x: float=0, y: float=0, z: float=0) -> np.array:
    "Translation matrix"
    return np.array([
                [1,0,0,0],
                [0,1,0,0],
                [0,0,1,0],
                [x,y,z,1]
                    ])