
import pygame
from sudoku import Board

class SudokuGUI():

    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Sudoku GUI')
        self._screen = pygame.display.set_mode((286,286))
        self._RUNNING = True
        self._board = Board((9,9))
        self.makeBoard()
        self._board.printBoard()

    def solveBoard(self):
        self._board.solve(self.animate)
        self.makeBoard()

    def animate(self):
        self.makeBoard()
        self.draw()
        
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
            if event.type == pygame.KEYDOWN and event.key==pygame.K_SPACE:
                self.solveBoard()

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


g =SudokuGUI()
g.runGameLoop()
