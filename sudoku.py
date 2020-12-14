"""
Author: Trevor Stalnaker
File: sudoku.py
"""

import pprint, math, random, time, copy

class Board():

    def __init__(self, n=9):

        assert math.sqrt(n).is_integer()

        self._n = n

        self._board = [[0 for x in range(self._n)]
                       for x in range(self._n)]
        
        self.createBoard()

    def createBoard(self, emptyTiles=None):
        
        # Create board by solving an empty board
        self.solve()

        # Create empty spaces
        tileNum  = self._n**2
        emptyNum = int(tileNum * 0.63) if emptyTiles == None else emptyTiles
        spaces = random.sample(range(1, tileNum), emptyNum)
        for space in spaces:
            row = space // self._n
            column = space % self._n
            self._board[row][column] = 0

    def solve(self, displayFunction=None):
        for row in range(self._n):
            for column in range(self._n):
                if self._board[row][column] == 0:
                    temp = [i for i in range(1, self._n+1)]
                    ##random.shuffle(temp)
                    for e in temp:
                        if self.validPlacement(e, (row, column)):
                            self._board[row][column] = e
                            if displayFunction != None: displayFunction()
                            self.solve(displayFunction)
                            if not self.isSolved():
                                self._board[row][column] = 0
                    return

    def findEmptySpaces(self):
        spaces = []
        for row in range(self._n):
            for column in range(self._n):
                if self._board[row][column] == 0:
                    spaces.append((row, column))
        return spaces
        
                    
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
        return [e for row in q for e in row]
            
    def getQuadrant(self, r, c):
        q_n = int(math.sqrt(self._n))
        q_r = r * q_n
        q_c = c * q_n
        return [row[q_c:q_c+q_n] for row in
                self._board[q_r:q_r+q_n]]

    def findQuadrantByEntry(self, row, column):
        q_n = int(math.sqrt(self._n))
        r = row // q_n
        c = column // q_n
        return (r, c)

    def isSolved(self):
        return not 0 in [e for row in self._board for e in row]


##b1 = Board()
##b2 = copy.deepcopy(b1)
##
##b1.printBoard()
##t = time.time()
##b1.solveStarter()
##b1.printBoard()
##print(time.time()-t)
##
##print("*"*45)
##
##b2.printBoard()
##t = time.time()
##b2.altSolve()
##b2.printBoard()
##print(time.time()-t)

