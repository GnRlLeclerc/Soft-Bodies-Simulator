"""
main.py


# TODO : max fps mode : to test the limits of the rendering engine, and stiffer structures
(display fps too)
# TODO : take collisions between shapes into account

"""
from render2D import Render
from elements import *

renderObject = Render(fps=100)



renderObject.addObject(SoftBall(
    Point(4, 1),  # Center point
    1,  # Total mass (kg)
    0.5,  # Ball radius (m)
    50,  # Number of points
    100,  # spring stiffness
    0.2,  # spring damping coefficient
    100,  # Pressure coeff
    0.2)  # Pressure damping coeff

)


renderObject.start()



"""
Working presets :
# If shape is unstable, increase inertia by increasing mass
# this means that the k / m ratio cannot exceed a certain value because
# of sampling effect. Python might be too slow in order to be able to
# increase FPS

# A water-drop-like ball. There are still issues with grabbing the shape, as it creates
# a stress on the shape that is too high to be stable
SoftBall(
    Point(4, 1),  # Center point
    5,  # Total mass (kg)
    0.5,  # Ball radius (m)
    50,  # Number of points
    40,  # spring stiffness
    0.1,  # spring damping coefficient
    60,  # Pressure coeff
    0.2)  # Pressure damping coeff


# A soft polygon, less glitchy than the previous preset
SoftBall(
    Point(4, 1),  # Center point
    1,  # Total mass (kg)
    0.5,  # Ball radius (m)
    10,  # Number of points
    40,  # spring stiffness
    0.1,  # spring damping coefficient
    60,  # Pressure coeff
    0.2)  # Pressure damping coeff


# A jelly like square. kd = 0.05 for a much springier box
SpringyBox(
    Point(2, 2),  # Starting position
    0.1,  # Total mass  
    0.5,  # Radius
    7,  # k
    0.2)  # kd


# A vertical block of jelly
SpringyStructure(
    Point(1, 1),
    1.,
    0.5,
    2,
    3,
    30,
    0.2
)
# Issue : with 30 FPS, k cannot be raised too much, else the shape is unstable

# Same shape, with 100 fps instead of 30 (else, unstable)
SpringyStructure(
    Point(1, 1),
    1.,
    0.5,
    2,
    3,
    50,
    0.4
)

# Same SoftBall with 100 fps : stiffness can be increased, and the result is much better
SoftBall(
    Point(4, 1),  # Center point
    1,  # Total mass (kg)
    0.5,  # Ball radius (m)
    50,  # Number of points
    100,  # spring stiffness
    0.2,  # spring damping coefficient
    100,  # Pressure coeff
    0.2)  # Pressure damping coeff

)


"""