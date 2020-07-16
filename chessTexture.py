import math
import numpy as np

class ChessTexture:

	black = np.zeros(3)
	white = np.full((3), 255)

	@staticmethod
	def getColor(point):
		if (math.floor(point[0]) + math.floor(point[1])) % 2 == 0:
			return ChessTexture.black
		else:
			return ChessTexture.white

	@staticmethod
	def getColors(matrix):
		colors = (np.sum(np.floor(matrix), 2) % 2) * 255
		colors = np.expand_dims(colors, 2)
		colors = np.concatenate((colors, colors, colors), axis = 2)
		return colors
