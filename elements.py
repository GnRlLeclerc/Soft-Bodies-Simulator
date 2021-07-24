"""
elements.py

Basic classes of elements that are used in the 2D engine
"""
import numpy as np
from typing import List  # type hints for lists

from math_func import * 

class Point:
    """Basic 2D coordinates container
    
    pos : x, y : 2D coordinates
    m : mass (kg)
    v : vx, vy : 2D velocity vector coordinates
    f : fx, fy : 2D force vector coordinates

    Can also be used to return x,y coordinates
    np.array are simpler to use for Euler integration method
    x(), y() methods are still implemented for simplification
    """

    def __init__(self, x : float, y : float, m : float=0):
        
        self.pos = np.array([x, y])
        self.v = np.array([0, 0])
        self.f = np.array([0, 0])

        self.m = m

    def x(self) -> float:
        return self.pos[0]

    def y(self) -> float:
        return self.pos[1]



class Spring:
    """Spring class
    
    i1, i2 : Point id in the Object that contains the spring
    l0 : rest length (m), equal to the distance between pt1 & pt2 at rest (initially)
    k : spring stiffness (N/m)
    kd : spring damping (N/v)
    """

    def __init__(self, i1 : int, i2 : int, l0 : float, k : float, kd : float):
        
        self.i1 = i1
        self.i2 = i2
        self.l0 = l0
        self.k = k
        self.kd = kd


class Object:
    """Object class
    
    Base class of any object that is rendered in the 2D engine :
    Contains a list of points in the direct order of rotation
    (better in order to compute normal ext vectors)
    Contains helful methods for other classes that inherit from it
    """

    def __init__(self, points : List[Point]):

        self.points = points  # Points list

    def barycentre(self) -> Point:
        """returns the x,y coordinates of the center point"""

        x = sum([point.x for point in self.points])
        y = sum([point.y for point in self.points])

        n = len(self.points)

        return Point(x/n, y/n)


    def boundingBox(self) -> List[Point]:
        """Returns the bounding box of the object :
        (pt1, pt2)
        pt1 : point with the lowest x,y coordinates
        pt2 : point with the highest x,y coordinates
        """
        x = [point.x for point in self.points]
        y = [point.y for point in self.points]

        return Point(min(x), min(y)), Point(max(x), max(y))

        
    def isInBoundingBox(self, point : Point) -> bool:
        
        pt1, pt2 = self.boundingBox()

        if point.x > pt2.x or point.y > pt2.y or point.x < pt1.x or point.y < pt1.y:
            return False
        return True


    def nearest(self, point : Point) -> int:
        """point must be in the bounding box
        returns the index of the object's nearest point to point
        """

        assert self.isInBoundingBox(point)  # DEBUG purposes

        lengths = [norm(point.pos - pt.pos) for pt in self.points]

        return lengths.index(min(lengths))


    def reset_forces(self):
        """Sets all points forces to 0 before physics processing"""
        
        for point in self.points:

            point.f = np.array([0., 0.])


    def update(self):
        """Updates forces, velocities, and point positions"""
        pass


    def surface(self) -> float:
        """Returns the surface of the object
        Depending on whether the points order is direct or not, S
        will be positive or negative. To handle both cases : abs
        """

        S = 0
        pt_count = len(self.points)

        for i in range(pt_count):

            pt1 = self.points[i]
            pt2 = self.points[(i+1)%pt_count]

            # Surface of a trapèze
            S += (pt2.y + pt1.y) * (pt2.x - pt1.x) / 2

        return abs(S)


class SoftObject(Object):
    """Soft Object class
    
    Contains springs, and a method to take their forces into account
    """


    def __init__(self, points : List[Point], springs : List[Spring]=[]):
        super().__init__(points)

        self.springs = springs


    def addSpring(self, spring : Spring):

        self.springs.append(spring)


    def setSprings(self):
        """Method to automatically set the spring setup of the object
        It varies according to the type of SoftObject : soft ball, springy structure...
        """
        pass


    def spring_forces(self):
        """Called during update()
        
        Calculates spring forces on every single point of the SoftObject
        self.reset_forces() must be called beforehand
        """
        for spring in self.springs:

            pt1 = self.points[spring.i1]
            pt2 = self.points[spring.i2]

            spring_vector = unit_vector(pt2.pos - pt1.pos)  # from pt1 to pt2
            f = 0.  # f * spring_vector is the force vector applied on pt1

            # Spring force
            spring_length = norm(pt1.pos - pt2.pos)

            f = spring.k * (spring_length - spring.l0)

            # Damping force
            rel_velocity = pt2.v - pt1.v  # velocity vector, to be projected on spring_vector

            f += np.dot(rel_velocity, spring_vector) * spring.kd

            # Update forces :
            self.points[spring.i1].f += f * spring_vector
            self.points[spring.i2].f -= f * spring_vector


class SoftBall(SoftObject):
    """Soft ball class
    
    A ball with springs along the side, and an internal pressure force

    Parameters :
    m : mass (kg)
    r :  radius (m)
    n : number of points

    the mass is shared between each point
    """

    def __init__(self, pos : Point, m : float, r : float, n : int, k : float, kd : float, pressure_coeff : float):

        # Creating point list
        shared_mass = m / n
        points = [Point(pt.x + pos.x, pt.y + pos.y, shared_mass) for pt in self.init_ball_coordinates(r, n)]

        # Creating spring list
        springs = []
        for i in range(n):
            springs.append(Spring(i, (i+1)%n, norm(points[(i+1)%n].pos - points[i].pos), k, kd))

        # Initialize base SoftObject class
        super().__init__(points, springs)

        # TODO : initialize pressure, and define a pressure calculation function

        self.S0 = self.surface()  # initial surface
        self.pressure_coeff = pressure_coeff

        # pressure force : line_length * (1/V - 1/V0) * stiffness_coeff


    def init_ball_coordinates(r : float, n : int) -> List[Point]:
        """Returns points coordinate that make a circle around the origin"""

        points = []
        for i in range(n):

            points.append(Point(r * np.cos(2*np.pi*i/n), r * np.sin(2*np.pi*i/n)))

        return points

    def pressure_forces(self):
        """Calculate pressure forces on the side points"""
        pass


        

