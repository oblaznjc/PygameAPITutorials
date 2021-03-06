import pygame
import sys
import math
import time
import random

# --------------------------- Physics/Math functions ---------------------------
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
        self.color = (0, 255, 255)  # green
        self.speed_x = 0
        self.speed_y = 0  # down 1
        self.last_hit_time = 0
        self.mass = 1
        self.speed = 50
        self.sound = pygame.mixer.Sound("bounce.wav")

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.y = self.y + self.speed_y // 20
        self.x = self.x + self.speed_x // 7

        # gravity simulation
        self.speed_y = self.speed_y + 1
        if self.x < 0 or self.x > self.screen.get_width():
            self.wrap()

    def bounce_off(self, particle):
        unit_normal_vector = unit_normal_vector_between(self, particle)
        x, y = unit_normal_vector
        self.speed_x, self.speed_y = round(x * self.speed), round(y * self.speed)

    def hit(self, particle):
        distance = math.sqrt((self.x - particle.x) ** 2 + (self.y - particle.y) ** 2)
        if distance < self.radius:
            self.sound.play()
        return distance < self.radius

    def wrap(self):
        if self.x > self.screen.get_width():
            self.x = 0
        else:
            self.x = self.screen.get_width()


class Scoreboard:
    def __init__(self, screen, start_time):
        self.screen = screen
        self.start = start_time
        self.score = 0
        self.font = pygame.font.SysFont('bahnschrift', 30)

    def draw(self):
        score_string = "Time: {}".format(self.score)
        score_image = self.font.render(score_string, True, (255, 255, 255))
        self.screen.blit(score_image, (20, 20))

    def update(self):
        self.score = round(time.time() - self.start, 3)


class Leaderboard:
    def __init__(self, screen):
        self.all_scores = [0]
        self.screen = screen

    def add_score(self, score):
        self.all_scores.append(score)

    def high_score(self):
        return max(self.all_scores)

    def draw(self):
        font = pygame.font.SysFont('bahnschrift', 30)
        score_string = "Best: {}".format(self.high_score())
        score_image = font.render(score_string, True, (255, 255, 255))
        self.screen.blit(score_image, (20, 60))


class Laser:
    def __init__(self, screen, y):
        self.screen = screen
        self.color = (255, 0, 0)
        self.start_x = 0
        self.end_x = screen.get_width()
        self.y = y
        self.sound = pygame.mixer.Sound("laser_death.wav")

    def draw(self):
        pygame.draw.line(self.screen, self.color, (self.start_x, self.y), (self.end_x, self.y), 4)

    def top_hit(self, ball):
        if self.y + ball.radius > ball.y:
            self.sound.play()
            return True
        return False

    def bot_hit(self, ball):
        if self.y - ball.radius < ball.y:
            self.sound.play()
            return True
        return False


class LineParticle:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.color = (0, 255, 0)
        self.radius = 3
        self.diameter = self.radius * 2

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

    def move(self, speed):
        self.y = self.y - speed


class Lines:
    def __init__(self):
        self.list = []
        self.speed = 1

    def add(self, new_particle):
        self.list.append(new_particle)

    def erase_all(self):
        self.list = []

    def move(self):
        for particle in self.list:
            particle.move(self.speed)

    def draw(self):
        for particle in self.list:
            particle.draw()

    def hit(self, ball, level):
        for particle in self.list:
            if ball.hit(particle):
                ball.bounce_off(particle)

    def evaporate_particle(self, top_laser, bot_laser):
        for k in range(len(self.list) - 1, -1, -1):
            if self.list[k].y < top_laser.y or self.list[k].y == bot_laser.y:
                del self.list[k]

    def level_up(self, new_level):
        self.speed = new_level


class Pen:
    """ moves a draw dot on the screen, following the mouse"""
    def __init__(self, screen, radius=5):
        self.x, self.y = pygame.mouse.get_pos()
        self.screen = screen
        self.color = (255, 0, 255)
        self.radius = radius

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)


class Eraser:
    """ Erases the entire screen"""
    def __init__(self, screen, lines):
        self.screen = screen
        self.color = (255, 255, 0)
        self.radius = 1000
        self.lines = lines

    def draw(self):
        pygame.draw.circle(self.screen, self.color, pygame.mouse.get_pos(), self.radius)

    def erase(self, particle):
        x, y = pygame.mouse.get_pos()
        distance = math.sqrt((x - particle.x) ** 2 + (y - particle.y) ** 2)
        return distance < self.radius

    def erase_all(self):
        self.lines.erase_all()


