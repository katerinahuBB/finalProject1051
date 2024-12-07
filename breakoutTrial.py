import pygame
from pygame.locals import *
from random import randint
from ball import Ball
#music mode
from pygame import mixer






pygame.init()


screenWidth = 500
screenHeight = 650






screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("PyBreak Arcade Game")


#code for bckground
background = pygame.image.load("background.png")
#to change bckground colors use code below
bg = (0,0,0) #use diff numbers


#Code for background music
mixer.music.load("gamemusic.mp3")
mixer.music.play()


#block colors the ones that the ball destroys
red = (255, 0, 0)
pink = (255, 105, 180)
orange = (255, 165, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (255, 0, 255)
white = (255,255,255)
black = (0,0,0)


cols= 5
rows= 4


clock = pygame.time.Clock()
fps = 60


#platform variables
platformWidth = 100
platformHeight = 10
platformPos = [screenWidth // 2 - platformWidth // 2, screenHeight - platformHeight - 10]
platformSpeed = 10
platformColor = pink
platformOutline = (100,100,100)


#create ball variables
# OBJECTS
ballX = 250
ballY = 540
ballXspeed = 2
ballYspeed = 2
ballRadius = 15
ballColor = purple
ball = Ball(ballX, ballY, ballRadius, ballColor, ballXspeed, ballYspeed, screen)




#brick wall class
class wall():
   def __init__(self):
       self.width = screenWidth // cols
       self.height = 50
       self.blocks = []


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
               if row <1:
                   strength = 4
               elif row <2:
                   strength = 3
               elif row <3:
                   strength = 2
               elif row <4:
                   strength = 1
              
              
              
               blockInd = [rect, strength]
               blockRow.append(blockInd)
           self.blocks.append(blockRow)




   def drawWall(self): #color = based on strength
       for row in self.blocks:
           for block in row:
               if block[1] ==4:
                   blockCol = red
               elif block[1] ==3:
                   blockCol = green
               elif block[1] ==2:
                   blockCol = blue
               elif block[1] ==1:
                   blockCol = purple
               pygame.draw.rect(screen, blockCol, block[0])
               pygame.draw.rect(screen, black, (block[0]), 2)
  
   def checkCollision(self,ball):
        for row in self.blocks:
             for block in row:
                  brick_rect=block[0]
                  if brick_rect.collidepoint(ball.x, ball.y-ball.radius)or brick_rect.collidepoint(ball.x,ball.y+ball.radius):
                       block[1]-=1
                       if block[1]<=0:
                            row.remove(block)
                       ball.bounce_y()
                       return True
        return False


#create platform
class platform():
   def __init__(self):
       self.reset()




   def move(self):
       #reset movement direction
       self.direction = 0
       key = pygame.key.get_pressed()
       if key[pygame.K_LEFT] and self.rect.left > 0:
           self.rect.x -= self.speed
           self.direction = -1
       if key[pygame.K_RIGHT] and self.rect.right < screenWidth:
           self.rect.x += self.speed
           self.direction = 1


   def draw(self):
       pygame.draw.rect(screen, pink, self.rect)
       pygame.draw.rect(screen, platformOutline, self.rect, 3)




   def reset(self):
       #define platform variables
       self.height = 20
       self.width = int(screenWidth / cols)
       self.x = int((screenWidth / 2) - (self.width / 2))
       self.y = screenHeight - (self.height * 2)
       self.speed = 10
       self.rect = Rect(self.x, self.y, self.width, self.height)
       self.direction = 0
#code for score
class score:
    def __init__(self,x,y,color,screen):
         self.screen=screen
         self.color=color
         self.x=x
         self.y=y
         self.score=0
    def update(self,points):
         self.score+=points
    def draw(self):
         font=pygame.font.Font("Times New Roman",45)
         score_text=font.render(f"Your current score: {self.score}",True,self.color)
         self.screen.blit(score_text,(self.x,self.y))




wall = wall()
wall.createWall()


playerPlatform = platform()






run = True
while run:




   #add bckground here
   screen.fill(bg)
   #add background image
   screen.blit(background,(0,0))
   #the wall
   wall.drawWall()
   #slow down platform
   clock.tick(fps)
   #add platform
   playerPlatform.draw()
   playerPlatform.move()
   #create ball
   ball.move()
   # Check if ball hits the x-axis above
   ball.check_for_contact_on_x()
  # Check if ball hits y-axis on the side
   ball.check_for_contact_on_y()
  # Check if ball hits platform
   if (playerPlatform.rect.y < ball.y + ball.radius < playerPlatform.rect.y + playerPlatform.height
         and
       playerPlatform.rect.x < ball.x + ball.radius < playerPlatform.rect.x + playerPlatform.width):
       ball.bounce_y()
       ball.y = playerPlatform.y - ball.radius
   #check if ball hits wall
   for row in wall.blocks:
       for block in row:
           brick_rect = block[0]
           if brick_rect.collidepoint(ball.x, ball.y - ball.radius) or brick_rect.collidepoint(ball.x, ball.y + ball.radius):
               block[1] -= 1  # Decrease brick strength
               if block[1] <= 0:
                   row.remove(block)  # Remove brick if strength is 0
               ball.bounce_y()
   for event in pygame.event.get():
       if event.type ==pygame.QUIT:
           run = False
#scoreboard
   for event in pygame.event.get():
           if event.type ==pygame.QUIT:
               run = False






   pygame.display.update()


pygame.quit()
