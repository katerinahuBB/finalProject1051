import pygame as pg

class Ball:
    def __init__(self, x, y, radius, color, x_speed, y_speed, screen):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = pg.Color(color)
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.screen = screen

    def move(self):
        pg.draw.circle(self.screen, self.color, [self.x, self.y], self.radius)
        self.y -= self.y_speed
        self.x -= self.x_speed


    def bounce_x(self):
        self.x_speed *= -1

    def bounce_y(self):
        self.y_speed *= -1

    def check_for_contact_on_x(self):
        if self.x - self.radius <= 0 or self.x + self.radius >= self.screen.get_width():
            self.bounce_x()

    def check_for_contact_on_y(self):
        if self.y + self.radius <= 0:
            self.bounce_y()

    def update_speed(self, level):
        speed_increase = 0.5 * level
        self.x_speed += speed_increase if self.x_speed > 0 else -speed_increase
        self.y_speed += speed_increase if self.y_speed > 0 else -speed_increase