class BonusList:
    def __init__(self, screen):
        self.screen = screen
        self.live_list = []
        self.collected_list = [0, 1]
        self.color = (255, 255, 0)
        self.bar_width = self.screen.get_width() // 5

    def add_live(self, bonus):
        self.live_list.append(bonus)

    def move(self):
        for bonus in self.live_list:
            bonus.move()

    def draw(self):
        for bonus in self.live_list:
            bonus.draw()

    def draw_inventory(self):
        for k in range(len(self.collected_list)):
            pygame.draw.rect(self.screen, self.color, (k * self.bar_width, 0, self.bar_width - 1, 18))

    def check_for_hit(self, ball):
        for bonus in self.live_list:
            if bonus.collected(ball):
                self.convert_live_to_collected()

    def convert_live_to_collected(self):
        for k in range(len(self.live_list) - 1, -1, -1):
            if self.live_list[k].collected:
                self.collected_list.append(self.live_list[k])
                del self.live_list[k]
                break

    def use_bonus(self, lines):
        if len(self.collected_list) > 0:
            lines.erase_all()
            k = self.collected_list[0]
            self.collected_list.remove(k)


class NewBonus:
    def __init__(self, screen):
        self.screen = screen
        self.color = (255, 255, 0)
        self.side_length = 50
        self.x = random.randrange(0, self.screen.get_width())
        self.y = screen.get_height()
        self.speed_divider = 2
        self.move_counter = 0

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.side_length, self.side_length))

    def move(self):
        if self.move_counter % self.speed_divider == 0:
            self.y -= 1

    def collected(self, ball):
        hitbox = pygame.Rect(self.x, self.y, self.side_length, self.side_length)
        ballbox = pygame.Rect(ball.x - ball.radius, ball.y - ball.radius, ball.diameter, ball.diameter)
        return hitbox.colliderect(ballbox)


