import pygame
from pygame.locals import *

pygame.init()

# Screen setup
screenWidth = 500
screenHeight = 650
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("PyBreak Arcade Game")

# Colors
bg = (0, 0, 0)  # Background color
color = (255, 255, 255)  # White for text
color_light = (170, 170, 170)  # Light gray
color_dark = (100, 100, 100)  # Dark gray

#block colors the ones that the ball destroys
red = (255, 0, 0)
pink = (255, 105, 180)
orange = (255, 165, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (255, 0, 255)
white = (255,255,255)

# Button properties
button_width = 140
button_height = 40
start_button_x = (screenWidth - button_width) // 2
start_button_y = screenHeight // 2 - button_height
quit_button_x = (screenWidth - button_width) // 2
quit_button_y = screenHeight // 2 + button_height + 20


# Load the "Tiny5" font
tiny_font = pygame.font.Font("C:\\Users\\Admin\\Desktop\\Python\\game\\Tiny5-Regular.ttf", 30)

# Render the text using the "Tiny5" font
start_text = tiny_font.render('Start', True, color)
quit_text = tiny_font.render('Quit', True, color)


# Game variables
game_active = False  # Tracks if the game is active
clock = pygame.time.Clock()
fps = 60

# Wall class
class Wall:
    def __init__(self):
        self.width = screenWidth // 5
        self.height = 50
        self.blocks = []

    def createWall(self):
        for row in range(4):
            row_blocks = []
            for col in range(5):
                rect = pygame.Rect(col * self.width, row * self.height, self.width, self.height)
                strength = 4 - row
                row_blocks.append([rect, strength])
            self.blocks.append(row_blocks)

    def drawWall(self):
        for row in self.blocks:
            for block in row:
                if block[1] == 4:
                    block_color = (255, 0, 0)
                elif block[1] == 3:
                    block_color = (0, 255, 0)
                elif block[1] == 2:
                    block_color = (0, 0, 255)
                elif block[1] == 1:
                    block_color = (255, 0, 255)
                pygame.draw.rect(screen, block_color, block[0])
                pygame.draw.rect(screen, bg, block[0], 2)

# Platform class
class Platform:
    def __init__(self):
        self.width = 100
        self.height = 20
        self.rect = Rect((screenWidth - self.width) // 2, screenHeight - 40, self.width, self.height)
        self.speed = 10

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.right < screenWidth:
            self.rect.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, (255, 105, 180), self.rect)
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 3)

# Create objects
wall = Wall()
wall.createWall()
platform = Platform()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # Handle button clicks in menu
        if not game_active and event.type == MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if start_button_x <= mouse[0] <= start_button_x + button_width and start_button_y <= mouse[1] <= start_button_y + button_height:
                game_active = True  # Start the game
            if quit_button_x <= mouse[0] <= quit_button_x + button_width and quit_button_y <= mouse[1] <= quit_button_y + button_height:
                running = False  # Quit the game

    if game_active:
        # Game screen
        screen.fill(bg)
        wall.drawWall()
        platform.draw()
        platform.move()
    else:
        # Main menu
        screen.fill((60, 25, 60))
        mouse = pygame.mouse.get_pos()

        # Start button
        if start_button_x <= mouse[0] <= start_button_x + button_width and start_button_y <= mouse[1] <= start_button_y + button_height:
            pygame.draw.rect(screen, color_light, [start_button_x, start_button_y, button_width, button_height])
        else:
            pygame.draw.rect(screen, color_dark, [start_button_x, start_button_y, button_width, button_height])
        screen.blit(start_text, (start_button_x + 35, start_button_y + 5))

        # Quit button
        if quit_button_x <= mouse[0] <= quit_button_x + button_width and quit_button_y <= mouse[1] <= quit_button_y + button_height:
            pygame.draw.rect(screen, color_light, [quit_button_x, quit_button_y, button_width, button_height])
        else:
            pygame.draw.rect(screen, color_dark, [quit_button_x, quit_button_y, button_width, button_height])
        screen.blit(quit_text, (quit_button_x + 40, quit_button_y + 5))

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
