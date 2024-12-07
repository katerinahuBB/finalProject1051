import pygame
from pygame.locals import *
from random import randint
from ball import Ball
from pygame import mixer


pygame.init()

screenWidth = 500
screenHeight = 650

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("PyBreak Arcade Game")

# Code for background
background = pygame.image.load("background.png")
bg = (0, 0, 0)  # background color
# Code for background music
mixer.music.load("gamemusic.mp3")
mixer.music.play()
mixer.music.set_volume(0.15)

# Block colors
red = (255, 0, 0)
pink = (255, 105, 180)
orange = (255, 165, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (255, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)

cols = 5
rows = 4

game_active = False  # Set to False initially to show the start menu
clock = pygame.time.Clock()
fps = 60

# Button properties
button_width = 140
button_height = 40
start_button_x = (screenWidth - button_width) // 2
start_button_y = screenHeight // 2 - button_height
quit_button_x = (screenWidth - button_width) // 2
quit_button_y = screenHeight // 2 + button_height + 20

# Load the "Tiny5" font
tiny_font = pygame.font.Font("Tiny5-Regular.ttf", 30)

# Render the text using the "Tiny5" font
start_text = tiny_font.render('Start', True, white)
quit_text = tiny_font.render('Quit', True, white)

# Platform variables
platformWidth = 100
platformHeight = 10
platformPos = [screenWidth // 2 - platformWidth // 2, screenHeight - platformHeight - 10]
platformSpeed = 10
platformColor = pink
platformOutline = (100, 100, 100)

# Create ball variables
ballX = 250
ballY = 540
ballXspeed = 2
ballYspeed = 2
ballRadius = 15
ballColor = purple
ball = Ball(ballX, ballY, ballRadius, ballColor, ballXspeed, ballYspeed, screen)

# Brick wall class
class Wall():
    def __init__(self):
        self.width = screenWidth // cols
        self.height = 50
        self.blocks = []

    def createWall(self):
        self.blocks = []
        for row in range(rows):
            blockRow = []
            for col in range(cols):  # Iterate through the cols
                blockX = col * self.width  # Create x and y, create rect
                blockY = row * self.height
                rect = pygame.Rect(blockX, blockY, self.width, self.height)
                # Making bricks stronger/harder to break below
                if row < 1:
                    strength = 4
                elif row < 2:
                    strength = 3
                elif row < 3:
                    strength = 2
                elif row < 4:
                    strength = 1

                blockRow.append([rect, strength])
            self.blocks.append(blockRow)

    def drawWall(self):  # Color = based on strength
        for row in self.blocks:
            for block in row:
                if block[1] == 4:
                    blockCol = red
                elif block[1] == 3:
                    blockCol = green
                elif block[1] == 2:
                    blockCol = blue
                elif block[1] == 1:
                    blockCol = purple
                pygame.draw.rect(screen, blockCol, block[0])
                pygame.draw.rect(screen, black, (block[0]), 2)

# Create platform
class Platform():
    def __init__(self):
        self.reset()

    def move(self):
        # Reset movement direction
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
        # Define platform variables
        self.height = 20
        self.width = int(screenWidth / cols)
        self.x = int((screenWidth / 2) - (self.width / 2))
        self.y = screenHeight - (self.height * 2)
        self.speed = 10
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.direction = 0

# Scoreboard
class Score():
    def __init__(self, x, y, color, screen):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.score = 0

    def update(self, points):
        self.score += points

    def draw(self):
        font = pygame.font.SysFont('Comic Sans MS', 25)
        scoreText = font.render(f"Score: {self.score}", True, self.color)
        self.screen.blit(scoreText, (self.x, self.y))

# Create the wall, platform, and scoreboard
wall = Wall()
wall.createWall()
playerPlatform = Platform()
gameScore = Score(10, 10, white, screen)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Handle button clicks in menu
        if not game_active and event.type == MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if start_button_x <= mouse[0] <= start_button_x + button_width and start_button_y <= mouse[1] <= start_button_y + button_height:
                game_active = True  # Start the game
            if quit_button_x <= mouse[0] <= quit_button_x + button_width and quit_button_y <= mouse[1] <= quit_button_y + button_height:
                run = False  # Quit the game

    if game_active:
        # Game screen
        screen.fill(bg)
        screen.blit(background, (0, 0))
        wall.drawWall()
        playerPlatform.draw()
        playerPlatform.move()

        # Create ball
        ball.move()
        ball.check_for_contact_on_x()
        ball.check_for_contact_on_y()

        # Check if ball hits platform
        if (playerPlatform.rect.y < ball.y + ball.radius < playerPlatform.rect.y + playerPlatform.height
              and
            playerPlatform.rect.x < ball.x + ball.radius < playerPlatform.rect.x + playerPlatform.width):
            ball.bounce_y()
            ball.y = playerPlatform.y - ball.radius

        # Check if ball hits wall
        for row in wall.blocks:
            for block in row:
                brick_rect = block[0]
                if brick_rect.collidepoint(ball.x, ball.y - ball.radius) or brick_rect.collidepoint(ball.x, ball.y + ball.radius):
                    block[1] -= 1  # Decrease brick strength
                    if block[1] <= 0:
                        row.remove(block)  # Remove brick if strength is 0
                        gameScore.update(10)
                    ball.bounce_y()

        # Scoreboard
        gameScore.draw()

    else:
        # Main menu
        screen.fill((60, 25, 60))
        mouse = pygame.mouse.get_pos()

        # Start button
        if start_button_x <= mouse[0] <= start_button_x + button_width and start_button_y <= mouse[1] <= start_button_y + button_height:
            pygame.draw.rect(screen, white, [start_button_x, start_button_y, button_width, button_height])
        else:
            pygame.draw.rect(screen, black, [start_button_x, start_button_y, button_width, button_height])
        screen.blit(start_text, (start_button_x + 35, start_button_y + 5))

        # Quit button
        if quit_button_x <= mouse[0] <= quit_button_x + button_width and quit_button_y <= mouse[1] <= quit_button_y + button_height:
            pygame.draw.rect(screen, white, [quit_button_x, quit_button_y, button_width, button_height])
        else:
            pygame.draw.rect(screen, black, [quit_button_x, quit_button_y, button_width, button_height])
        screen.blit(quit_text, (quit_button_x + 40, quit_button_y + 5))

    # Slow down platform
    clock.tick(fps)

    pygame.display.update()

pygame.quit()
