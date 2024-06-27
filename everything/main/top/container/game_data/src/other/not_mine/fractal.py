import pygame
import math
def findLocation(start, dir, dist):
    x = start[0] + (math.cos(dir) * dist)
    y = start[1] + (math.sin(dir) * dist)
    return [x,y]
    
white_color = [255,255,255]
class Line:

    def __init__(self, start, end):
        self.start = start
        self.end = end
    def draw(self, screen):
        pygame.draw.line(screen, white_color, self.start, self.end, 1)

pygame.init
window = pygame.display.set_mode((1200, 800))

def drawFractal(degree):
    window.fill((20, 20, 20))

    lines = []
    lines.append(Line([0,700], [1200,700]))
    newLines = []
    for i in range(degree):
        for line in lines:
            
            lineXDifference = line.end[0] - line.start[0]
            lineYDifference = line.end[1] - line.start[1]
            lineLength = pow(pow(lineXDifference, 2) + pow(lineYDifference, 2),0.5)
            lineDirection = math.atan2(lineYDifference, lineXDifference)
            lineMidPoint = [lineXDifference / 2 + line.start[0], lineYDifference / 2 + line.start[1]]
            firstThird = Line(line.start, [line.start[0] + lineXDifference / 3,line.start[1] + lineYDifference / 3])
            lastThird = Line([line.end[0] - lineXDifference / 3,line.end[1] - lineYDifference/3],line.end)
            slopeUp = Line(firstThird.end,findLocation(lineMidPoint, lineDirection + math.radians(-90), lineLength/3))
            slopeDown = Line(slopeUp.end, lastThird.start)
            newLines.append(firstThird)
            newLines.append(lastThird)
            newLines.append(slopeUp)
            newLines.append(slopeDown)
            
        lines = newLines
        newLines = []
        
    # pygame.draw.line(window, white_color, [0,700], [1200,700], 5)
    for line in lines:
        line.draw(window)
    pygame.display.update()

running = True

DIVIDE = pygame.USEREVENT + 1

pygame.time.set_timer(DIVIDE, 1250)  # 1000 milliseconds is 1 seconds.
degree = 0
while running:
    drawFractal(degree)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == DIVIDE:
            degree = min(degree + 1, 7)

    
            