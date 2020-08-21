import pygame
import sys


class Missile:
    def __init__(self, screen, x, y):
        # Store the data.  Initialize:   y to 591   and   has_exploded to False.
        self.screen = screen
        self.x = x
        self.y = y
        self.has_exploded = False

    def move(self):
        # Make self.y 5 smaller than it was (which will cause the Missile to move UP).
        self.y -= 5

    def draw(self):
        # Draw a vertical, 4 pixels thick, 8 pixels long, red (or green) line on the screen,
        # where the line starts at the current position of this Missile.
        pygame.draw.line(self.screen, (0, 255, 0), (self.x, self.y), (self.x, self.y + 8), 4)


class Fighter:
    def __init__(self, screen, x, y):
        # Store the data.
        # Set   self.missiles   to the empty list.
        # Load the file  "fighter.png"  as the image
        # DONE: Set the colorkey to white (it has a white background that needs removed)
        self.screen = screen
        self.x = x
        self.y = y
        self.image = pygame.image.load("fighter.png")
        self.image.set_colorkey((255, 255, 255))
        self.missiles = []
        self.pew_sound = pygame.mixer.Sound("pew.wav")

    def draw(self):
        # Draw this Fighter, using its image at its current (x, y) position.
        self.screen.blit(self.image, (self.x, self.y))

    def fire(self):
        # Construct a new Missile 50 pixels to the right of this Fighter.
        # Append that Missile to this Fighter's list of Missile objects.
        new_missile = Missile(self.screen, self.x + self.image.get_width() // 2,
                              self.screen.get_height() - self.image.get_height() - 1)
        self.missiles.append(new_missile)
        self.pew_sound.play()

    def remove_exploded_missiles(self):
        # Already complete
        for k in range(len(self.missiles) - 1, -1, -1):
            if self.missiles[k].has_exploded or self.missiles[k].y < 0:
                del self.missiles[k]


class Badguy:
    def __init__(self, screen, x, y, speed):
        # Store the given arguments as instance variables with the same name.
        # Set   is_dead to False   and   original_x to x   and move_right to True.
        # Load the file  "badguy.png"  as the image. and set its colorkey to black.
        self.screen = screen
        self.x = x
        self.original_x = x
        self.y = y
        self.speed = speed
        self.is_dead = False
        self.image = pygame.image.load("badguy.png")

    def move(self):
        # Move 2 units in the current direction.
        # Switch direction if this Badguy's position is more than 100 pixels from its original position.
        self.x += self.speed

    def turn(self):
        # turns a badguy if called
        self.speed = -self.speed
        self.y = self.y + self.image.get_height() // 2

    def draw(self):
        # Draw this Badguy, using its image at its current (x, y) position.
        self.screen.blit(self.image, (self.x, self.y))

    def hit_by(self, missile):
        # Make a Badguy hitbox rect.
        # Return True if that hitbox collides with the xy point of the given missile.
        hitbox = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        return hitbox.collidepoint(missile.x, missile.y)


class EnemyFleet:
    def __init__(self, screen, enemy_rows):
        # Already done.  Prepares the list of Badguys.
        self.screen = screen
        self.badguys = []
        for j in range(enemy_rows):
            for k in range(6):  # Maximum 7 due to newly added turn feature
                self.badguys.append(Badguy(screen, 80 * k, 50 * j + 20, enemy_rows))
        self.explosion_sound = pygame.mixer.Sound("explosion.wav")
        self.win_sound = pygame.mixer.Sound("win.wav")

    @property
    def is_defeated(self):
        # Return True if the number of badguys in this Enemy Fleet is 0,
        # otherwise return False.
        if len(self.badguys) == 0:
            self.win_sound.play()
            return True
        return False

    def move(self):
        # Make each badguy in this EnemyFleet move.
        for badguy in self.badguys:
            badguy.move()

    def turn(self):
        # Checks if any badguys reach screen border
        for badguy in self.badguys:
            if badguy.x < 0 or badguy.x + badguy.image.get_width() > self.screen.get_width():
                return True

    def draw(self):
        # Make each badguy in this EnemyFleet draw itself.
        for badguy in self.badguys:
            badguy.draw()

    def remove_dead_badguys(self):
        for k in range(len(self.badguys) - 1, -1, -1):
            if self.badguys[k].is_dead:
                del self.badguys[k]
                self.explosion_sound.play()


class Scoreboard:
    def __init__(self, screen, ):
        self.screen = screen
        self.score = 0
        self.font = pygame.font.Font(None, 30)

    def draw(self):
        score_string = "Score: {}".format(self.score)
        score_image = self.font.render(score_string, True, (255, 255, 255))
        self.screen.blit(score_image, (5, 5))


def main():
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("SPACE INVADERS!")
    screen = pygame.display.set_mode((640, 650))

    is_game_over = False
    enemy_rows = 2
    enemy_fleet = EnemyFleet(screen, enemy_rows)
    fighter = Fighter(screen, screen.get_width() // 2 - 50, screen.get_height() - 60)
    game_over_image = pygame.image.load("gameover.png")
    scoreboard = Scoreboard(screen)
    lose_sound = pygame.mixer.Sound("lose.wav")

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            pressed_keys = pygame.key.get_pressed()
            # DONE 5: If the event type is KEYDOWN and pressed_keys[pygame.K_SPACE] is True, then fire a missile
        if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_SPACE]:
            fighter.fire( )
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill((0, 0, 0))

        # Draw these before game over
        enemy_fleet.draw()
        fighter.draw()
        for missile in fighter.missiles:
            missile.draw()
        scoreboard.draw()

        if is_game_over:
            screen.blit(game_over_image, (screen.get_width() // 2 - game_over_image.get_width() // 2,
                                          screen.get_height() // 2 - game_over_image.get_height() // 2))
            pygame.display.update()
            continue

        # Move fighter
        pressed_keys = pygame.key.get_pressed()
        speed = 5
        if pressed_keys[pygame.K_LEFT] and fighter.x > -fighter.image.get_width() // 2 + fighter.image.get_width() // 2:
            fighter.x -= speed
        if pressed_keys[pygame.K_RIGHT] and fighter.x < screen.get_width() - fighter.image.get_width():
            fighter.x += speed

        # Move bad guys and (newly added) turn feature allows for full screen movement of bad guys!
        enemy_fleet.move()
        if enemy_fleet.turn():
            for badguy in enemy_fleet.badguys:
                badguy.turn()

        for missile in fighter.missiles:
            missile.move()

        for badguy in enemy_fleet.badguys:
            for missile in fighter.missiles:
                if badguy.hit_by(missile):
                    badguy.is_dead = True
                    missile.has_exploded = True
                    scoreboard.score += 100

        fighter.remove_exploded_missiles()
        enemy_fleet.remove_dead_badguys()

        if enemy_fleet.is_defeated:
            enemy_rows += 1
            enemy_fleet = EnemyFleet(screen, enemy_rows)

        for badguy in enemy_fleet.badguys:
            if badguy.y > screen.get_height() - fighter.image.get_height() - badguy.image.get_height():
                is_game_over = True
                lose_sound.play()

        # When a Badguy is killed add 100 points to the scoreboard.score

        pygame.display.update()


main()