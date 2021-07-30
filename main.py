"""
main.py

TODO :
finish the pressure ball (start with a square)

issue : the shape 'explodes' : issue with unstable oscillations (good example with the triangle)
=> volume might be the issue

idea : to prevent crashing, a test at each frame could correct extreme behaviour

"""
from render2D import Render
from elements import *

renderObject = Render()

renderObject.addObject(SoftBall(
    Point(5, 2),  # Center point
    0.1,  # Total mass (kg)
    0.5,  # Ball radius (m)
    4,  # Number of points
    20.,  # spring stiffness
    0.2,  # spring damping coefficient
    0.5,  # Pressure coeff
    0.2))  # Pressure damping coeff

renderObject.start()