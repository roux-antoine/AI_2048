
import numpy as np
import random
import time

# class bcolors:
#     HEADER = '\033[95m'
#     OKBLUE = '\033[94m'
#     OKGREEN = '\033[92m'
#     WARNING = '\033[93m'
#     FAIL = '\033[91m'
#     ENDC = '\033[0m'
#     BOLD = '\033[1m'
#     UNDERLINE = '\033[4m'
# print (bcolors.OKBLUE + "Some text"
#   + bcolors.ENDC)

class Grid (object) :

    def __init__ (self, grid) :
        """
        """
        self.grid = np.array(grid)

    def __str__ (self) :
        string = ""
        for k in range (4) :
            for i in range (4) :
                if self.grid[k][i] == 0 :
                    string += "." + "    "
                else :
                    nbrDigits = 1
                    power = 10
                    while (self.grid[k][i] // power > 0.5) : #0.5 is to avoid numeric noise
                            nbrDigits+=1
                            power *= 10
                    string += str(self.grid[k][i]) + (5-nbrDigits)*" "
            string += "\n"
        return string

    def canSwipeBase (self) :
        """ returns True if swiping up has an effect
        """
        for columnNbr in range(4) :
            currentColumn = self.grid[:,columnNbr]
            nbrNonZero = np.count_nonzero(currentColumn)
            if nbrNonZero == 0 : #if empty, go to next
                #print("isEmpty")
                continue
            if nbrNonZero == 4 : #if full, go to next
                #print("isFull")
                continue

            for lineNbr in range(3, -1 + nbrNonZero, -1) :
                if currentColumn[lineNbr] != 0 :
                    return True

            for lineNbr in range(0, 3) :
                if currentColumn[lineNbr] == currentColumn[lineNbr+1] :
                    return True

        return False

    def canSwipeUp (self) :
        """ returns True if swiping up has an effect
            using canSwipeBase
        """
        return(self.canSwipeBase())

    def canSwipeRight (self) :
        """ returns True if swiping right has an effect
            using canSwipeBase
        """
        rotated = np.rot90(self.grid)
        return(Grid(rotated).canSwipeBase())

    def canSwipeDown (self) :
        """ returns True if swiping down has an effect
            using canSwipeBase
        """
        rotated = np.rot90(np.rot90(self.grid))
        return(Grid(rotated).canSwipeBase())

    def canSwipeLeft (self) :
        """ returns True if swiping left has an effect
            using canSwipeBase
        """
        rotated = np.rot90(np.rot90(np.rot90(self.grid)))
        return(Grid(rotated).canSwipeBase())

    def swipeBase (self) :
        """ swipes the grid up, doing all the necessary additions ()
        """
        grid = self.grid

        #we start by putting every tile up
        for columnNbr in range(4) :
            nbrZeros = 4 - np.count_nonzero(grid[:,columnNbr])

            for lineNbr in range(4) :
                counter = 0
                while (grid[lineNbr, columnNbr] == 0) and (counter < 4):
                    counter += 1
                    if np.count_nonzero(grid[lineNbr:4, columnNbr]) != 0 :
                        for remainingLine in range (lineNbr, 3) :
                            grid[remainingLine, columnNbr] = grid[remainingLine+1, columnNbr]
                        grid[3, columnNbr] = 0

        #now we do the additions
            for lineNbr in range(3) :
                if grid[lineNbr, columnNbr] == grid[lineNbr+1, columnNbr] :
                    grid[lineNbr, columnNbr] *= 2
                    for remainingLine in range (lineNbr+1, 3) :
                        grid[remainingLine, columnNbr] = grid[remainingLine+1, columnNbr]
                    grid[3, columnNbr] = 0

        return (grid)

    def swipeUp (self) :
        """ swipes the grid up, doing all the necessary additions
            uses swipeBase
        """
        self.grid = self.swipeBase()

    def swipeRight (self) :
        """ swipes the grid right, doing all the necessary additions
            uses swipeBase
        """
        rotated = Grid(np.rot90(self.grid))
        self.grid = np.rot90(np.rot90(np.rot90(rotated.swipeBase())))

    def swipeDown (self) :
        """ swipes the grid down, doing all the necessary additions
            uses swipeBase
        """
        rotated = Grid(np.rot90(np.rot90(self.grid)))
        self.grid = np.rot90(np.rot90(rotated.swipeBase()))

    def swipeLeft (self) :
        """ swipes the grid left, doing all the necessary additions
            uses swipeBase
        """
        rotated = Grid(np.rot90(np.rot90(np.rot90(self.grid))))
        self.grid = np.rot90(rotated.swipeBase())

    def addNbr (self) :
        """ adds a number on a empty space
            2 with probability 9/10 ; 4 with probability 1/10
            doesnt return anything
            UN PEU BOURRIN POUR LE MOMENT
        """
        #we pick out the random number : 2 or 4
        if random.randint(1,10) == 1:
            randomNbr = 4
        else :
            randomNbr = 2

        #we pick a random position for the number
        emptyCounter = 0
        for k in range (4) :
            for i in range (4) :
                if self.grid[k,i] == 0 :
                    emptyCounter += 1

        randomPosition = random.randint(0,emptyCounter-1)
        counter = 0
        for k in range (4) :
            for i in range (4) :
                if self.grid[k,i] == 0 :
                    if (counter == randomPosition) :
                        self.grid[k,i] = randomNbr
                        return #we leave the function
                    counter += 1

    def calcFitness (self) :
        """ Returns the fitness of the grid

        """
        fitnessArray = [[8,  4, 2, 1],
                        [16,  8, 4, 2],
                        [32,  16, 8, 4],
                        [64, 32, 16, 8]]
        # fitnessArray = [[160,  80, 5, 4],
        #                 [320,  40, 4, 3],
        #                 [640,  20, 3, 2],
        #                 [1280, 10, 2, 1]]
        fitness = 0
        for k in range(4) :
            for i in range (4) :
                fitness += self.grid[k,i] * fitnessArray[k][i]
        return (fitness / 100)

##############################################

arrayGrid1 = [[0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0]]

arrayGrid2 = [[2, 8, 2, 2],
              [2, 2, 2, 0],
              [4, 2, 4, 0],
              [2, 2, 2, 2]]



# MODE = "PLAY"
# MODE = "TEST"
MODE = "AI"

##############################################


if MODE == "TEST" :
    # myGrid = Grid(arrayGrid2)
    # print(myGrid)
    pass


if MODE == "PLAY" :
    myGrid = Grid(arrayGrid1)
    myGrid.addNbr()
    myGrid.addNbr()

    while True :
        print(myGrid)
        print("Press key")
        user_input = input()
        if user_input == "z" and myGrid.canSwipeUp() :
            myGrid.swipeUp()
            myGrid.addNbr()
        elif user_input == "s" and myGrid.canSwipeRight() :
            myGrid.swipeUp()
            myGrid.addNbr()
        elif user_input == "w" and myGrid.canSwipeDown() :
            myGrid.swipeDown()
            myGrid.addNbr()
        elif user_input == "q" and myGrid.canSwipeLeft() :
            myGrid.swipeLeft()
            myGrid.addNbr()
        else :
            pass
        print(myGrid.calcFitness())

if MODE == "AI" :
    myGrid = Grid(arrayGrid1)
    myGrid.addNbr()
    myGrid.addNbr()

    while True :
        print(myGrid)
        fitnessArray = [0,0,0,0]

        tempGrid = Grid(myGrid.grid)
        if tempGrid.canSwipeUp() :
            tempGrid.swipeUp()
            fitnessArray[0] = tempGrid.calcFitness()

        tempGrid = Grid(myGrid.grid)
        if tempGrid.canSwipeRight() :
            tempGrid.swipeRight()
            fitnessArray[1] = tempGrid.calcFitness()

        tempGrid = Grid(myGrid.grid)
        if tempGrid.canSwipeDown() :
            tempGrid.swipeDown()
            fitnessArray[2] = tempGrid.calcFitness()

        tempGrid = Grid(myGrid.grid)
        if tempGrid.canSwipeLeft() :
            tempGrid.swipeLeft()
            fitnessArray[3] = tempGrid.calcFitness()


        direction = fitnessArray.index(max(fitnessArray))
        print(int(fitnessArray[0]), int(fitnessArray[1]), int(fitnessArray[2]), int(fitnessArray[3]))
        print(direction)
        if direction == 0 :
            myGrid.swipeUp()
        elif direction == 1 :
            myGrid.swipeRight()
        elif direction == 2 :
            myGrid.swipeDown()
        elif direction == 3 :
            myGrid.swipeLeft()

        myGrid.addNbr()
        user_input = input()
