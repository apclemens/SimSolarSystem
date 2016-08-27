#!/usr/bin/env python

import sys
import math
import pygame
import random
from collections import defaultdict
from progressbar import ProgressBar

import os
import psutil,pickle

GRAVCONSTANT = 1.993e-44

g_listOfPlanets = []


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


class Planet:
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
		for p in g_listOfPlanets:
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
		"""Runge-Kutta 4th order solution to update planet's pos/vel."""
		a = self.initialDerivative(self._st)
		b = self.nextDerivative(self._st, a, dt*0.5)
		c = self.nextDerivative(self._st, b, dt*0.5)
		d = self.nextDerivative(self._st, c, dt)
		dxdt = 1.0/6.0 * (a._dx + 2.0*(b._dx + c._dx) + d._dx)
		dydt = 1.0/6.0 * (a._dy + 2.0*(b._dy + c._dy) + d._dy)
		dzdt = 1.0/6.0 * (a._dz + 2.0*(b._dz + c._dz) + d._dz)
		dvxdt = 1.0/6.0 * (a._dvx + 2.0*(b._dvx + c._dvx) + d._dvx)
		dvydt = 1.0/6.0 * (a._dvy + 2.0*(b._dvy + c._dvy) + d._dvy)
		dvzdt = 1.0/6.0 * (a._dvz + 2.0*(b._dvz + c._dvz) + d._dvz)
		self._st._x += dxdt*dt
		self._st._y += dydt*dt
		self._st._z += dzdt*dt
		self._st._vx += dvxdt*dt
		self._st._vy += dvydt*dt
		self._st._vz += dvzdt*dt

def main(n=1):

	global g_listOfPlanets
	pid = os.getpid()
	py = psutil.Process(pid)
	
	memoryUse = []

	f = open('cartesian.txt', 'r')
	objInfos = f.read().split('\n\n')
	f.close()
	while '' in objInfos:
		objInfos.remove('')
	g_listOfPlanets = []
	for info in objInfos:
		g_listOfPlanets.append(Planet(info))

	dt = 1.*24.*60.*60. * n

	pbar = ProgressBar()
	
	for i in pbar(range(int(365./n))):

		for p in g_listOfPlanets:
			p.updatePlanet(dt)
		memoryUse.append(py.memory_info()[0]/2.**30)
	
	#write planet histories
	for planet in g_listOfPlanets:
		f = open('coordinates/'+planet._n.replace("/",'')+'.txt', 'w')
		f.write('\n'.join(planet._history))
		f.close()
	pickle.dump(memoryUse,open('memory.p','wb'))

if __name__ == "__main__":
	main()
