"""
Author: Trevor Stalnaker
File: sudoku_gui.py
"""

import pygame, math
from sudoku import Board
from _thread import start_new_thread

class SudokuGUI():

    def __init__(self, n=9):
        assert math.sqrt(n).is_integer()
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Sudoku GUI')
        dim = 26 * (n+2) #pixelsPerSquare * (numSquares + padding)
        self._screen = pygame.display.set_mode((dim,dim))
        self._RUNNING = True
        self._board = Board(n)
        self.makeBoard()
        self._board.printBoard()
        self._solved = False
        self._solving = False

    def solveBoard(self):
        self._solving = True
        start_new_thread(self._solve, ())

    def quickSolve(self):
        self._solved = True
        self._board.solve()
        self.makeBoard()

    def _solve(self):
        self._board.altSolve(self.animate)
        self.makeBoard()
        self._solved = True

    def animate(self):
        self.makeBoard()
        
    def makeBoard(self):
        tiles = []
        for i, row in enumerate(self._board._board):
            for j, e in enumerate(row):
                x = (26 * (j+1))
                y = (26 * (i+1))
                entry = str(e) if e != 0 else ""
                tiles.append(SudokuTile((x,y),entry))
        self._tiles = tiles
        
    def draw(self):
        self._screen.fill((120,120,120))
        for t in self._tiles:
            t.draw(self._screen)
        pygame.display.flip()

    def handleEvents(self): 
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                self._RUNNING = False
            if not self._solved:
                if not self._solving:
                    if event.type == pygame.KEYDOWN and event.key==pygame.K_SPACE:
                        self.solveBoard()
                    if event.type == pygame.KEYDOWN and event.key==pygame.K_RETURN:
                        self.quickSolve()

    def runGameLoop(self):
        while self.isRunning():
            #self._gameClock.tick()
            self.draw()
            self.handleEvents()
            #self.update()
        pygame.quit()

    def isRunning(self):
        return self._RUNNING

class SudokuTile():

    def __init__(self, pos, entry):
        self._pos = pos
        self._entry = entry

        font = pygame.font.SysFont("Courier", 18)
        text = font.render(entry, True, (0,0,0))
        self._image = pygame.Surface((26,26))
        self._image.fill((0,0,0))
        whiteBackground = pygame.Surface((24,24))
        whiteBackground.fill((255,255,255))
        x = self._image.get_width()//2 - text.get_width()//2
        y = self._image.get_height()//2 - text.get_height()//2
        self._image.blit(whiteBackground, (1,1))
        self._image.blit(text, (x,y))

    def draw(self, screen):
        screen.blit(self._image, self._pos)


g =SudokuGUI(9)
g.runGameLoop()
