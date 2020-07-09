import numpy as np

class Triangle:

	def __init__(self, vertices):
		self.vertices = vertices


	def points(self):
		return np.array([v.point for v in self.vertices])

	def inside(self, point):
		pass

	def project(self, projection_matrix):
		pass

