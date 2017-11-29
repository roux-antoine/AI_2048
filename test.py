import numpy as np
import time

grid = np.array([[2, 16, 4, 8],
                 [8, 4, 32, 4],
                 [64, 8, 2, 2],
                 [4, 16, 4, 4]])

grid2 = np.array([[1, 16, 4, 8],
                 [8, 5, 32, 9],
                 [6, 8, 2, 2],
                 [4, 32, 12, 4]])

# startTime = time.time()
# for k in range (1000000) :
#     toto = sum(sum(grid))
#
# print(time.time()-startTime)
#
# start = time.time()
# for k in range (1000000) :
#     toto = grid.sum()
#
# print(time.time()-startTime)
