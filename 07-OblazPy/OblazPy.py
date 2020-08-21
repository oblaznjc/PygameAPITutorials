import pygame
import sys
import math


# Conversions
def angle_to_speed(speed, angle):
    speed_x = math.cos(angle) * speed
    speed_y = math.sin(angle) * speed
    return speed_x, speed_y


def collision(ball, particle):
    pass


def ball_line_angle(ball, line):
    pass

class Ball:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.angle = math.pi * 3 / 2
        self.radius = 30
        self.diameter = self.radius * 2
        self.color = (0, 255, 255) # green
        self.speed = 5

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        speed_x, speed_y = angle_to_speed(self.speed, self.angle)
        self.y = self.y - math.floor(speed_y) # TODO: Check + - ?
        self.x = self.x - math.floor(speed_x)

    def bounce_off(self, particle):
        collision(self, particle)
        self.speed = -self.speed

    """
    def hit(self, particle):
        hitbox = pygame.Rect(self.x - self.radius, self.y - self.radius, self.diameter, self.diameter)
        pygame.draw.rect(self.screen, self.color,
                         (self.x - self.radius, self.y - self.radius, self.diameter, self.diameter))
        return hitbox.collidepoint(particle.x, particle.y)
    """


class Balls:
    def __init__(self):
        pass


class LineParticle:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.color = (0, 255, 0)
        self.radius = 2
        self.diameter = self.radius * 2

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

    def hit(self, particle):
        hitbox = pygame.Rect(self.x - self.radius, self.y - self.radius, self.diameter, self.diameter)
        pygame.draw.rect(self.screen, self.color,
                         (self.x - self.radius, self.y - self.radius, self.diameter, self.diameter))
        return hitbox.collidepoint(particle.x, particle.y)

    def move(self):
        pass


class Pen():
    """ moves a draw dot on the screen, following the mouse"""
    def __init__(self, screen):
        pos = pygame.mouse.get_pos()
        self.x, self.y = pygame.mouse.get_pos()
        self.screen = screen
        self.color = (255, 0, 255)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), 5)



def main():
    # Boilerplate code
    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    clock = pygame.time.Clock()

    # construct ball and line list
    line_list = []
    ball_list = []

    ball = Ball(screen, screen.get_width() // 2, 10)
    ball_list.append(ball)


    while True:
        screen.fill((0, 0, 0))  # black
        clock.tick(60)  # sets clock speed to 60 fps
        pen = Pen(screen)
        pen.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # construct line when clicked
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_SPACE]:
            particle = LineParticle(screen,pen.x, pen.y)
            particle.draw()
            line_list.append(particle)

        for ball in ball_list:
            for particle in line_list:
                if particle.hit(ball):
                    ball.bounce_off(particle)

        # Draw and move line up
        for particle in line_list:
            particle.draw()
            particle.move()

        # Draw and move ball
        for ball in ball_list:
            ball.draw()
            ball.move()

        pygame.display.update()


main()