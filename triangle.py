import numpy as np
import math
from vertex import Vertex

class Triangle:

	def __init__(self, points, colors = np.zeros((3,3)), texture = None, texture_coordinates = None):
		self.points = np.array(points)
		self.colors = np.array(colors)
		self.texture = texture
		self.texture_coordinates = np.array(texture_coordinates)


	"""def points(self):
		return np.array([v.point for v in self.vertices])"""

	def __str__(self):
		return str(self.points())


	def project_to_XY(self, focal_distance):
		"""Returns new triangle projected to an XY plane focal_distance away from the origin"""
		new_points = np.zeros((0,3))

		for point in self.points:
			s = focal_distance/point[2]
			projection_matrix = np.array([[s, 0, 0],
										  [0, s, 0],
										  [0, 0, 1]])
			new_points = np.append(new_points, [projection_matrix.dot(point)], 0)
			#new_vertices = np.append(new_vertices, [vertex.morph(projection_matrix.dot(vertex.point))], 0)
		return(self.morph(new_points))


	def morph(self, new_points):
		"""Copies vertex attributes over to new triangle"""
		#new_vertices = np.array([self.vertices[i].morph(new_points[i]) for i in range(3)])
		return Triangle(new_points, self.colors, self.texture, self.texture_coordinates)


	def get_normals(self):
		if not hasattr(self, 'normals'):
			points = np.delete(self.points, 2, 1)
			vs = [points[(i+1)%3] - points[i] for i in range(3)]
			self.normals = [np.array([-vs[i][1], vs[i][0]]) for i in range(3)]
		return self.normals


	def raster_matrix(self, matrix):
		#TODO: implement tiling optimization, maybe remove matrix dependence and let triangle handle it (would need to return rast matrix origin)

		points = np.delete(self.points, 2, 1)

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


	def interpol_props(self, grid, rast_mask):

		points = self.points
		#normal = self.get_plane_normal()

		T = np.array([[points[0][0] - points[2][0], points[1][0] - points[2][0]], 
			          [points[0][1] - points[2][1], points[1][1] - points[2][1]]])

		T_inv = (1/np.linalg.det(T)) * np.array([[T[1,1], -T[0,1]],
												 [-T[1,0], T[0,0]]])

		color = np.zeros((grid.shape[0], grid.shape[1], 3))
		depth = np.full((grid.shape[0], grid.shape[1]), np.inf)

		for i in range(grid.shape[0]):
			for j in range(grid.shape[1]):
				l = T_inv.dot(np.array([grid[i][j][0] - points[2][0], grid[i][j][1] - points[2][1]]))
				l1, l2 = l[0], l[1]
				l3 = 1 - l1 - l2

				g1, g2, g3 = l1/points[0][2], l2/points[1][2],  l3/points[2][2]

				z = 1/(g1 + g2 + g3)
				depth[i, j] = z

				if self.texture == None:
					#Interpolate color
					color[i, j] = z * (self.colors[0] * g1 + self.colors[1] * g2 + self.colors[2] * g3)
				else:
					#Interpolate texture coordinates
					u = z * (self.texture_coordinates[0] * g1 + self.texture_coordinates[1] * g2 + self.texture_coordinates[2] * g3)
					color[i, j] = self.texture.getColor(u[0], u[1])


		return (depth, color)
