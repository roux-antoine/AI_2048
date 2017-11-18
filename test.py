import numpy as np
import time

grid = np.array([[2, 16, 4, 8],
                 [8, 4, 32, 4],
                 [64, 8, 2, 2],
                 [4, 16, 4, 4]])

grid2 = [[2, 16, 4, 8],
                 [8, 4, 32, 4],
                 [64, 8, 2, 2],
                 [4, 16, 4, 4]]


fitnessArray = [[9,  5, 3, 1],
                [17,  9, 4, 2],
                [33,  16, 8, 4],
                [64, 32, 16, 8]]

start = time.time()
for k in range (100000) :
    # for i in range(4) :
    #     for j in range (4) :
    #         fitness = grid[i,j] * fitnessArray[i][j]
    toto = grid2*fitnessArray
    fitness = sum(toto)

print(time.time()-start)
