"""
render2D.py

Rendering class using pygame

"""
import pygame as pg
from elements import *
import sys
from typing import List
from time import time
from statistics import mean


# Default values that work well


# Screen size
SIZE_X, SIZE_Y = 640, 480
FPS = 30
SCALE = 100  # pixels per meter

# Colors :
blue = pg.Color(0, 0, 255)  # Shape color
white = pg.Color(255, 255, 255)  # Background color
red = pg.Color(255, 0, 0)  # Spring color
black = pg.Color(0, 0, 0)  # Normal vector color




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

        self.grabbed_object : Object = None  # Grabbed object whose point must be moved

        # Display spring, normal
        self.display_normal = False
        self.display_springs = False
        
        # Display max fps available based on frames computing time
        self.monitor_fps = False
        self.monitor_period = 1.  # (seconds) : time between each fps update

    
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

        pg.display.set_caption("Soft bodies simulator")

        start, new_time = 0., 0.  # Fps monitoring
        seconds = 0.
        time_counter = []  # Use mean() to get average frame time


        # Font to display fps :
        font = pg.font.SysFont(None, 24)  # Adjust font side if needed (here : 24 px)
        img = pg.Surface((0, 0))  # Initialize surface

        while True:
            

            # Get frame beginning time
            start = time()

            # Pygame event loop
            for event in pg.event.get():

                # QUIT events
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()   

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:  # left click

                        pos = pg.mouse.get_pos()  # cursor position in pixels

                        x,y = pixel_to_coord(pos, self.scale, self.ymax)
                        mouse_pos = Point(x, y)  # cursor pos in x,y float coordinates

                        # Set a point to be the "grabbed point"
                        # The "grabbed point" is ignored by its shape "update"
                        # It is only moved 

                        # Bring the closest object near the cursor
                        self.grabbed_object = self.getClosestObject(mouse_pos)
                        if self.grabbed_object is not None:

                            # The nearest point's state is changed to "grabbed point"
                            self.grabbed_object.grabNearestPoint(mouse_pos)
                    
                elif event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:  # Left click is released

                        # Release the grabbed point
                        self.grabbed_object.grabbed_point = None
                        self.grabbed_object = None
             

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.event.post(pg.event.Event(pg.QUIT))

                    # Change display normal vectors on pressing key A (qwerty -> q -> A key in azerty)
                    elif event.key == pg.K_q:
                        self.display_normal = not self.display_normal
                    # Display springs on pressing key Z (azerty Z is qwerty w)
                    elif event.key == pg.K_w:
                        self.display_springs = not self.display_springs
                    # Display max available fps (updated every second)
                    elif event.key == pg.K_e:
                        self.monitor_fps = not self.monitor_fps
                        seconds = time()  # Reset time passed
                        time_counter = []  # Reset time counter

            # Process the grabbed point:
            if self.grabbed_object is not None:
                
                # Mouse position :
                pos = pg.mouse.get_pos()  # cursor position in pixels

                x,y = pixel_to_coord(pos, self.scale, self.ymax)
                mouse_pos = Point(x, y)  # cursor pos in x,y float coordinates

                self.grabbed_object.computeGrabbedPoint(mouse_pos, self.dt)


            # Clear screen
            window.fill(white)

            # Update the objects physics and then render them on the screen
            for obj in self.objectList:

                obj.update(self.dt)

                obj.compute_container_box_collision(self.xmin, self.xmax, self.ymin, self.ymax)

                pg.draw.polygon(window, blue, rescale(obj.point_coordinates(), self.scale, self.size_y))


                if self.display_normal:
                    # Displaying normal vectors (on top of the shape)
                    for i in range(len(obj.points)):

                        pt1, pt2 = obj.points[i].pos, obj.points[(i+1)%len(obj.points)].pos

                        # Center position of each side
                        center = (pt1 + pt2)/2

                        # Point in the side's normal direction, 1 meter farther
                        normal_point = center + normal(pt1, pt2)

                        # 2D x,y coordinates to position on screen
                        center, normal_point = rescale((center, normal_point), self.scale, self.size_y)

                        # Drawing the 1 meter long vector
                        pg.draw.line(window, black, center, normal_point)
                

                if isinstance(obj, SoftObject) and self.display_springs:  # Has springs & display

                    for spring in obj.springs:

                        # Get the coordinates of the spring's edge points
                        pt1, pt2 = obj.points[spring.i1].pos, obj.points[spring.i2].pos

                        # Rescale them to the screen display size
                        pt1, pt2 = rescale((pt1, pt2), self.scale, self.size_y)

                        # Draw spring :
                        pg.draw.line(window, red, pt1, pt2, 2)  # Line size = 2 : thicker

            # Display available fps
            if self.monitor_fps:
                
                new_time = time()
                # Update counter
                time_counter.append(new_time - start)

                if seconds + self.monitor_period < new_time:
                    seconds += self.monitor_period

                    # Display fps
                    img = font.render("Available FPS : " + str(int(1/mean(time_counter))), True, black)

                    # Reset counter:
                    time_counter = []

                # Each loop : display fps
                window.blit(img, (0, 0))  # Print the fps in the top left corner
                    
 
            # Update screen and monitor fps   
            pg.display.update()
            fpsClock.tick(self.fps)