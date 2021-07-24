"""
main.py

test modules
"""
from render2D import Render
from elements import *

renderObject = Render()

renderObject.addObject(SoftBall(Point(1, 1), 0.1, 0.5, 3, 10, 0.1, 0))

renderObject.start()