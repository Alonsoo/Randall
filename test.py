import numpy as np
import randall

rn = randall.Randall(30, 15, 10)
ws = np.array([[[0,0,20], [5,10,10], [15, 0, 30]]])

rn.update_world_space(ws)

print(rn.world_space)
print(rn.projection_space)