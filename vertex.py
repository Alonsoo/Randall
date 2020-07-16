import numpy as np

class Vertex:

	def __init__(self, point, color = np.zeros(3), texture = None, texture_coordinates = None):
		self.point = np.array(point)
		self.color = np.array(color)
		self.texture = texture
		self.texture_coordinates = np.array(texture_coordinates)

	def morph(self, new_point):
		return Vertex(new_point, self.color, self.texture, self.texture_coordinates)