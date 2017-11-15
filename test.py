fitnessArray = [[2,5,0,0],
                [0,0,0,0],
                [0,0,0,0],
                [0,0,0,0]]

maxArray = [0,0,0,0]
for k in range (4) :
    maxArray[k] = max(fitnessArray[k])

print(maxArray)
direction = maxArray.index(max(maxArray))

print(direction)
