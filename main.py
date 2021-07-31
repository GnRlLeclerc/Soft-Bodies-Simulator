"""
main.py

"""
from render2D import Render
from elements import *

renderObject = Render()

renderObject.addObject(SpringyBox(
    Point(2, 2),  # Starting position
    0.1,  # Total mass  
    0.5,  # Radius
    7,  # k
    0.2)  # kd
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


# A jelly like square
SpringyBox(
    Point(2, 2),  # Starting position
    0.1,  # Total mass  
    0.5,  # Radius
    7,  # k
    0.2)  # kd

"""