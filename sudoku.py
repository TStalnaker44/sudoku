import pprint, math, random

class Board():

    def __init__(self, dimensions=(9,9)):

        self._height = dimensions[1]
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

        # Create empty spaces
        tileNum  = self._width*self._height
        emptyNum = int(tileNum * 0.63)
        spaces = random.sample(range(1, tileNum), emptyNum)
        for space in spaces:
            row = space // self._width
            column = space % self._width
            self._board[row][column] = 0

    def solve(self):
        # Initialize the move stack
        moveStack = []

        initialEmptySpaces = []
        for row in range(self._height):
            for column in range(self._width):
                if self._board[row][column] == 0:
                    index = (self._width * row) + column
                    initialEmptySpaces.append(index)

##        print(initialEmptySpaces)
##        print(len(initialEmptySpaces))
        
        # Find the initial empty space
        index = initialEmptySpaces[0]
        prevIndex = index
        row = index // self._width
        column = index % self._width
            
        # Push initial moves to the stack
        for x in range(1, self._width+1):
            moveStack.append(Move(x, (row,column)))

        #print(moveStack)
        
        while not self.isSolved():

            # Pop a move off the stack
            try:
                move = moveStack.pop()
            except:
                print("Broken")
                self.printBoard()
                break

##            print("-"*25)
            # Pop the stack until you find a valid move
            while not self.validPlacement(move._entry, move._coords):
                try:
                    move = moveStack.pop()
                except:
                    print("Broken")
                    return 0
                #Reset entry currently at that position to 0
                self._board[move._coords[0]][move._coords[1]] = 0
                newIndex = (move._coords[0] * self._width) + move._coords[1]
                if prevIndex > newIndex:
                    start = initialEmptySpaces.index(newIndex)
                    end = initialEmptySpaces.index(prevIndex) + 1
                    for i in initialEmptySpaces[start:end]:
                        r = i // self._width
                        c = i % self._width
                        self._board[r][c] = 0
##                self.printBoard()
##            print("-"*25)
                
            # Add the new entry to the board        
            self._board[move._coords[0]][move._coords[1]] = move._entry

            # Save the index of the previous move
            prevIndex = index

            # Determine the index / coordinates for the next move
            index = (move._coords[0] * self._width) + move._coords[1]
            row, column = 0, 0 #Initialize variables outside of loop
            while True:
                row = index // self._width
                column = index % self._width
                if index >= self._width*self._height or \
                   self._board[row][column] == 0:
                    break
                index += 1

##            print(row, column)
                
            # Determine the available numbers to fill space
            availNums = [x for x in range(1,self._width+1)]

            # Add all potential moves to the stack
            random.shuffle(availNums)
            for num in availNums:
                moveStack.append(Move(num, (row, column)))

##            self.printBoard()
           # print(moveStack)
            
 
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



##b = Board((9,9))
##b.printBoard()
##print(Move(4, (0,0)))
##print(repr(Move(4, (0,0))))
##b.solve()
##b.printBoard()
print("Running...")
for x in range(100):
    b = Board((9,9))
    code = b.solve()
    if code == 0:
        print("Oof")
print("Done")
