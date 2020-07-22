import numpy as np
import randall
from triangle import *
from thing import * 
from PIL import Image
from chessTexture import ChessTexture
from itertools import permutations


def prism(origin, dims):
	ts = np.array([[dims[0],0,0], [0,dims[1],0], [0,0,dims[2]]])

	perms = permutations(range(3), 2)
	triangles = []

	for perm in perms:
		i,j = perm[0], perm[1]
		for d in [-1, 1]:
			p = dims * d/2
			points = [p, p - d*ts[i], p - d*(ts[i] + ts[j])]
			texture_coords = [[0,0], [ts[i,i], 0], [ts[i,i], ts[j,j]]]
			triangles.append(Triangle(points, texture = ChessTexture, texture_coordinates = texture_coords))

	return Thing(triangles, origin)




rn = randall.Randall(512, 512, 10)
rn.set_camera_position([15,0,0],[0,0,0])

#points = [[rn.viewport_width/2, rn.viewport_height/2, 18], [-rn.viewport_width/2, rn.viewport_height/2, 15], [0, 0, 40]]
#texture = ChessTexture
#texture_coordinates = [[0,0],[0,10],[10,10]]

#t = Triangle(points, texture = texture, texture_coordinates = texture_coordinates)
#thing = Thing([t])

cube = prism(np.array([0,0,50]), np.array([20,10,10]))


#rn.render()
for i in range (45):
	#rn.set_camera_position([0,0,0],[0,0,i*4])
	#cube.set_orientation([i*8,0,0])
	rn.draw_thing(cube)
	rn.render()

#print(rn.world_space[0])
#print(rn.projection_space[0])






