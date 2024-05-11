import pygame
import math

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 1 # scale
        self.rotation = 0 # not used
    
    def worldToScreenPoint(self,worldPosition: tuple,) -> tuple: # gets screen location of world coordinate
        width = pygame.display.get_window_size()[0]
        height = pygame.display.get_window_size()[1]
        x = ((worldPosition[0] - self.x) / max(self.z, 0.0001) / 1920) * width + (width / 2)
        y = ((worldPosition[1] - self.y) / max(self.z, 0.0001) / 1920) * width + (height / 2)
        return (x,y)
    
    def screenToWorldPoint(self,screenPosition: tuple) -> tuple: # gets world location of screen coordinate
        # may or may not be written by my bf, ChatGPT
        width = pygame.display.get_window_size()[0]
        height = pygame.display.get_window_size()[1]
        x = self.x + max(self.z, 0.0001) * (1920 * (screenPosition[0] - width / 2) / width)
        y = self.y + max(self.z, 0.0001) * (1920 * (screenPosition[1] - height / 2) / width)
        return (x, y)
    
    def scaleFactor(self) -> float:
        width = width = pygame.display.get_window_size()[0]
        return 1 / max(self.z, 0.0001) * width / 1920

class BoardRenderer:
    def __init__(self,camera=Camera()):
        self.camera = camera
        self.FPS = 30
        self.clock = pygame.time.Clock()
        self.backgroundColor = (0,0,0)
        self.onColor = (255,255,255)
        self.offColor = (25,25,25)
        self.cellSize = 50
        self.borderSize = 0

    def drawSquare(self,window,x,y,sideLength,color):
        scaleFactor = self.camera.scaleFactor()
        rect = pygame.Rect(0,0,sideLength * scaleFactor,sideLength * scaleFactor)
        screenPosition = self.camera.worldToScreenPoint((x,y))
        screenPosition = (round(screenPosition[0]),round(screenPosition[1]))
        rect.center = screenPosition
        #import random
        #color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        pygame.draw.rect(window,color,rect)

    def drawBoard(self,window,board: list[list[bool]]):
        for y,row in enumerate(board):
            for x,alive in enumerate(row):
                if alive:
                    color = self.onColor
                else:
                    color = self.offColor

                self.drawSquare(window, x * self.cellSize, y * self.cellSize, self.cellSize - (self.borderSize * 2), color)
    
    def tick(self,window,board):
        window.fill(self.backgroundColor)
        self.drawBoard(window,board)
        #pygame.display.update()
        self.clock.tick(self.FPS)