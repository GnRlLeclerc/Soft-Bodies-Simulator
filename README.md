# 2D-physics-engine

2D simulation using pygame, numpy

soft bodies and hard bodies simulations:
springs, pressure forces...

The different objects are generated inside a box the size of the window.

ELements of an object :
- points with the same mass : the sum of the masses of an object's points is the object's mass
- springs that link different points. (for soft objects)
- internal pressure force, that simulates an object's elasticity in a way that cannot be reproduced with springs

Forces applied to points and Euler integration

- Springs : 3 paramaters : l0, k, kd
l0 : rest length of the spring
k : stiffness coefficient of the srping
kd : dampening coefficient, in order to avoid infinite oscillations

F = k * (length - l0)  # spring elastic force
Fk = kd * d(length)/dt = kd * spring_points_relative_speed  # dampening force

- Pressure (not yet finished)
An object can be subject to a pressure force :
P = object_stiffness * (1/current_surface - 1/rest_surface)

In reality, pressures are scalar fields in volume that apply forces to surfaces
In this 2D engine, pressures are scalar fields in shape surfaces that apply forces to the lines that make up the outline of a shape.

Pressure model : in a perfect gas : P*V = n*R*T, so P = constant / V
Hence why in this model, pressure is proportional to 1/V, or 1/surface in 2D.

the object_stiffness coefficient describes the compressibility of the object.

A pressure force is applied to each pair of point that are part of an object's outline, in the direction normal to the outline. The pressure force is shared by both points, who are both affected by half the force.

A pressure damping force also needs to be applied to reduce oscillations between opposing points that are not
linked by any spring. This force works like a spring damping force between every point and the shape's barycentre.

TODO : identify the physical meaning of "pressure_coeff" and maybe "pressure_damping_coeff" also.

All of theses forces, along with gravity, are integrated in real time using Euler integration.

Remarks :
- the engine can be unstable if the coefficients entered are too great : because of numeric integration with a finite time step, stiffness and dampening coefficients that are too high create unstable oscillations and abrupt changes in position. They must be avoided for the engine to work correctly. The main.py file provides a working example with reasonable coefficients.

