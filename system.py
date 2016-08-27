#!/usr/bin/env python

import math
from progressbar import ProgressBar

import os,pickle

GRAVCONSTANT = 1.993e-44

g_listOfObjects = []

class State:
	
  """Class representing position and velocity."""
  def __init__(self, x, y, z, vx, vy, vz):
    self._x, self._y, self._z, self._vx, self._vy, self._vz = x, y, z, vx, vy, vz

  def __repr__(self):
    return 'x:{x} y:{y} z:{z} vx:{vx} vy:{vy} vz:{vz}'.format(
      x=self._x, y=self._y, z=self._z, vx=self._vx, vy=self._vy, vz=self._vz)

class Derivative:
	
  """Class representing velocity and acceleration."""
  def __init__(self, dx, dy, dz, dvx, dvy, dvz):
    self._dx, self._dy, self._dz, self._dvx, self._dvy, self._dvz = dx, dy, dz, dvx, dvy, dvz

  def __repr__(self):
    return 'dx:{dx} dy:{dy} dz:{dz} dvx:{dvx} dvy:{dvy} dvz:{dvz}'.format(
      dx=self._dx, dy=self._dy, dz=self._dz, dvx=self._dvx, dvy=self._dvy, dvz=self._dvz)

class ObjectInSpace:
	
  def __init__(self, info):
    infoSplit = info.split('\n')
    self._n = infoSplit[0]
    self._st = State(eval(infoSplit[2]), eval(infoSplit[3]), eval(infoSplit[4]),
             eval(infoSplit[5]), eval(infoSplit[6]), eval(infoSplit[7]))
    self._m = eval(infoSplit[1])
    self._history = []

  def __repr__(self):
    return repr(self._st)

  def acceleration(self, state):
    """Calculate acceleration caused by other planets on this one."""
    ax = 0.0
    ay = 0.0
    az = 0.0
    for p in g_listOfObjects:
      if p is self:
        continue  # ignore ourselves
      dx = p._st._x - state._x
      dy = p._st._y - state._y
      dz = p._st._z - state._z
      dsq = dx*dx + dy*dy + dz*dz # distance squared
      dr = math.sqrt(dsq)  # distance
      force = GRAVCONSTANT*p._m/dsq
      # Accumulate acceleration...
      ax += force*dx/dr
      ay += force*dy/dr
      az += force*dz/dr
    return (ax, ay, az)

  def initialDerivative(self, state):
    """Part of Runge-Kutta method."""
    ax, ay, az = self.acceleration(state)
    return Derivative(state._vx, state._vy, state._vz, ax, ay, az)

  def nextDerivative(self, initialState, derivative, dt):
    """Part of Runge-Kutta method."""
    state = State(0., 0., 0., 0., 0., 0.)
    state._x = initialState._x + derivative._dx*dt
    state._y = initialState._y + derivative._dy*dt
    state._z = initialState._z + derivative._dz*dt
    state._vx = initialState._vx + derivative._dvx*dt
    state._vy = initialState._vy + derivative._dvy*dt
    state._vz = initialState._vz + derivative._dvz*dt
    ax, ay, az = self.acceleration(state)
    return Derivative(state._vx, state._vy, state._vz, ax, ay, az)

  def updatePlanet(self, dt):
    self._history.append(repr(self._st))
    k1 = self.initialDerivative(self._st)
    k2 = self.nextDerivative(self._st, a, dt*0.5)
    k3 = self.nextDerivative(self._st, b, dt*0.5)
    k4 = self.nextDerivative(self._st, c, dt)
    dxdt = 1.0/6.0 * (k1._dx + 2.0*(k2._dx + k3._dx) + k4._dx)
    dydt = 1.0/6.0 * (k1._dy + 2.0*(k2._dy + k3._dy) + k4._dy)
    dzdt = 1.0/6.0 * (k1._dz + 2.0*(k2._dz + k3._dz) + k4._dz)
    dvxdt = 1.0/6.0 * (k1._dvx + 2.0*(k2._dvx + k3._dvx) + k4._dvx)
    dvydt = 1.0/6.0 * (k1._dvy + 2.0*(k2._dvy + k3._dvy) + k4._dvy)
    dvzdt = 1.0/6.0 * (k1._dvz + 2.0*(k2._dvz + k3._dvz) + k4._dvz)
    self._st._x += dxdt*dt
    self._st._y += dydt*dt
    self._st._z += dzdt*dt
    self._st._vx += dvxdt*dt
    self._st._vy += dvydt*dt
    self._st._vz += dvzdt*dt

def main(n=1):

  global g_listOfObjects

  f = open('cartesian.txt', 'r')
  objInfos = f.read().split('\n\n')
  f.close()
  while '' in objInfos:
    objInfos.remove('')
  g_listOfObjects = []
  for info in objInfos:
    g_listOfObjects.append(ObjectInSpace(info))

  dt = 1.*24.*60.*60. * n

  pbar = ProgressBar()
  
  for i in pbar(range(int(365./n))):
    for p in g_listOfObjects:
      p.updatePlanet(dt)
  
  #write planet histories
  for planet in g_listOfObjects:
    f = open('coordinates/'+planet._n.replace("/",'')+'.txt', 'w')
    f.write('\n'.join(planet._history))
    f.close()

if __name__ == "__main__":
  main()
