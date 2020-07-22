import numpy as np
import math


class Thing:

	def __init__(self, triangles, origin = (0,0,0), angles = (0,0,0), rad = False):
		self.triangles = triangles
		self.origin = np.array(origin)
		self.set_orientation(angles, rad)


	def set_orientation(self, angles, rad = False):
		angles = np.array(angles)
		if not rad:
			angles = angles * (math.pi / 180)
		self.angles = angles


	def place_in_world_space(self):
		triangles = [t.rotate(self.angles) for t in self.triangles]
		triangles = [t.translate(self.origin) for t in triangles]
		return triangles

