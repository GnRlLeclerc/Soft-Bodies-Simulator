"""
elements.py

Basic classes of elements that are used in the 2D engine

Global variables : dt
TODO : il faudrait une sorte de classe bien plus générale qui contient dt
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
        self.v = np.array([0., 0.])  # IMPORTANT : type must be float
        self.f = np.array([0., 0.])

        self.m = m

    @property  # call function without brackets
    def x(self) -> float:
        return self.pos[0]

    @property
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
        """Checks if given point is in the Object's bouding box
        in order to limit complexity and avoid calling self.isIn each time
        """

        pt1, pt2 = self.boundingBox()

        if point.x > pt2.x or point.y > pt2.y or point.x < pt1.x or point.y < pt1.y:
            return False
        return True


    def isIn(self, point : Point) -> bool:
        """Checks if given point is inside the object
        Method used : 
        if the given point is inside the object, any vector going from this
        point to any point of the object will have a positive dot product
        with the vector going from the barycentre to the given point        
        """
        barycentre_vec = point.pos - self.barycentre().pos

        for pt in self.points:

            pt_vec = pt.pos - point.pos

            if np.dot(barycentre_vec, pt_vec) < 0:
                return False
        
        return True  # By default, if no negative dot product has been found

    # TODO : method that gives the closest coordinates that are out of the Object
    # if a point is inside : could be used to compute a collision and avoid the
    # merging of two objects

    def grabNearestPoint(self, point : Point, dt : float):
        """
        Grabs the object's point which is nearest to point, and
        applies an immediate change of position with a specific velocity
        in order to "grab" the object with a mouse click
        """
        # Get nearest point index :
        distances = [norm(point.pos - pt.pos) for pt in self.points]
        i = distances.index(min(distances))

        # Compute a velocity that scales with distance, in order to bring the object
        # closer to the mouse cursor quickly
        pt = self.points[i]
        velocity = (point.pos - pt.pos) / pt.m  # Directly proportionnal to the distance

        # Update position
        pt.pos += velocity * dt


    def reset_forces(self):
        """Sets all points forces to 0 before physics processing"""
        
        for point in self.points:

            point.f = np.array([0., 0.])


    def update(self, dt : float):
        """CALL AT EACH LOOP ITERATION : 
        Updates forces, velocities, and point positions"""
        pass


    def update_points(self, dt : float):
        """Updates the velocity and position of each point based on the forces applied on them
        Euler's integration method
        """

        for point in self.points:
            point.v += point.f * dt / point.m
            point.pos += point.v * dt


    def compute_container_box_collision(self, xmin : float, xmax : float, ymin : float, ymax : float):
        """Computes the collisions with the box that contains all Objects
        Solid contact : if there is a contact :
        * tangent velocity = 0
        * normal velocity *= -1
        """
        for point in self.points:

            
            if point.y < ymin:
                point.pos[1] = ymin
                point.v *= -1.  # invert velocity direction
                point.v[0] = 0.  # void tangent velocity

            elif point.x > xmax:
                point.pos[0] = xmax
                point.v *= -1.  # invert velocity direction
                point.v[1] = 0.  # void tangent velocity

            elif point.x < xmin:
                point.pos[0] = xmin
                point.v *= -1.
                point.v[1] = 0.

            elif point.y > ymax:
                point.pos[1] = ymax
                point.v *= -1.
                point.v[0] = 0.


    def surface(self) -> float:
        """Returns the surface of the object
        Depending on whether the rotation direction of the points
        is positive or not, S will be positive or negative.
        To handle both cases : abs
        """

        S = 0
        pt_count = len(self.points)

        for i in range(pt_count):

            pt1 = self.points[i]
            pt2 = self.points[(i+1)%pt_count]

            # Surface of a trapèze
            S += (pt2.y + pt1.y) * (pt2.x - pt1.x) / 2

        return abs(S)


    def point_coordinates(self) -> List[np.array]:
        """Returns a list [(x,y), (x,y)] of the coordinates of every point
        of the shape, ready to use for pygame.draw.polygon(window, color, points)
        """
        return [ point.pos for point in self.points]

    def gravity_forces(self, g : float=9.81):
        """Compute gravity forces for each point
        g = 9.81 m/s² : gravity acceleration
        """

        for point in self.points:

            point.f += np.array([0, -g * point.m])


class SoftObject(Object):
    """Soft Object class
    
    Contains springs, and a method to take their forces into account
    """


    def __init__(self, points : List[Point], springs : List[Spring]=[]):
        super().__init__(points)

        self.springs = springs


    def addSpring(self, spring : Spring):

        self.springs.append(spring)


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
            pt1.f += f * spring_vector
            pt2.f -= f * spring_vector

            # pt1 is self.points[spring.i1] -> True. pt1, pt2 are references


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


    def init_ball_coordinates(self, r : float, n : int) -> List[Point]:
        """Returns points coordinate that make a circle around the origin"""

        points = []
        for i in range(n):

            points.append(Point(r * np.cos(2*np.pi*i/n), r * np.sin(2*np.pi*i/n)))

        return points

    def pressure_forces(self):
        """Calculate pressure forces on the side points of the Object"""
        
        # Pressure to apply on every line of the Object
        P = self.pressure_coeff * (1/self.surface() - 1/self.S0)

        n = len(self.points)
        for i in range(n):

            pt1 = self.points[i]
            pt2 = self.points[(i+1)%n]

            # Remark : in SoftBall, the points are listed in the positive direction of...
            # ...rotation : normal() will return a normal vector pointing inwards

            ext_vector = - normal(pt1.pos, pt2.pos)
            side_length = norm(pt1.pos - pt2.pos)

            F = side_length * P * ext_vector

            # The pressure force is shared between the 2 points

            pt1.f += F / 2
            pt2.f += F / 2


    def update(self, dt : float):
        """
        Update the physics of the object over a dt time-step
        """
        
        # Update forces

        # Reset point forces to 0.
        self.reset_forces()
        
        # Calculate forces
        self.spring_forces()
        self.pressure_forces()
        self.gravity_forces()

        # Update velocity and position for each point
        self.update_points(dt)

        # Do not forget to then call collision detection methods!


class SpringyBox(SoftObject):
    """Spring box : jello-like appearance, only springs
    
    TODO : how to build structures made out of small cubes?
    """

    def __init__(self, pos : Point, m : float, r : float, n : int, k : float, kd : float):


        # TODO
        points = []
        springs = []

        super().__init__(points, springs=springs)



