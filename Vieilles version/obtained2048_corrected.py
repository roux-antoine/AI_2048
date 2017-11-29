
import numpy as np
import random
import time
import matplotlib.pyplot as plt

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

    def canSwipeBase (self, grid) :
        """ returns True if swiping up has an effect
        """
        for columnNbr in range(4) :
            currentColumn = grid[:,columnNbr]
            nbrNonZero = np.count_nonzero(currentColumn)
            if nbrNonZero == 0 : #if empty, go to next
                #print("isEmpty")
                continue
            #warning : if the line is full, it can still be swiped !!

            for lineNbr in range(3, -1 + nbrNonZero, -1) :
                if currentColumn[lineNbr] != 0 :
                    return True

            for lineNbr in range(0, 3) :
                if currentColumn[lineNbr] == currentColumn[lineNbr+1] and currentColumn[lineNbr] != 0:
                    return True

        return False

    def canSwipe (self, direction) :
        """ returns True if swiping has an effect using canSwipeBase
            direction = 0 up, 1 right, 2 down, 3 left
        """
        if direction == 0 :
            return(self.canSwipeBase(self.grid))

        elif direction == 1 :
            rotated = np.rot90(self.grid)
            return(self.canSwipeBase(rotated))

        elif direction == 2 :
            rotated = np.rot90(np.rot90(self.grid))
            return(self.canSwipeBase(rotated))

        elif direction == 3 :
            rotated = np.rot90(np.rot90(np.rot90(self.grid)))
            return(self.canSwipeBase(rotated))

        else :
            return False

    def swipeBase (self, grid) :
        """ swipes the grid up, doing all the necessary additions ()
        """
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

    def swipe (self, direction) :
        """ swipes the grid, doing all the necessary additions (uses swipeBase)
        """

        if direction == 0 :
            self.grid = self.swipeBase(self.grid)

        elif direction == 1 :
            rotated = np.rot90(self.grid)
            self.grid = np.rot90(np.rot90(np.rot90(self.swipeBase(rotated))))

        elif direction == 2 :
            rotated = np.rot90(np.rot90(self.grid))
            self.grid = np.rot90(np.rot90(self.swipeBase(rotated)))

        elif direction == 3 :
            rotated = np.rot90(np.rot90(np.rot90(self.grid)))
            self.grid = np.rot90(self.swipeBase(rotated))

        else :
            pass

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

        # we pick a random position for the number
        emptyCounter = 16 - np.count_nonzero(self.grid)

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
        # fitnessArray = [[64,  16, 4, 1],  #a peu près pareil
        #                 [256,  64, 16, 4],
        #                 [1024,  256, 64, 16],
        #                 [4096, 1024, 256, 64]]

        fitnessArray = [[8,  4, 2, 1],
                        [16,  8, 4, 2],
                        [32,  16, 8, 4],
                        [64, 32, 16, 8]]
        fitness = 0
        for k in range(4) :
            for i in range (4) :
                fitness += self.grid[k,i] * fitnessArray[k][i]
        return (fitness)

##############################################

arrayGrid1 = [[0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0]]

arrayGrid2 = [[2, 8, 2, 2],
              [2, 2, 2, 0],
              [4, 2, 4, 0],
              [2, 2, 2, 2]]

arrayGrid3 = [[2, 16, 4, 8],
              [8, 4, 32, 4],
              [64, 8, 2, 2],
              [4, 16, 4, 4]]


# MODE = "PLAY"
# MODE = "TEST"
# MODE = "AI"
MODE = "MULTI_AI"

##############################################
def evaluateGrid(givenGrid) :
    """ Returns the max value of the grid
    """
    return(givenGrid.max())

