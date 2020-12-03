import pprint
import math
import random

class Board():

    def __init__(self, dimensions=(9,9)):

        self._height = dimensions[0]
        self._width  = dimensions[0]
        
        self._board = [[0 for x in range(self._width)]
                       for x in range(self._height)]
        
        self.createBoard()

    def createBoard(self):
        # Initialize the move stack
        moveStack = []
        
        # Create a seed move
        moveStack.append(Move(random.randint(1,self._width+1), (0,0)))
        
        while self._board[self._height-1][self._width-1] == 0:

            # Pop a move off the stack
            move = moveStack.pop() 

            # Pop the stack until you find a valid move
            while not self.validPlacement(move._entry, move._coords):
                move = moveStack.pop()
                #Reset entry currently at that position to 0
                self._board[move._coords[0]][move._coords[1]] = 0
                
            # Add the new entry to the board        
            self._board[move._coords[0]][move._coords[1]] = move._entry

            # Determine the index / coordinates for the next move
            index = (move._coords[0] * self._width) + move._coords[1]
            index += 1 #increment the index
            row = index // self._width
            column = index % self._width

            # Determine the available numbers to fill space
            availNums = [x for x in range(1,self._width+1)]

            # Add all potential moves to the stack
            random.shuffle(availNums)
            for num in availNums:
                moveStack.append(Move(num, (row, column)))

            
        
        


        
##        for row in range(self._height):
##            potential = [x for x in range(1,self._width)]
##            random.shuffle(potential)
##            validRow = all([self.validPlacement(e, (row, column))
##                         for column, e in enumerate(potential)])
##            while not validRow:
##                random.shuffle(potential)
##                validRow = all([self.validPlacement(e, (row, column))
##                         for column, e in enumerate(potential)])
##            self._board[row] = potential
##
##            print(self._board)

##        potential = [x for x in range(1,10)]
##            for column in range(self._width):
##                e = 0
##                while not self.validPlacement(e, (row, column)):
##                    e = random.choice(potential)
##                self._board[row][column] = e
##                potential.remove(e)
        
    def validPlacement(self, e, coords):
        inRow = e in self.getRow(coords[0])
        inColumn = e in self.getColumn(coords[1])
        quadCoords = self.findQuadrantByEntry(*coords)
        inQuad = e in self.getNumbersInQuadrant(*quadCoords)
        return not inRow and not inColumn and not inQuad

    def getAt(self, row, column):
        return self._board[row][column]

    def getRow(self, row):
        return self._board[row]

    def getColumn(self, column):
        return [row[column] for row in self._board]

    def printBoard(self):
        pprint.pprint(self._board)

    def getNumbersInQuadrant(self, r, c):
        q = self.getQuadrant(r, c)
        return [e for row in q for e in row ]
            
    def getQuadrant(self, r, c):
        q_r = r * int(math.sqrt(self._height))
        q_c = c * int(math.sqrt(self._width))
        quadWidth = int(math.sqrt(self._width))
        quadHeight = int(math.sqrt(self._height))
        return [row[q_c:q_c+quadWidth] for row in
                self._board[q_r:q_r+quadHeight]]

    def findQuadrantByEntry(self, row, column):
        r = row // int(math.sqrt(self._height))
        c = column // int(math.sqrt(self._width))
        return (r, c)

class Move():

    def __init__(self, entry, coords):
        self._entry = entry
        self._coords = coords

    def __repr__(self):
        return f"{self._entry} : {self._coords}"



b = Board((16,16))
b.printBoard()
