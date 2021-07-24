"""
Useful small functions to commpute norms, unit vectors, normal vectors...
"""
import numpy as np
from typing import List


# Useful functions for calculations on 2D coordinates
def norm(vect : np.array) -> float:

    return np.sqrt(np.dot(vect, vect))


def unit_vector(vect : np.array) -> np.array:

    return vect / norm(vect)


def normal(vec1 : np.array, vec2 : np.array):
    """Returns a vector normal to vec1->vec2 so that
    vec1->vec2, normal, z define a direct 3D base
    
    For a ball object : 
    * points are listed in the positive rotation direction -> this returns an ext normal
    * points are listed in the negative rotation direction -> this returns an in normal
    """
    vec = unit_vector(vec2 - vec1)

    return np.array([vec[1], -vec[0]])


def rescale(coordinates : List[np.array], scale : int, size_y : int):
    """
    Rescales a list of (x,y) coordinates from an object
    into a list of pixel coordinates
    The y axis change in direction is also taken into account
    """
    return [(int(point[0]*scale), size_y - int(point[1]*scale)) for point in coordinates]
    

