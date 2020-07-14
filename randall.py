import numpy as np
from PIL import Image
import math
import triangle
import time

class Randall:

	pixel_grid_builder = np.vectorize(lambda i, j, k: i + 0.5 if k == 0 else j + 0.5)


	def __init__(self, im_width, im_height, focal_distance = 10, fov = 90):
		self.world_space = np.array([], dtype = object)
		self.projection_space = np.array([], dtype = object)
		self.z_buffer = np.full([im_width, im_height], np.inf)
		self.image_buffer = np.full([im_width, im_height, 3], 255, dtype = np.uint8)

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
		projection_space = np.array([], dtype = object)
		for triangle in self.world_space:
			self.projection_space = np.append(self.projection_space, [triangle.project_to_XY(self.focal_distance)], 0)


	def rasterize(self):
		for triangle in self.projection_space:

			#transform from projection space to image space
			im_points = np.zeros([0,3], dtype = float)
			for point in triangle.points():
				translation_matrix = np.array([self.viewport_width/2, -self.viewport_height/2, 0])
				scaling_matrix = np.array([[self.im_width/self.viewport_width, 0,							         0], 
										   [0, 						  	       -self.im_height/self.viewport_height, 0], 
										   [0,                                 0,                                    1]])
				new_point = scaling_matrix.dot(point + translation_matrix)
				im_points = np.append(im_points, [new_point], 0)
			im_triangle = triangle.morph(im_points)


			x_min = math.floor(min(p[0] for p in im_points))
			x_max = math.ceil(max(p[0] for p in im_points))
			y_min = math.floor(min(p[1] for p in im_points))
			y_max = math.ceil(max(p[1] for p in im_points))

			s_time = time.time()

			"""for i in range(x_min, x_max):
				for j in range(y_min, y_max):
					pixel_center = np.array([i + 0.5, j + 0.5])

					if im_triangle.contains(pixel_center):
					 	depth = 1 #im_triangle.interpolateDepth(pixel_center)
					 	if depth < self.z_buffer[i, j]:
					 		self.image_buffer[i, j] = np.zeros(3) #triangle.interpolateColor(pixel_center)
					 		self.z_buffer[i, j] = depth
					#TODO: anti-aliasing (multisampling?) """

			bbox = np.fromfunction(self.pixel_grid_builder, (x_max - x_min, y_max - y_min, 2)) + (x_min, y_min)
			rast = im_triangle.raster_matrix(bbox)
			print(rast)

			color = np.zeros((x_max - x_min, y_max - y_min, 3))
			#rast_color = color * np.expand_dims(rast, 2) + np.invert(np.expand_dims(rast, 2)) * 255
			self.image_buffer[x_min: x_max, y_min: y_max][rast] = color[rast]


			e_time = time.time() - s_time
			print(e_time)


	def display(self):
		img = Image.fromarray(self.image_buffer, 'RGB')
		img.save('test.png')
		img.show()		



	def render(self):
		self.transform_world()
		self.project_space()
		self.rasterize()
		self.display()
