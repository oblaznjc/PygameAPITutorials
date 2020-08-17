import pygame
import sys
import random
import math


class Ball:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        self.x = x
        self.y = y
        self.speed_x = random.randint(-10, 10)
        self.speed_y = random.randint(-10, 10)
        self.radius = math.floor((200 ** 0.5) - ((self.speed_y ** 2 + self.speed_x ** 2) ** 0.5) )  # smaller = faster

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
        return self.x < 0 + self.radius or self.x > self.screen.get_width() - self.radius

    def top_bottom_walls(self):
        return self.y < 0 + self.radius or self.y > self.screen.get_height() - self.radius


def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption('Bouncing Ball')
    screen.fill(pygame.Color('gray'))
    clock = pygame.time.Clock()

    num_balls = 100

    ball_list = []
    for k in range(num_balls):
        ball1 = Ball(screen, 500, 500)
        ball_list.append(ball1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        clock.tick(60)
        screen.fill(pygame.Color('gray'))

        for k in range(len(ball_list)):
            ball_list[k].move()
            ball_list[k].draw()




        pygame.display.update()


main()


# Optional challenges (if you finish and want do play a bit more): # TODO: Come back for more later!
#   DONE: After you get 1 ball working make a few balls (ball2, ball3, etc) that start in different places.
#   DONE: Make each ball a different color
#   DONE: Make the screen 1000 x 800 to allow your balls more space (what needs to change?)
#   DONE: Make the speed of each ball randomly chosen (1 to 5)
#   DONE: After you get that working try making a list of balls to have 100 balls (use a loop)!
#   DONE: Use random colors for each ball
