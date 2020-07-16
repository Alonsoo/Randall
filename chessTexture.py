import math
import numpy as np

class ChessTexture:

	black = np.zeros(3)
	white = np.full((3), 255)

	@staticmethod
	def getColor(x, y):
		if (math.floor(x) + math.floor(y)) % 2 == 0:
			return ChessTexture.black
		else:
			return ChessTexture.white