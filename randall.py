import numpy as np
from PIL import Image, ImageTk
import math
import triangle
import time 
import tkinter

class Randall:

	pixel_grid_builder = np.vectorize(lambda i, j, k: i + 0.5 if k == 0 else j + 0.5)


	def __init__(self, im_width, im_height, focal_distance = 10, fov = 90):
		self.world_space = np.array([], dtype = object)
		self.camera_space = np.array([], dtype = object)
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

		self.camera_position = (np.array((0,0,0)),np.array((0,0,0)))

		self.tk_root = tkinter.Tk()
		self.tk_frame = tkinter.Frame(self.tk_root, width = im_width, height = im_height)
		self.tk_frame.pack()
		self.canvas = tkinter.Canvas(self.tk_frame, width = im_width, height = im_height)

	def set_camera_position(self, point, angles, rad = False):
		angles = np.array(angles)
		if not rad:
			angles = angles * (math.pi / 180)
		self.camera_position = (np.array(point), angles)

	def update_world_space(self, world_space):
		self.world_space = world_space

	def add_to_world_spce(self, shapes):
		self.update_world_space(np.append(self.world_space, shapes))

	def clear_world_space(self):
		self.world_space = np.array([], dtype = object)

	def draw_thing(self, thing):
		self.add_to_world_spce(thing.place_in_world_space())

	def transform_world(self):
		for triangle in self.world_space:
			nt = triangle.translate(self.camera_position[0])
			nt = nt.rotate(self.camera_position[1])
			self.camera_space = np.append(self.camera_space, [nt])

	def project_space(self):
		projection_space = np.array([], dtype = object)
		for triangle in self.camera_space:
			self.projection_space = np.append(self.projection_space, [triangle.project_to_XY(self.focal_distance)], 0)


	def rasterize(self):
		for triangle in self.projection_space:

			#transform from projection space to image space
			im_points = np.zeros([0,3], dtype = float)
			for point in triangle.points:
				translation_matrix = np.array([self.viewport_width/2, -self.viewport_height/2, 0])
				scaling_matrix = np.array([[self.im_width/self.viewport_width, 0,							         0], 
										   [0, 						  	       -self.im_height/self.viewport_height, 0], 
										   [0,                                 0,                                    1]])
				new_point = scaling_matrix.dot(point + translation_matrix)
				im_points = np.append(im_points, [new_point], 0)
			im_triangle = triangle.morph(im_points)


			x_min = math.floor(min(p[0] for p in im_points))
			x_max = math.ceil (max(p[0] for p in im_points))
			y_min = math.floor(min(p[1] for p in im_points))
			y_max = math.ceil (max(p[1] for p in im_points))

			x_min = max(x_min, 0)
			x_max = min(x_max, self.im_width)
			y_min = max(y_min, 0)
			y_max = min(y_max, self.im_height)


			#TODO: anti-aliasing (multisampling?)

			bbox_grid = np.fromfunction(self.pixel_grid_builder, (x_max - x_min, y_max - y_min, 2)) + (x_min, y_min)
			rast_mask = im_triangle.raster_matrix(bbox_grid)

			depth, color = im_triangle.interpol_props(bbox_grid, rast_mask)
			depth_mask = depth <= self.z_buffer[x_min:x_max, y_min:y_max]
			mask = rast_mask & depth_mask

			self.image_buffer[x_min: x_max, y_min: y_max][mask] = color[mask]
			self.z_buffer[x_min: x_max, y_min: y_max][mask] = depth[mask]




	def display(self):
		#img2 = Image.fromarray(self.image_buffer, 'RGB')
		img = ImageTk.PhotoImage(image=Image.fromarray(self.image_buffer))
		self.canvas.create_image(0,0, anchor="nw", image=img)
		self.canvas.pack()
		self.tk_root.update()

		#img2.save('test.png')



	def render(self):

		#Reset buffers
		self.camera_space = np.array([], dtype = object)
		self.projection_space = np.array([], dtype = object)
		self.z_buffer = np.full([self.im_width, self.im_height], np.inf)
		self.image_buffer = np.full([self.im_width, self.im_height, 3], 255, dtype = np.uint8)

		#start_time = time.time()

		#s_time = time.time()
		self.transform_world()
		#e_time = time.time() - s_time
		#print("World transform: ", e_time)

		#s_time = time.time()
		self.project_space()
		#e_time = time.time() - s_time
		#print("Projection: ", e_time)

		#s_time = time.time()
		self.rasterize()
		#e_time = time.time() - s_time
		#print("Rasterization: ", e_time)

		#s_time = time.time()
		self.display()
		self.clear_world_space()
		#e_time = time.time() - s_time
		#print("Display: ", e_time)

		#total_time = time.time() - start_time
		#print("Total: ", total_time)
