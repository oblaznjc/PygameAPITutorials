import pygame
import sys
import math

# --------------------------- Conversion helper functions ---------------------------
# https://stackoverflow.com/questions/35211114/2d-elastic-ball-collision-physics

def unit_normal_vector_between(ball, particle):
    ballx_to_particlex = ball.x - particle.x
    bally_to_particley = ball.y - particle.y
    norm = math.sqrt(ballx_to_particlex ** 2 + bally_to_particley ** 2)
    unit_normal_vector_x = ballx_to_particlex / norm
    unit_normal_vector_y = bally_to_particley / norm
    return unit_normal_vector_x, unit_normal_vector_y


class Ball:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.angle = 270
        self.radius = 30
        self.diameter = self.radius * 2
        self.color = (0, 255, 255) # green
        self.speed_x = 0
        self.speed_y = -3  # down 3
        self.last_hit_time = 0
        self.mass = 1

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.y = self.y - self.speed_y
        self.x = self.x - self.speed_x

    def bounce_off(self, particle):
        unit_normal_vector = unit_normal_vector_between(self, particle)
        print(unit_normal_vector)
        self.speed_x, self.speed_y = unit_normal_vector


    def hit(self, particle):
        distance = math.sqrt((self.x - particle.x) ** 2 + (self.y - particle.y) ** 2)
        return distance < self.radius


class Balls:
    def __init__(self):
        pass


class LineParticle:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.color = (0, 255, 0)
        self.radius = 5
        self.diameter = self.radius * 2
        self.speed = 0
        self.mass = math.inf  # TODO: check if 100 is better

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.y = self.y - self.speed




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
    time_threshold = 0.1

    # construct ball and line list
    line_list = []

    ball = Ball(screen, screen.get_width() // 2, 10)

    while True:
        screen.fill((0, 0, 0))  # black
        clock.tick(120)  # sets clock speed to 60 fps
        pen = Pen(screen)
        pen.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # construct line when clicked
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_SPACE] and not ball.hit(pen):
            particle = LineParticle(screen, pen.x, pen.y)
            particle.draw()
            line_list.append(particle)

        # if time.time() - ball.last_hit_time > time_threshold:
        for particle in line_list:
            if ball.hit(particle):
                ball.bounce_off(particle)
                # ball.last_hit_time = time.time()
                break


        # Draw and move line up
        for particle in line_list:
            particle.draw()
            particle.move()

        # Draw and move ball
        ball.draw()
        ball.move()

        pygame.display.update()


main()