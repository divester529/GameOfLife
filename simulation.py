import pygame, sys, time
from pygame.locals import *

TILES = [
    (255, 255, 255), # Empty
    (0, 0, 0), # Alive
]

MIN_FPS = 4
MAX_FPS = 120

class GameOfLife:
    def __init__(self, width, height, display):
        self.font = pygame.font.SysFont('Calibri B', 30)
        self.clock = pygame.time.Clock()

        self.width = width
        self.height = height
        self.display = display

        self.simulating = False
        self.grid_size = 32
        self.fps = 30
        self.offset = (0, 0)
        self.grid = [[0 for y in range(height)] for x in range(width)]

        self.alive = 0
        self.gen = 0

        self.aliveMessage = self.font.render(str(self.alive)+" Alive", True, (255, 0, 0), (248, 240, 176))
        self.statusMessage = self.font.render('Not Simulating', True, (255, 0, 0), (248, 240, 176))
        self.fpsMessage = self.font.render("FPS: "+str(self.fps), True, (255, 0, 0), (248, 240, 176))
        self.controlsMessage = self.font.render('Space - Run Simulation    Esc - Clear board    Right Click - Toggle Cell    WASD - Move Camera    Scrollwheel - Scroll    +/- - FPS', True, (255, 0, 0), (248, 240, 176))

    def getInput(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    shifted = (pos[0]-(self.offset[0]*self.grid_size), pos[1]-(self.offset[1]*self.grid_size))
                    (x, y) = tuple(z//self.grid_size for z in shifted)

                    if x in range (0, self.width) and y in range (0, self.height):
                        self.grid[x][y]= not self.grid[x][y]

                        if self.grid[x][y] == 1:
                            self.alive += 1
                            self.aliveMessage = self.font.render(str(self.alive)+" Alive", True, (255, 0, 0), (248, 240, 176))

                if event.button == 4:
                    self.grid_size += 1
                if event.button == 5:
                    self.grid_size -=1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.setSimulating(not self.simulating)

                if event.key == pygame.K_ESCAPE:
                    self.setSimulating(False)
                    self.alive = 0
                    self.aliveMessage = self.font.render(str(self.alive)+" Alive", True, (255, 0, 0), (248, 240, 176))
                    self.grid = [[0 for y in range(self.height)] for x in range(self.width)]
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.offset = (self.offset[0], self.offset[1]+1)
            if keys[pygame.K_s]:
                self.offset = (self.offset[0], self.offset[1]-1)
            if keys[pygame.K_a]:
                self.offset = (self.offset[0]+1, self.offset[1])
            if keys[pygame.K_d]:
                self.offset = (self.offset[0]-1, self.offset[1])
            if keys[pygame.K_KP_PLUS]:
                self.setFps(self.fps+1)
            if keys[pygame.K_KP_MINUS]:
                self.setFps(self.fps-1)
            

    def setSimulating(self, value):
        self.simulating=value

        if value == True:
            self.statusMessage = self.font.render('Running Simulation', True, (0, 255, 0), (248, 240, 176))
        else:
            self.statusMessage = self.font.render('Not Simulating', True, (255, 0, 0), (248, 240, 176))

    def setFps(self, value):
        if value > MIN_FPS and value < MAX_FPS:
            self.fps = value
            self.fpsMessage = self.font.render("FPS: "+str(self.fps), True, (255, 0, 0), (248, 240, 176))

    def isSimulating(self):
        return self.simulating

    def runSimulation(self):
        new_grid = [[0 for y in range(self.height)] for x in range(self.width)]
        self.alive = 0

        for y in range(0, self.height):
            for x in range(0, self.width):
                neighbors = 0

                for v in range(y-1, y+2):
                    if v < 0 or v >= self.height:
                        continue
                    for u in range(x-1, x+2):
                        if u < 0 or u >= self.width:
                            continue
                        if u==x and v==y:
                            continue
                        if self.grid[u][v]==1:
                            neighbors += 1

                if self.grid[x][y] == 1:
                    if neighbors == 3 or neighbors == 2:
                        new_grid[x][y]=1
                        self.alive += 1
                    else:
                        new_grid[x][y]=0
                else:
                    if neighbors == 3:
                        new_grid[x][y]=1
                        self.alive += 1
                    else:
                        new_grid[x][y]=0
        
        self.grid = new_grid
        self.aliveMessage = self.font.render(str(self.alive)+" Alive", True, (255, 0, 0), (248, 240, 176))

    def tick(self):
        self.clock.tick(self.fps)

    def drawTile(self, x, y, value):
        pygame.draw.rect(self.display, TILES[value], pygame.Rect((self.offset[0]*self.grid_size)+self.grid_size*x, (self.offset[1]*self.grid_size)+self.grid_size*y, (7/8)*self.grid_size, (7/8)*self.grid_size))

    def drawGameboard(self):
        self.display.fill((0,0,0))

        for y in range(0, self.height):
            for x in range(0, self.width):
                self.drawTile(x, y, self.grid[x][y])

        self.display.blit(self.statusMessage, (0,0))
        self.display.blit(self.aliveMessage, (0, 30))
        self.display.blit(self.fpsMessage, (self.display.get_width()-90, 0))
        self.display.blit(self.controlsMessage, (10, self.display.get_height()-30))
        pygame.display.update()
