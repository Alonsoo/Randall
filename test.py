import numpy as np
import randall
import triangle
from vertex import Vertex
from PIL import Image
from chessTexture import ChessTexture

rn = randall.Randall(512, 512, 10)
#ws = np.array([[[0,0,20], [5,10,10], [15, 0, 30]]])
#vertices = np.array([Vertex([0, 0, 20]), Vertex([5, 10, 10]), Vertex([15, 0, 30])])
#vertices = np.array([Vertex([0, 0, 10]), Vertex([100, 100, 10]), Vertex([100, 0, 10])])
#vertices = np.array([Vertex([0, 0, 15]), Vertex([-rn.viewport_width/2, rn.viewport_height/2, 15]), Vertex([rn.viewport_width/2, rn.viewport_height/2, 18])])
#vertices = np.array([Vertex([rn.viewport_width/2, rn.viewport_height/2, 18], color = [200, 0, 0]), 
#					 Vertex([-rn.viewport_width/2, rn.viewport_height/2, 15], color = [0, 200, 0]), 
#					 Vertex([0, 0, 10], color = [0, 0, 200])])

#vertices = np.array([Vertex([rn.viewport_width/2, rn.viewport_height/2, 18], texture = ChessTexture, texture_coordinates = [0,0]), 
#					 Vertex([-rn.viewport_width/2, rn.viewport_height/2, 15], texture = ChessTexture, texture_coordinates = [0,10]), 
#					 Vertex([0, 0, 40], texture = ChessTexture, texture_coordinates = [10,10])])

points = [[rn.viewport_width/2, rn.viewport_height/2, 18], [-rn.viewport_width/2, rn.viewport_height/2, 15], [0, 0, 40]]
texture = ChessTexture
texture_coordinates = [[0,0],[0,10],[10,10]]



ws = np.array([triangle.Triangle(points, texture = texture, texture_coordinates = texture_coordinates)])

rn.update_world_space(ws)

#print(rn.world_space[0])
#print(rn.projection_space[0])