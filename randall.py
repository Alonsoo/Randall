import numpy as np
import math

class Randall:

	def __init__(self, im_width, im_height, focal_distance = 10, fov = 90):
		self.world_space = np.zeros([0, 3, 3])
		self.projection_space = np.zeros([0, 3, 3])
		self.z_buffer = np.zeros([im_width, im_height])
		self.image_buffer = np.zeros([im_width, im_height, 3])

		self.im_width = im_width
		self.im_height = im_height
		self.fov = fov
		self.focal_distance = focal_distance
		aspect_ratio = im_height / im_width

		self.viewport_width = 2 * focal_distance * math.tan(math.radians(fov/2))
		self.viewport_height = self.viewport_width * aspect_ratio

	def update_world_space(self, world_space):
		self.world_space = world_space
		self.render()

	def add_to_world_spce(self, shapes):
		self.update_world_space(np.append(self.world_space, shapes))

	def transform_world(self):
		pass

	def project_space(self):
		projection_space = np.zeros([0, 3, 3])
		for triangle in self.world_space:
			projected_triangle = np.zeros([0, 3])

			for point in triangle:
				s = self.focal_distance/point[2] 
				print(s)
				projection_matrix = np.array([[s, 0, 0],
											  [0, s, 0],
											  [0, 0, 1]])
				# TODO: cut triangles that fall outside viewport
				projected_triangle = np.append(projected_triangle, [projection_matrix.dot(point)], 0)
			self.projection_space = np.append(self.projection_space, [projected_triangle], 0)


	def rasterize(self):
		for triangle in self.projection_space:
			pass


	def render(self):
		self.transform_world()
		self.project_space()
		self.rasterize()