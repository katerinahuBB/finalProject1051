import pygame
import random
import sys
from pygame.locals import *

pygame.init()

screenWidth = 500
screenHeight = 500
platformWidth = 100
platformHeight = 10
ballRadius = 20

font = pygame.font.Font(None, 36)
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("PyBreak Arcade Game")

#to change bckground colors use code below
bg = (0,0,0) #use diff numbers

#block colors the ones that the ball destroys
blockRed = (255, 0, 0)
pink = (255, 105, 180)
blockOrange = (255, 165, 0)
white = (255, 255, 255)
blockGreen = (0, 255, 0)
blue = (0, 0, 255)
blockPurple = (255, 0, 255)

cols= 5
rows= 4

#create ball
ball_pos = [screenWidth // 2, screenHeight // 2]
ball_speed = [random.uniform(2, 4), random.uniform(2, 4)]  # Faster starting speed
platformPos = [screenWidth // 2 - platformWidth // 2, screenHeight - platformHeight - 10]
platformSpeed = 10
score = 0
lives = 3
current_level = 1
platformColor = pink


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


def start_screen():
    screen.fill(bg)
    show_text_on_screen("Bouncing Ball Game", 50, platformWidth // 4)
    show_text_on_screen("Press any key to start...", 30, platformHeight // 3)
    show_text_on_screen("Move the platform with arrow keys...", 30, platformHeight // 2)
    pygame.display.flip()
    wait_for_key()

def game_over_screen():
    screen.fill(bg)
    show_text_on_screen("Game Over", 50, platformHeight // 3)
    show_text_on_screen(f"Your final score: {score}", 30, platformHeight // 2)
    show_text_on_screen("Press any key to restart...", 20, platformHeight * 2 // 3)
    pygame.display.flip()
    wait_for_key()

def victory_screen():
    screen.fill(bg)
    show_text_on_screen("Congratulations!", 50, platformHeight // 3)
    show_text_on_screen(f"You've won with a score of {score}", 30, platformHeight // 2)
    show_text_on_screen("Press any key to exit...", 20, platformHeight * 2 // 3)
    pygame.display.flip()
    wait_for_key()

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def show_text_on_screen(text, font_size, y_position):
    font = pygame.font.Font(None, font_size)
    text_render = font.render(text, True, white)
    text_rect = text_render.get_rect(center=(platformWidth // 2, y_position))
    screen.blit(text_render, text_rect)

def changePlatColor():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


run = True
while run:

    #add bckground here
    screen.fill(bg)
    #the wall
    wall.drawWall()

    #draw platform
    pygame.draw.rect(screen, platformColor, (int(platformPos [0]), int(platformPos[1]), platformWidth, platformHeight))

    # Draw the ball
    pygame.draw.circle(screen, white, (int(ball_pos[0]), int(ball_pos[1])), ballRadius)

    info_line_y = 10  # Adjust the vertical position as needed
    info_spacing = 75

    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()


    # Move the platform
    platformPos[0] += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * platformSpeed
    platformPos[1] += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * platformSpeed

    # Ensure the platform stays within the screen boundaries
    platformPos[0] = max(0, min(platformPos[0], screenWidth - platformWidth))
    platformPos[1] = max(0, min(platformPos[1], screenWidth - platformHeight))

    # Move the ball
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Bounce off the walls
    if ball_pos[0] <= 0 or ball_pos[0] >= screenWidth:
        ball_speed[0] = -ball_speed[0]

    if ball_pos[1] <= 0:
        ball_speed[1] = -ball_speed[1]

    # Check if the ball hits the platform
    if (
        platformPos[0] <= ball_pos[0] <= platformPos[0] + platformWidth
        and platformPos[1] <= ball_pos[1] <= platformPos[1] + platformHeight
    ):
        ball_speed[1] = -ball_speed[1]
        score += 1

    # Check if the player advances to the next level
    if score >= current_level * 10:
        current_level += 1
        ball_pos = [screenWidth // 2, screenHeight // 2]
        ball_speed = [random.uniform(2, 4), random.uniform(2, 4)]  # Randomize the ball speed
        platform_color = changePlatColor()

    # Check if the ball falls off the screen
    if ball_pos[1] >= screenHeight:
        # Decrease lives
        lives -= 1
        if lives == 0:
            game_over_screen()
            start_screen()  # Restart the game after game over
            score = 0
            lives = 3
            current_level = 1
        else:
            # Reset the ball position
            ball_pos = [screenWidth // 2, screenHeight // 2]
            # Randomize the ball speed
            ball_speed = [random.uniform(2, 4), random.uniform(2, 4)]


    # Draw the score in an orange rectangle at the top left
    score_text = font.render(f"Score: {score}", True, white)
    score_rect = score_text.get_rect(topleft=(10, info_line_y))
    pygame.draw.rect(screen, pink, score_rect.inflate(10, 5))
    screen.blit(score_text, score_rect)

    # Draw the level indicator in a light-blue rectangle at the top left (next to the score)
    level_text = font.render(f"Level: {current_level}", True, white)
    level_rect = level_text.get_rect(topleft=(score_rect.topright[0] + info_spacing, info_line_y))
    pygame.draw.rect(screen, blue, level_rect.inflate(10, 5))
    screen.blit(level_text, level_rect)

    # Draw the lives in a red rectangle at the top left (next to the level)
    lives_text = font.render(f"Lives: {lives}", True, white)
    lives_rect = lives_text.get_rect(topleft=(level_rect.topright[0] + info_spacing, info_line_y))
    pygame.draw.rect(screen, pink, lives_rect.inflate(10, 5))
    screen.blit(lives_text, lives_rect)

    # Update the display
    #pygame.display.flip()        

    pygame.display.update()

pygame.quit