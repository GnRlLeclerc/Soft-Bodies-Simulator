"""
render2D.py

Rendering class using pygame

"""
import pygame as pg
from elements import *


# Default values that work well
DT = 0.1
XMIN, XMAX = -5., 5.
YMIN, YMAX = -2., 10.
# and more...


# Screen size
SIZE_X, SIZE_Y = 640, 480
FPS = 30

# Colors :
blue = pg.Color(0, 0, 255)  # Shape color


class Render:
    """Render class:
    
    Contains all necessary information and methods in order to render the simulation
    """
    def __init__(self, dt : float=DT, xmin : float=XMIN, xmax : float=XMAX, ymin : float=YMIN, ymax : float=YMAX):
        
        self.dt = dt
        self.xmin, self.xmax = xmin, xmax
        self.ymin, self.ymax = ymin, ymax

    
    def setBoundaries(self, xmin : float, xmax : float, ymin : float, ymax : float):
        """Set container box boundaries"""
        self.xmin, self.xmax = xmin, xmax
        self.ymin, self.ymax = ymin, ymax
        

    def start(self):
        """Start the simulation"""
        
        pg.init()  # Initialize pygame
        fpsClock = pg.time.Clock()  # Monitor fps

        # Screen parameters :
        window = pg.display.set_mode((SIZE_X, SIZE_Y))

        # TODO : ready to loop