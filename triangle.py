import numpy as np
import math
from vertex import Vertex

class Triangle:

	def __init__(self, vertices):
		self.vertices = vertices


	def points(self):
		return np.array([v.point for v in self.vertices])

	def __str__(self):
		return str(self.points())


	def project_to_XY(self, focal_distance):

		new_vertices = np.array([], dtype = object)

		for vertex in self.vertices:
			s = focal_distance/vertex.point[2]
			projection_matrix = np.array([[s, 0, 0],
										  [0, s, 0],
										  [0, 0, 1]])
			new_vertices = np.append(new_vertices, [Vertex(projection_matrix.dot(vertex.point), vertex.color)], 0)

		return(Triangle(new_vertices))

	def morph(self, new_points):
		"""Copies vertex colors over to new triangle"""
		new_vertices = np.array([Vertex(new_points[i], self.vertices[i].color) for i in range(3)])
		return Triangle(new_vertices)


	def contains(self, point):
		"""Checks weather a 2D point is inside the 2D projection of the triangle over the XY plane
			point must be a one dimensional, length 2 numpy array"""
		points = np.delete(self.points(), 2, 1)

		x_min = min([p[0] for p in points])
		x_max = max([p[0] for p in points])
		y_min = min([p[1] for p in points])
		y_max = max([p[1] for p in points])

		if point[0] > x_max or point[0] < x_min or point[1] > y_max or point[1] < y_min:
			print("bbox fail")
			return False

		positions = []

		for i in range(3):
			v = points[(i+1)%3] - points[i]
			n = np.array([-v[1], v[0]])

			p = point - points[i]

			d = n.dot(p)
			print(n)
			positions.append(np.sign(d))

		return np.all([s >= 0 for s in positions]) or np.all([s <= 0 for s in positions])
		#TODO, check whether floating point error correction for points on line is necesary
		#TODO, implement top left rule