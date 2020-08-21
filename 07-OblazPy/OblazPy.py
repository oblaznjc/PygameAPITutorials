import pygame
import sys
import math


# Conversions
def angle_to_speed(speed, angle):
    speed_x = math.cos(angle) * speed
    speed_y = math.sin(angle) * speed
    return speed_x, speed_y


def ball_line_angle(ball, line):


class Ball:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.angle = math.pi * 3 / 2
        self.radius = 30
        self.color = (0, 255, 0) # green
        self.speed = 5

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        speed_x, speed_y = angle_to_speed(self.speed, self.angle)
        self.y = self.y - math.floor(speed_y) # TODO: Check + - ?
        self.x = self.x - math.floor(speed_x)

    def bounce_off(self, line):
        pass


class Balls:
    def __init__(self):
        pass


class Line:
    def __init__(self, screen, start, end): # TODO: change to line
        self.screen = screen
        self.start = start
        self.end = end
        self.color = (0, 255, 0)
        self.speed = 0 #TODO: change
        self.radius = 5 # TODO: delete
        self.width = 50
        self.height = 10
        self.start_x, self.start_y = self.start
        self.end_x, self.end_y = self.end


    def draw(self):
        # pygame.draw.rect(self.screen, self.color, ((self.x, self.y), (self.width, self.height)))
        pygame.draw.line(self.screen, self.color, self.start, self.end) # TODO: uncomment
        # pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        # self.y -= self.speed
        pass

    def hit_by(self, ball):
        hitbox = pygame.draw.line(self.screen, (255, 0, 0), self.start, self.end, ball.radius) # TODO: uncomment
        # hitbox = pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
        return hitbox.collidepoint(ball.x, ball.y)
        hitbox


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
        clock.tick(30)  # sets clock speed to 60 fps
        for event in pygame.event.get():
            pressed_keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                sys.exit()
            # construct line when clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                start = pygame.mouse.get_pos()
                print(start)
            if event.type == pygame.MOUSEBUTTONUP:
                end = pygame.mouse.get_pos()
                line = Line(screen, start, end)
                print(start, end)
                line_list.append(line)

        for ball in ball_list:
            for line in line_list:
                if line.hit_by(ball):
                    ball.bounce_off(line)
                    print("hit!")

        # Draw and move line up
        for line in line_list:
            line.draw()
            line.move()

        # Draw and move ball
        for ball in ball_list:
            ball.draw()
            ball.move()

        pygame.display.update()


main()