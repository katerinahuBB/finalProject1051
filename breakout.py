import pygame
from pygame.locals import *

pygame.init()

screenWidth = 500
screenHeight = 500

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("PyBreak Arcade Game")

#to change bckground colors use code below
bg = (0,0,0) #use diff numbers

#block colors the ones that the ball destroys
blockRed = (255, 0, 0)
#blockPink = (255, 105, 180)
blockOrange = (255, 165, 0)
#blockYellow = (255, 255, 0)
blockGreen = (0, 255, 0)
#blockBlue = (0, 0, 255)
blockPurple = (255, 0, 255)

cols= 5
rows= 4

#brick wall class
class wall():
    def __init__(self):
        self.width = screenWidth // cols
        self.height = 50

    def createWall(self):
        self.blocks = []
        blockInd = []
        for row in range(rows):
            blockRow = []
            for col in range(cols): #iterate through the cols
                blockX = col * self.width #create x and y, create rect
                blockY = row * self.height
                rect = pygame.Rect(blockX, blockY, self.width, self.height)
                #making bricks stronger/harder to break below
                if row <2:
                    strength = 1
                elif row <4:
                    strength = 2
                
                
                
                blockInd = [rect, strength]
                blockRow.append(blockInd)
            self.blocks.append(blockRow)


    def drawWall(self): #color = based on strength
        for row in self.blocks:
            for block in row:
                if block[1] ==4:
                    blockCol = blockRed
                elif block[1] ==3:
                    blockCol = blockOrange
                elif block[1] ==2:
                    blockCol = blockGreen
                elif block[1] ==1:
                    blockCol = blockPurple
                pygame.draw.rect(screen, blockCol, block[0])
                pygame.draw.rect(screen, bg, (block[0]), 2)

wall = wall()
wall.createWall()

run = True
while run:

    #add bckground here
    screen.fill(bg)
    #the wall
    wall.drawWall()

    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit