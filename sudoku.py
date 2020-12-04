import pprint, math, random

class Board():

    def __init__(self, dimensions=(9,9)):

        self._height = dimensions[1]
        self._width  = dimensions[0]
        
        self._board = [[0 for x in range(self._width)]
                       for x in range(self._height)]
        
        self.createBoard()

    def createBoard(self):
        
        # Create board by solving an empty board
        self.solve()

        # Create empty spaces
        tileNum  = self._width*self._height
        emptyNum = int(tileNum * 0.63)
        spaces = random.sample(range(1, tileNum), emptyNum)
        for space in spaces:
            row = space // self._width
            column = space % self._width
            self._board[row][column] = 0

    def solve(self, displayFunction=None):
        # Initialize the move stack
        moveStack = []

        initialEmptySpaces = []
        for row in range(self._height):
            for column in range(self._width):
                if self._board[row][column] == 0:
                    index = (self._width * row) + column
                    initialEmptySpaces.append(index)
        
        # Find the initial empty space
        index = initialEmptySpaces[0]
        prevIndex = index
        row = index // self._width
        column = index % self._width
            
        # Push initial moves to the stack
        for x in range(1, self._width+1):
            moveStack.append(Move(x, (row,column)))
        
        while not self.isSolved():

            move = moveStack.pop()
            if displayFunction != None: displayFunction()

            # Pop the stack until you find a valid move
            while not self.validPlacement(move._entry, move._coords):

                move = moveStack.pop()

                #Reset the board state, removing previous bad moves
                newIndex = (move._coords[0] * self._width) + move._coords[1]
                startPos = initialEmptySpaces.index(newIndex)
                for i in initialEmptySpaces[startPos:]:
                    r = i // self._width
                    c = i % self._width
                    self._board[r][c] = 0

                if displayFunction != None: displayFunction()

            # Add the new entry to the board        
            self._board[move._coords[0]][move._coords[1]] = move._entry

            # Determine the index / coordinates for the next move
            index = (move._coords[0] * self._width) + move._coords[1]
            nextSpace = min(initialEmptySpaces.index(index) + 1,
                            len(initialEmptySpaces)-1)
            index = initialEmptySpaces[nextSpace]
            row = index // self._width
            column = index % self._width
                     
            # Determine the available numbers to fill space
            availNums = [x for x in range(1,self._width+1)]

            # Add all potential moves to the stack
            random.shuffle(availNums)
            for num in availNums:
                moveStack.append(Move(num, (row, column)))

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

    def isSolved(self):
        return not 0 in [e for row in self._board for e in row]

class Move():

    def __init__(self, entry, coords):
        self._entry = entry
        self._coords = coords

    def __str__(self):
        return f"Move: {self._entry} @ {self._coords}"

    def __repr__(self):
        return f"Move({self._entry}, {self._coords})"


print("Running...")
for x in range(1):
    b = Board((9,9))
    b.solve(b.printBoard)
print("Done")