def game_loop(screen, leaderboard, clock, font):
    # load images and booleans
    game_over_image = pygame.image.load("gameover.png")
    wait_to_start = True
    is_game_over = False
    time_of_bonus = 0
    level = 1

    # construct opening screen (lasers, ball, score and leader board)
    scoreboard = Scoreboard(screen, time.time())
    top_laser = Laser(screen, 20)
    bot_laser = Laser(screen, screen.get_height() - 20)
    ball = Ball(screen, screen.get_width() // 2, 60)
    ball.draw()
    scoreboard.draw()
    leaderboard.draw()
    top_laser.draw()
    bot_laser.draw()
    lines = Lines()
    bonus_list = BonusList(screen)
    bonus_list.draw_inventory()
    bonus_list.draw()

    # wait for mouse click to start game
    while wait_to_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            pressed_keys = pygame.mouse.get_pressed()
            if pressed_keys == (1, 0, 0):
                scoreboard = Scoreboard(screen, time.time())
                wait_to_start = False
        pygame.display.update()

    # introduction screen and game is over screen
    while True:
        screen.fill((0, 0, 0))  # black
        clock.tick(120)  # sets clock speed to 120 fps

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Use a bonus you have in the list
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_SPACE] and (time.time() - time_of_bonus > 1):
                screen.fill((255, 255, 0))
                bonus_list.use_bonus(lines)
                time_of_bonus = time.time()
                break

        # Draw these before game is over
        scoreboard.draw()
        leaderboard.draw()
        ball.draw()
        lines.draw()
        top_laser.draw()
        bot_laser.draw()
        pen = Pen(screen)
        pen.draw()
        bonus_list.draw()
        bonus_list.draw_inventory()

        if is_game_over:
            # draw game over image
            screen.blit(game_over_image, (screen.get_width() // 2 - game_over_image.get_width() // 2,
                                          screen.get_height() // 2 - game_over_image.get_height() // 2))

            # draw current score
            score_image = font.render(str(scoreboard.score), True, (255, 255, 255))
            screen.blit(score_image, (screen.get_width() // 2 - score_image.get_width() // 2,
                                      screen.get_height() // 2 - score_image.get_height() // 2 + 10))

            # draw high score if new high score
            high_score_image = font.render("NEW HIGH SCORE!", True, (255, 255, 255))
            if scoreboard.score == leaderboard.high_score():  # TODO: flashing
                screen.blit(high_score_image, (screen.get_width() // 2 - high_score_image.get_width() // 2,
                                               screen.get_height() // 2 - high_score_image.get_height() // 2 - 180))

            # check for restart click
            pressed_keys = pygame.mouse.get_pressed()
            position_x, position_y = pygame.mouse.get_pos()
            hitbox = pygame.Rect(screen.get_width() // 2 - game_over_image.get_width() // 2,
                                 screen.get_height() // 2 - game_over_image.get_height() // 2,
                                 game_over_image.get_width(),
                                 game_over_image.get_height())
            if pressed_keys == (1, 0, 0) and hitbox.collidepoint(position_x, position_y):
                screen.fill((0, 0, 0))
                game_loop(screen, leaderboard, clock, font)

            pygame.display.update()
            continue

        scoreboard.update()

        # construct line when mouse clicked
        pressed_keys = pygame.mouse.get_pressed()
        if pressed_keys == (1, 0, 0) and not ball.hit(pen):
            particle = LineParticle(screen, pen.x, pen.y)
            particle.draw()
            lines.add(particle)

        # interactions between bonus-ball, line-ball, and line-laser
        bonus_list.check_for_hit(ball)
        lines.hit(ball, level)
        lines.evaporate_particle(top_laser, bot_laser)

        # move lines, ball, and bonuses
        lines.move()
        ball.move()
        bonus_list.move()

        # check for level up
        new_level = math.ceil(scoreboard.score / 5)
        if level < new_level:
            bonus = NewBonus(screen)
            bonus_list.add_live(bonus)
            level = new_level

        # Check for game over
        if top_laser.top_hit(ball) or bot_laser.bot_hit(ball):
            is_game_over = True
            leaderboard.add_score(scoreboard.score)

        pygame.display.update()


def main():
    pygame.init()
    pygame.display.set_caption("LASER HATER!")
    screen = pygame.display.set_mode((800, 800))
    leaderboard = Leaderboard(screen)
    clock = pygame.time.Clock()
    scoreboard = Scoreboard(screen, time.time())
    pygame.mouse.set_cursor(*pygame.cursors.ball)
    font = pygame.font.SysFont('bahnschrift', 90)
    pygame.mixer.music.load('background.wav')
    pygame.mixer.music.play(999)
    new_game_image = pygame.image.load("newgame.png")
    lines = Lines()

    # draw opening page
    while True:
        screen.fill((0, 0, 0))  # black
        clock.tick(120)  # sets clock speed to 120 fps

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


        # construct opening screen (lasers, ball, score and leader board)
        top_laser = Laser(screen, 20)
        bot_laser = Laser(screen, screen.get_height() - 20)
        ball = Ball(screen, screen.get_width() // 2, 60)
        ball.draw()
        scoreboard.draw()
        leaderboard.draw()
        top_laser.draw()
        bot_laser.draw()
        pen = Pen(screen)
        pen.draw()
        lines.draw()

        # construct line when mouse clicked
        pressed_keys = pygame.mouse.get_pressed()
        if pressed_keys == (1, 0, 0) and not ball.hit(pen):
            particle = LineParticle(screen, pen.x, pen.y)
            particle.draw()
            lines.add(particle)

        # draw image and check for start game click
        screen.blit(new_game_image, (screen.get_width() // 2 - new_game_image.get_width() // 2,
                                      screen.get_height() // 2 - new_game_image.get_height() // 2))

        pressed_keys = pygame.mouse.get_pressed()
        position_x, position_y = pygame.mouse.get_pos()

        hitbox = pygame.Rect(screen.get_width() // 2 - new_game_image.get_width() // 2,
                             screen.get_height() // 2 - new_game_image.get_height() // 2,
                             new_game_image.get_width(),
                             new_game_image.get_height())
        if pressed_keys == (1, 0, 0) and hitbox.collidepoint(position_x, position_y):
            screen.fill((0, 0, 0))
            break

        pygame.display.update()

    game_loop(screen, leaderboard, clock, font)


main()