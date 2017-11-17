arrayGrid3 = [[2, 16, 4, 8],
              [8, 4, 32, 4],
              [64, 8, 2, 2],
              [4, 16, 4, 4]]

import numpy as np

toto = np.array(arrayGrid3)

print(np.count_nonzero(toto))
