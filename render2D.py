"""
render2D.py

Rendering class using pygame

"""
import pygame as pg
from elements import *
import sys
from typing import List


# Default values that work well


# Screen size
SIZE_X, SIZE_Y = 640, 480
FPS = 30
SCALE = 100  # pixels per meter

# Colors :
blue = pg.Color(0, 0, 255)  # Shape color
white = pg.Color(255, 255, 255)  # Background color


class Render:
    """Render class:
    
    Contains all necessary information and methods in order to render the simulation
    """
    def __init__(self, fps : int=FPS, size_x : int=SIZE_X, size_y : int=SIZE_Y, scale : int=SCALE):

        self.fps = fps
        self.dt = 1/fps  # Simulation time step

        # Screen size : pixel number along x,y axis
        self.size_x = size_x
        self.size_y = size_y
        self.scale = scale  # Pixels per meter

        # x,y axis maximum
        self.xmax = size_x / scale
        self.ymax = size_y / scale

        self.xmin, self.ymin = 0., 0.  # Default minimum is zero : simplest option

        self.objectList : List[Object] = []  # Empty object list

    
    def setBoundaries(self, xmax : float, ymax : float):
        """Set container box boundaries, limited by screen size"""
        
        scale_x = self.size_x // xmax
        scale_y = self.size_y // ymax

        # In order to fit both axis, even though they might not have the same dimensions
        # as the screen, the minimum scale must be picked
        self.scale = min(scale_x, scale_y)


    def addObject(self, object : Object):
        """Add an object before starting simulation"""
        self.objectList.append(object)


    def getClosestObject(self, point : Point) -> Object:
        """
        Get the object which is the closest to the point
        (using barycentre)
        """
        
        if len(self.objectList) == 0:
            return None
        else:
            distances = [norm(point.pos - object.barycentre().pos) for object in self.objectList]

            index = distances.index(min(distances))

            return self.objectList[index] 
            

    def start(self):
        """Start the simulation"""
        
        pg.init()  # Initialize pygame
        fpsClock = pg.time.Clock()  # Monitor fps

        # Screen parameters :
        window = pg.display.set_mode((self.size_x, self.size_y))

        while True:
            
            # Pygame event loop
            for event in pg.event.get():

                # QUIT events
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()              
             
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.event.post(pg.event.Event(pg.QUIT))

            # Out of event loop : grab shapes

            if pg.mouse.get_pressed()[0]:  # left click detected / held pressed

                pos = pg.mouse.get_pos()  # cursor pos in pixels

                x,y = pixel_to_coord(pos, self.scale, self.ymax)
                mouse_pos = Point(x, y)  # cursor pos in x,y float coordinates

                # Bring the closest object near the cursor
                closest_obj = self.getClosestObject(mouse_pos)
                if closest_obj is not None:

                    closest_obj.grabNearestPoint(mouse_pos, self.dt)

            # Clear screen
            window.fill(white)

            # Update the objects physics and then render them on the screen
            for object in self.objectList:

                object.update(self.dt)

                object.compute_container_box_collision(self.xmin, self.xmax, self.ymin, self.ymax)

                pg.draw.polygon(window, blue, rescale(object.point_coordinates(), self.scale, self.size_y))
 
            # Update screen and monitor fps   
            pg.display.update()
            fpsClock.tick(self.fps)