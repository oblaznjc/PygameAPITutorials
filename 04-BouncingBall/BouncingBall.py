import pygame
import sys
import random


# You will implement this module ENTIRELY ON YOUR OWN!

# DONE: Create a Ball class.
class Ball:
    def __init__(self, screen, color, x, y, radius):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = random.randint(-5, 5)
        self.speed_y = random.randint(-5, 5)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x = self.x + self.speed_x
        self.y = self.y + self.speed_y
        if self.right_left_walls():
            self.speed_x = - self.speed_x
        if self.top_bottom_walls():
            self.speed_y = - self.speed_y

    def right_left_walls(self):
        return self.x == 0 + self.radius or self.x == self.screen.get_width() - self.radius

    def top_bottom_walls(self):
        return self.y == 0 + self.radius or self.y == self.screen.get_height() - self.radius


# DONE: Possible member variables: screen, color, x, y, radius, speed_x, speed_y
# DONE: Methods: __init__, draw, move


def main():
    pygame.init()
    screen = pygame.display.set_mode((300, 300))
    pygame.display.set_caption('Bouncing Ball')
    screen.fill(pygame.Color('gray'))
    clock = pygame.time.Clock()

    # DONE: Create an instance of the Ball class called ball1
    ball = Ball(screen, (0, 0, 0), 150, 150, 10)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        clock.tick(60)
        screen.fill(pygame.Color('gray'))

        # DONE: Move the ball
        ball.move()
        # DONE: Draw the ball
        ball.draw()

        pygame.display.update()


main()


# Optional challenges (if you finish and want do play a bit more): # TODO: Come back for more later!
#   After you get 1 ball working make a few balls (ball2, ball3, etc) that start in different places.
#   Make each ball a different color
#   Make the screen 1000 x 800 to allow your balls more space (what needs to change?)
#   Make the speed of each ball randomly chosen (1 to 5)
#   After you get that working try making a list of balls to have 100 balls (use a loop)!
#   Use random colors for each ball
