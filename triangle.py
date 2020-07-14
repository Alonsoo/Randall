import numpy as np
import math
from vertex import Vertex
import time

class Triangle:

	def __init__(self, vertices):
		self.vertices = vertices


	def points(self):
		return np.array([v.point for v in self.vertices])

	def __str__(self):
		return str(self.points())


	def project_to_XY(self, focal_distance):
		"""Returns new triangle projected to an XY plane focal_distance away from the origin"""
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


	def get_normals(self):
		if  not hasattr(self, 'normals'):
			points = np.delete(self.points(), 2, 1)
			vs = [points[(i+1)%3] - points[i] for i in range(3)]
			self.normals = [np.array([-vs[i][1], vs[i][0]]) for i in range(3)]
		return self.normals


	#Deprecated
	def contains(self, point):
		"""Checks weather a 2D point is inside the 2D projection of the triangle over the XY plane
			point must be a one dimensional, length 2 numpy array"""
		#Get only the x and y coordinates of points
		points = np.delete(self.points(), 2, 1)
		positions = []

		for i in range(3):
			p = point - points[i]
			d = self.get_normals()[i].dot(p)

			positions.append(np.sign(d))

		return np.all([s >= 0 for s in positions]) or np.all([s <= 0 for s in positions])
		#TODO: check whether floating point error correction for points on line is necesary
		#TODO: implement top left rule


	def raster_matrix(self, matrix):
		#TODO: implement tiling optimization, maybe remove matrix dependence and let triangle handle it (would need to return rast matrix origin)

		points = np.delete(self.points(), 2, 1)

		dif1 = matrix - points[0]
		slice1 = dif1.dot(self.get_normals()[0])
		rast1 = slice1 >= 0 
		rast1b = slice1 <= 0 

		dif2 = matrix - points[1]
		slice2 = dif2.dot(self.get_normals()[1])
		rast2 = slice2 >= 0 
		rast2b = slice2 <= 0 

		dif3 = matrix - points[2]
		slice3 = dif3.dot(self.get_normals()[2])
		rast3 = slice3 >= 0 
		rast3b = slice3 <= 0 

		return (rast1 & rast2 & rast3) | (rast1b & rast2b & rast3b)