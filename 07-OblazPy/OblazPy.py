import pygame
import sys


class Ball:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.radius = 30
        self.color = (0, 255, 0) # green
        self.speed = 5 #TODO: modify not hard

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.y = self.y + self.speed

    def bounce(self):
        self.speed = -self.speed
        print(self.x, self.y)

    def hit_by(self, line):
        hitbox = pygame.draw.circle(self.screen, self.x - self.radius, self.y -self.radius,
                             self.radius * 2, self.radius * 2)
        return hitbox.collidepoint(line.x, line.y)


class Balls:
    def __init__(self):
        pass


class Line:
    def __init__(self, screen, x, y): # TODO: change to line
        self.screen = screen
        self.x = x
        self.y = y
        self.color = (0, 255, 0)
        self.speed = 0 #TODO: change
        self.radius = 5 # TODO: delete
        self.width = 50
        self.height = 10

    def draw(self):
        pygame.draw.rect(self.screen, self.color, ((self.x, self.y), (self.width, self.height)))
        # pygame.draw.line(self.screen, self.color, (self.x, self.y), (self.x + 20, self.y + 20), 5) # TODO: uncomment

    def move(self):
        self.y -= self.speed


def main():

    # Boilerplate code

    pygame.init()
    screen = pygame.display.set_mode((640, 480))
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
                click_x, click_y = pygame.mouse.get_pos()
                line = Line(screen, click_x, click_y)
                print(click_x, click_y)
                line_list.append(line)

        for ball in ball_list:
            for line in line_list:
                if ball.hit_by(line):
                    ball.bounce()
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