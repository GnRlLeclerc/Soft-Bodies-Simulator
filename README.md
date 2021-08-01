# Soft-Bodies-Simulator
2D soft boy simulation using pygame, numpy

---SETUP---
Made in python 3.7.3 64-bit
Modules used : pygame, numpy, and built-in modules

---GUIDE---
The code is documented

Example setups are provided in main.py

Interacting with the simulation :

-> right-click to pick up the closest point to the cursor and move a shape

-> keys (AZERTY)
- A : show normal vectors (only recommended for SoftBall objects, not well implemented for Springy Boxes and Structures)
- Z : show springs (in red)
- E : show max FPS available. Based on each frames' computing time, displays the maximum fps available. Refreshes every second
If the specified fps is too high, the simulation will run slower, but at the specified time step (1/fps) for Euler integration.
Better fps improves stability and enables higher force coefficients with lighter masses (else, unstable oscillations can occur)

---PHYSICS---

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
P = pressure_coeff * (1/current_surface - 1/rest_surface)

pressure_coeff : P = nRT/V => pressure_coeff = total energy of the gaz particle model.
When pressure_coeff is increased, the particle's energy is increased with the external pressure (total energy/rest volume). The result is a less compressible particle

pressure dampening coefficient : in order to dissipate energy, a dampening force proportionnal to each point's relative velocity to the barycentre is applied. It is linked to the particle's internal viscosity

F/S = visc * dv/dx
F = visc * dv.dx * S = visc * rel_velocity * S/dx
=> pressure_dampening_coeff = viscosity * distance_between_barycentre_and_point = viscosity * radius

In reality, pressures are scalar fields in volume that apply forces to surfaces
In this 2D engine, pressures are scalar fields in shape surfaces that apply forces to the lines that make up the outline of a shape.

Pressure model : in a perfect gas : P*V = n*R*T, so P = constant / V
Hence why in this model, pressure is proportional to 1/V, or 1/surface in 2D.

the object_stiffness coefficient describes the compressibility of the object.

A pressure force is applied to each pair of point that are part of an object's outline, in the direction normal to the outline. The pressure force is shared by both points, who are both affected by half the force.

A pressure damping force also needs to be applied to reduce oscillations between opposing points that are not
linked by any spring. This force works like a spring damping force between every point and the shape's barycentre.

All of theses forces, along with gravity, are integrated in real time using Euler integration.

Remarks :
- the engine can be unstable if the coefficients entered are too great : because of numeric integration with a finite time step, stiffness and dampening coefficients that are too high create unstable oscillations and abrupt changes in position. They must be avoided for the engine to work correctly. The main.py file provides a working example with reasonable coefficients.