def single_AI() :
    myGrid = Grid([[0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0]])
    myGrid.addNbr()
    myGrid.addNbr()

    while True :
        fitnessArray = np.array([[0, 0, 0, 0], #lignes = à 1er move constant
                                 [0, 0, 0, 0],
                                 [0, 0, 0, 0],
                                 [0, 0, 0, 0]])

        #we determine what moves to consider (not necessarily all the possible moves)
        possibleMoves = [False, False, False, False]
        for k in range (4) :
            possibleMoves[k] = myGrid.canSwipe(k)

        if sum(possibleMoves) != 0 : #if at least one move is possible

            if (possibleMoves[0] == True or possibleMoves[2] == True or possibleMoves[3] == True) :
                #if can swipe up, left or down, do not swipe right
                consideredMovesArray = [0, 2, 3]

            # if np.count_nonzero(myGrid.grid[0]) != 0 :
            #     #if first line is not full, do not swipe up
            #     consideredMovesArray = [0, 2, 3]


            #we compute the fitness for the moves considered
            for k in consideredMovesArray :
                for i in range (4) :
                    tempGrid = Grid(myGrid.grid)
                    if tempGrid.canSwipe(k) :
                        tempGrid.swipe(k)
                        if tempGrid.canSwipe(i) :
                            tempGrid.swipe(i)
                            fitnessArray[k][i] = tempGrid.calcFitness()



            maxArray = [0,0,0,0]
            for k in range (4) :
                maxArray[k] = max(fitnessArray[k])
                # maxArray[k] = fitnessArray[k].mean() #moins bon que le max

            #we reverse the array to make sure the default swipe is left and not up
            reversedMaxArray = maxArray[::-1]
            direction2 = reversedMaxArray.index(max(reversedMaxArray))
            direction = maxArray.index(max(maxArray))

            if direction2 == 0 :
                direction2 = 3
            elif direction2 == 1 :
                direction2 = 2
            elif direction2 == 2 :
                direction2 = 1
            elif direction2 == 3 :
                direction2 = 0

            myGrid.swipe(direction2) #mettre direction pour swiper sans avoir reverse l'array
            myGrid.addNbr()

        else : #if no move is possible
            return(myGrid.grid)
            break

        #useful for debugging and seeing what is happening:
        # print(myGrid)
        # user_input = input()


##############################################


if MODE == "TEST" :
    myGrid = Grid(arrayGrid3)
    print(myGrid.canSwipe(2))
    pass

if MODE == "PLAY" :
    myGrid = Grid(arrayGrid1)
    myGrid.addNbr()
    myGrid.addNbr()

    while True :
        print(myGrid)
        print("Press key")
        user_input = input()
        if user_input == "z" and myGrid.canSwipe(0) :
            myGrid.swipe(0)
            myGrid.addNbr()
        elif user_input == "s" and myGrid.canSwipe(1) :
            myGrid.swipe(1)
            myGrid.addNbr()
        elif user_input == "w" and myGrid.canSwipe(2) :
            myGrid.swipe(2)
            myGrid.addNbr()
        elif user_input == "q" and myGrid.canSwipe(3) :
            myGrid.swipe(3)
            myGrid.addNbr()
        else :
            pass
        print(myGrid.calcFitness())

if MODE == "AI" :
    startTime = time.time()
    finishedGrid = single_AI()
    endTime = time.time()
    print(" \n----- Partie finie -----")
    print("Temps écoulé :", int((endTime-startTime)*1000), "ms")
    print("Valeur max :", evaluateGrid(finishedGrid))
    print(Grid(finishedGrid))
    print("------------------------")


if MODE == "MULTI_AI" :
    startTime = time.time()
    nbrGames = 30
    listScores = [[],[]]
    for k in range(nbrGames) :
        finishedGrid = single_AI()
        maxObtainedValue = evaluateGrid(finishedGrid)
        if ( maxObtainedValue not in listScores[0][:]) :
            listScores[0].append(maxObtainedValue)
            listScores[1].append(1)
        else :
            listScores[1][listScores[0].index(maxObtainedValue)] += 1
        print("Partie", k+1, "sur", nbrGames)
    endTime = time.time()
    print(" \n----- Parties finies -----")
    print("Temps écoulé :", int((endTime-startTime)*1000), "ms")
    print(np.array(listScores))
    print("--------------------------")
    #plot a bar graph
    width = 30
    plt.bar(listScores[0], listScores[1], width)
    plt.show()
