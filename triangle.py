import numpy as np
import math

class Triangle:

	def __init__(self, points, colors = np.zeros((3,3)), texture = None, texture_coordinates = None):
		self.points = np.array(points)
		self.colors = np.array(colors)
		self.texture = texture
		self.texture_coordinates = np.array(texture_coordinates)


	def __str__(self):
		return str(self.points())

	def translate(self, matrix):
		return self.morph(self.points + matrix)

	def rotate(self, angles):
		sin_a, cos_a = math.sin(angles[0]), math.cos(angles[0])
		sin_b, cos_b = math.sin(angles[1]), math.cos(angles[1])
		sin_c, cos_c = math.sin(angles[2]), math.cos(angles[2])
		x_rot = np.array([[1,     0,      0], 
						  [0, cos_a, -sin_a],
						  [0, sin_a,  cos_a]])

		y_rot = np.array([[cos_b,  0, sin_b],
						  [0,      1,     0],
						  [-sin_b, 0, cos_b]]) #checar si este si esta bien ???

		z_rot = np.array([[cos_c, -sin_c, 0], 
						  [sin_c,  cos_c, 0],
						  [0,      0,     1]])

		R = z_rot.dot(y_rot.dot(x_rot))
		new_points = [R.dot(p) for p in self.points]
		return self.morph(new_points)


	def project_to_XY(self, focal_distance):
		"""Returns new triangle projected to an XY plane focal_distance away from the origin"""
		new_points = np.zeros((0,3))

		for point in self.points:
			s = focal_distance/point[2]
			projection_matrix = np.array([[s, 0, 0],
										  [0, s, 0],
										  [0, 0, 1]])
			new_points = np.append(new_points, [projection_matrix.dot(point)], 0)
		return(self.morph(new_points))


	def morph(self, new_points):
		"""Copies vertex attributes over to new triangle"""
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

		#Compute barycentric coordinates for points in grid
		ls = np.zeros((grid.shape[0], grid.shape[1], 3))
		ls[:, :, 0:2] = np.tensordot(grid - np.delete(points[2], 2), T_inv, (2, 1))
		ls[:, :, 2] = 1 -ls[:, :, 0] - ls[:, :, 1]

		gs = ls / points[ : , 2]

		depth = 1/np.sum(gs, axis = 2)

		us = np.zeros((grid.shape[0], grid.shape[1], 2))

		if self.texture == None:
			color = depth * gs.dot(self.colors)
		else:
			m = np.insert(np.expand_dims(gs, 3), 1, gs, axis = 3)
			f = np.tile(self.texture_coordinates, (grid.shape[0], grid.shape[1], 1, 1))
			us = np.insert(np.expand_dims(depth, 2), 1, depth, axis = 2) * np.sum(m * f, axis = 2 )
			color = self.texture.getColors(us)


		return (depth, color)
