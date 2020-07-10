import numpy as np
import randall
import triangle
from vertex import Vertex
from PIL import Image

rn = randall.Randall(512, 512, 10)
#ws = np.array([[[0,0,20], [5,10,10], [15, 0, 30]]])
#vertices = np.array([Vertex([0, 0, 20]), Vertex([5, 10, 10]), Vertex([15, 0, 30])])
#vertices = np.array([Vertex([0, 0, 10]), Vertex([100, 100, 10]), Vertex([100, 0, 10])])
vertices = np.array([Vertex([0, 0, 10]), Vertex([-rn.viewport_width/2, rn.viewport_height/2, 10]), Vertex([rn.viewport_width/2, rn.viewport_height/2, 10])])
ws = np.array([triangle.Triangle(vertices)])

rn.update_world_space(ws)

#print(rn.world_space[0])
#print(rn.projection_space[0])