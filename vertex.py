import numpy as np

class Vertex:

	def __init__(self, point, color = np.zeros(3)):
		self.point = np.array(point)
		self.color = color