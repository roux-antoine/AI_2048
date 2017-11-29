
import numpy as np
import random
import time
import matplotlib.pyplot as plt

##CMA-ES

# class Neuron (object) :
#
#     def __init__ (self) :
#         """
#         """
#         self.grid = Grid()
#
#         for k in range (4) :
#             for i in range (4) :
#                 self.grid.grid[k,i] = random.randint(-10, 10)
#
#         self.fitnessValue = -1 #while unknown, it is set to -1
#
#
#     def evaluate (self) :
#         """ Attributes the rawScore as fitness
#             Doesnt return anything
#         """
#         self.fitness = sum(sum(self.grid.grid))


######################################   Classes   #########################################

class Grid (object) :

    def __init__ (self, givenGrid, givenFitnessGrid) :
        """
        """
        # self.grid = np.array([[0, 0, 0, 0],
        #                       [0, 0, 0, 0],
        #                       [0, 0, 0, 0],
        #                       [0, 0, 0, 0]])
        self.grid = np.array(givenGrid)
        # self.fitnessGrid = np.array([[8,  4, 2, 1],
        #                                  [16,  8, 4, 2],
        #                                  [32,  16, 8, 4],
        #                                  [64, 32, 16, 8]])
        self.fitnessGrid = givenFitnessGrid

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
                if currentColumn[lineNbr] == currentColumn[lineNbr+1] and currentColumn[lineNbr] != 0 :
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
        # fitnessGrid = [[64,  16, 4, 1],  #a peu près pareil
        #                 [256,  64, 16, 4],
        #                 [1024,  256, 64, 16],
        #                 [4096, 1024, 256, 64]]

        ## pas nécessairement plus lent...
        # fitness = 0
        # for k in range(4) :
        #     for i in range (4) :
        #         fitness += self.grid[k,i] * self.fitnessGrid[k][i]

        fitness = sum(sum(np.multiply(self.grid, self.fitnessGrid)))
        return (fitness)

class Generation (object) :

    def __init__ (self, givenSizeOfPopulation) :
        """
        """
        self.sizeOfPopulation = givenSizeOfPopulation
        self.individuals = []
        self.fitnesses = []

        for k in range(givenSizeOfPopulation) :
            fitnessGrid = np.array([[0, 0, 0, 0],
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 0]])
            for i in range (4) :
                for j in range (4) :
                    fitnessGrid[i,j] = random.randint(0, 10)

            self.individuals.append(Grid([[0, 0, 0, 0],
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 0]],
                                          fitnessGrid))


    def __str__ (self) :
        for k in range(self.sizeOfPopulation) :
            print(self.individuals[k])
            # print(self.individuals[k].fitnessGrid)
            # print("--------------")
        return ("")

    def evaluate(self, nbrIterations) :
        """ Fills the fitnesses array
            Doesnt return anything
        """
        for k in range(self.sizeOfPopulation) :
            currentFitness = 0
            for i in range(nbrIterations) :
                print("k, i =", k, i)
                finishedGrid = single_AI(self.individuals[k].grid, self.individuals[k].fitnessGrid)
                currentFitness += sum(sum(finishedGrid))
            self.fitnesses.append(int(currentFitness / nbrIterations))

    def select (self, proportionOfBest, proportionOfOthers) :
        """ Selects the x best individuals from the generation
            Selects also y individuals randomly selected

        """
        assert proportionOfBest + proportionOfOthers < 1

        nbrOfBest = int((self.sizeOfPopulation) * proportionOfBest)
        nbrOfOthers = int((self.sizeOfPopulation) * proportionOfOthers)
        indexes = []

        for k in range(nbrOfBest) :
            currentMaxIndex = self.fitnesses.index(max(self.fitnesses))
            indexes.append(currentMaxIndex)
            self.fitnesses[currentMaxIndex] = 0

        for k in range (nbrOfOthers) :
            randomlySelected = random.randint(0, self.sizeOfPopulation-1)
            while randomlySelected in indexes : #if already one of the best, try again
                randomlySelected = random.randint(0, self.sizeOfPopulation-1)
            indexes.append(randomlySelected)

        self.fitnesses = [] #we reset the fitnesses

        #we delete the individuals not selected
        for k in range(self.sizeOfPopulation) :
            if k not in indexes :
                self.individuals[k] = 0

        return(indexes)

    def mutate (self, indexes, probability) :
        """ Mutates the selected individuals
            indexes = indexes of the selected
            Doesnt return anything
        """
        for k in indexes :
            if random.randint(1, int(1/probability)) == 1 :
                #in this case we add a small noise to the grid, proportional to the tile values
                for i in range(4) :
                    for j in range(4) :
                        tileValue = self.individuals[k].grid[i,j]
                        self.individuals[k].fitnessGrid[i][j] += random.randint(-0.05 * tileValue, 0.05 * tileValue) #valeurs random....

    def reproduce (self, indexes) :
        """ The reproduction phase
            indexes = indexes of the selected
            At the moment : randomly mates the selected to fill up the blanks -> TROP VIOLENT ??
            Doesnt return anything
        """
        assert len(indexes) >= 2

        numberOfMissing = self.sizeOfPopulation - len(indexes)
        indexesOfMissing = []
        for k in range(self.sizeOfPopulation) :
            if k not in indexes :
                indexesOfMissing.append(k)

        for k in indexesOfMissing :
            parent1 = random.choice(indexes)
            parent2 = random.choice(indexes)
            while (parent2 == parent1) :
                parent2 = random.choice(indexes)

            self.individuals[k] = Grid([[0, 0, 0, 0],
                                          [0, 0, 0, 0],
                                          [0, 0, 0, 0],
                                          [0, 0, 0, 0]] ,

                                          [[0, 0, 0, 0],
                                          [0, 0, 0, 0],
                                          [0, 0, 0, 0],
                                          [0, 0, 0, 0]])
            for i in range(4) :
                for j in range(4) :
                    self.individuals[k].fitnessGrid[i][j] = 0.5 * (self.individuals[parent1].grid[i,j] + self.individuals[parent2].grid[i,j])



######################################  Variables   #########################################

arrayGrid = [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0]]


# MODE = "PLAY"
# MODE = "TEST"
# MODE = "AI"
# MODE = "MULTI_AI"
MODE = "GENETIC"

######################################  Fonctions  ##########################################
def evaluateGrid(givenGrid) :
    """ Returns the max value of the grid
    """
    return(givenGrid.max())

def single_AI(givenGrid, givenFitnessGrid) :
    myGrid = Grid(givenGrid, givenFitnessGrid)
    myGrid.addNbr()
    myGrid.addNbr()

    while True :
        fitnessGrid = np.array([[0, 0, 0, 0], #lignes = à 1er move constant
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

            # if np.count_nonzero(myGrid.grid[:,0]) != 0 :
            #     #if first line is not full, do not swipe up
            #     #PAS SUFFISANT CAR MM SI LA LIGNE EST PLEINE SWIPER PEUT AVOIR UN EFFET
            #     #EN PLUS CA DIMINUE LE MEILLEUR SCORE...
            #     consideredMovesArray = [2, 3]

            for k in consideredMovesArray :
                for i in range (4) :
                    tempGrid = Grid(myGrid.grid, myGrid.fitnessGrid)
                    if tempGrid.canSwipe(k) :
                        tempGrid.swipe(k)
                        if tempGrid.canSwipe(i) :
                            tempGrid.swipe(i)
                            fitnessGrid[k][i] = tempGrid.calcFitness()



            maxArray = [0,0,0,0]
            for k in range (4) :
                maxArray[k] = max(fitnessGrid[k])
                # maxArray[k] = fitnessGrid[k].mean() #moins bon que le max

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

            ##useful for debugging and seeing what is happening:
            # print(myGrid)
            # print(fitnessGrid)
            # print(maxArray)
            # print(direction2)
            # user_input = input()

            myGrid.swipe(direction2) #mettre direction pour swiper sans avoir reverse l'array
            myGrid.addNbr()

        else : #if no move is possible
            return(myGrid.grid)
            break


######################################   Main   ###########################################


if MODE == "TEST" :
    # myGrid = Grid(arrayGrid3)
    # print(myGrid.canSwipe(3))
    myGrid = Grid(arrayGrid)

    print(single_AI(myGrid))
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

# if MODE == "AI" :
#     startTime = time.time()
#     finishedGrid = single_AI()
#     endTime = time.time()
#     print(" \n----- Partie finie -----")
#     print("Temps écoulé :", int((endTime-startTime)*1000), "ms")
#     print("Valeur max :", evaluateGrid(finishedGrid))
#     print("Score brut :", sum(sum(finishedGrid)))
#     print(Grid(finishedGrid))
#     print("------------------------")

# if MODE == "MULTI_AI" :
#     startTime = time.time()
#     nbrGames = 10
#     listScores = [[],[]]
#     sumRawScores = 0
#     for k in range(nbrGames) :
#         finishedGrid = single_AI()
#         sumRawScores += sum(sum(finishedGrid))
#         maxObtainedValue = evaluateGrid(finishedGrid)
#         if (maxObtainedValue not in listScores[0][:]) :
#             listScores[0].append(maxObtainedValue)
#             listScores[1].append(1)
#         else :
#             listScores[1][listScores[0].index(maxObtainedValue)] += 1
#         print("Partie", k+1, "sur", nbrGames, " -  Score brut :", rawScore)
#     endTime = time.time()
#     print(" \n----- Parties finies -----")
#     print("Temps écoulé :", int((endTime-startTime)*1000), "ms")
#     print(np.array(listScores))
#     print("Temps par unité :", (endTime-startTime)/sumRawScores*1000, "ms")
#     print("--------------------------")
#     #plot a bar graph
#     width = 30
#     plt.bar(listScores[0], listScores[1], width)
#     plt.show()

if MODE == "GENETIC" :

    myGeneration = Generation(10)
    myGeneration.evaluate(10)
    indexes = myGeneration.select(0.3, 0)
    print(indexes)
    print(myGeneration)
    myGeneration. reproduce(indexes)
    print(myGeneration)
