import pygame, sys
import math


def distance(point1, point2):
    point1_x = point1[0]
    point2_x = point2[0]
    point1_y = point1[1]
    point2_y = point2[1]

    # TODO 4: Return the actual distance between point 1 and point 2.
    #  Hint: you will need the math library for the sqrt function.
    #       distance = sqrt(   (delta x) ** 2 + (delta y) ** 2  )
    return math.sqrt((point2_x - point1_x) ** 2 + (point2_y - point1_y) ** 2)


def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Mouse click positions")
    font = pygame.font.Font(None, 25)

    # DONE 8: Load the "drums.wav" file into the pygame music mixer

    pygame.mixer.music.load('drums.wav')

    instruction_text = 'Click in the circle'
    text_color = (222, 222, 0)
    instructions_image = font.render(instruction_text, True, text_color)

    circle_color = (154, 58, 212)
    circle_center = (screen.get_width() // 2, screen.get_height() // 2)
    circle_radius = 50
    circle_border_width = 3

    message_text = ''

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # DONE 2: For a MOUSEBUTTONDOWN event get the click position.

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = event.pos
                print(click_pos)

            # DONE 3: Determine the distance between the click position and the circle_center using the distance
                #  function and save the result into a variable called distance_from_circle

                dist_from_circle = distance(click_pos, circle_center)

            # DONE 5a: If distance_from_circle is less than or equal to circle_radius, set message_text to 'Bullseye!'

                if dist_from_circle < 50:
                    message_text = "Bullseye!"
                    pygame.mixer.music.play(-1)
            # DONE 5b: If distance_from_circle is greater than the circle_radius, set the message_text to 'You missed!'

                else:
                    message_text = "You missed!"

            # DONE 9: Start playing the music mixer looping forever if the click is within the circle

            # see DONE 5a

            # DONE 10: Stop playing the music if the click is outside the circle

                    pygame.mixer.music.stop()

        screen.fill(pygame.Color("Black"))

        # DONE 1: Draw the circle using the screen, circle_color, circle_center, circle_radius, and circle_border_width

        pygame.draw.circle(screen, circle_color, circle_center, circle_radius, circle_border_width)

        # DONE 6: Create a text image (render the text) based on the message_text with the color (122, 237, 201)

        message_image = font.render(message_text, True, (122, 237, 201))
        screen.blit(instructions_image, (25, 25))

        # DONE 7: Draw (blit) the message to the user that says 'Bullseye!' or 'You missed!'

        screen.blit(message_image, (25, 375))
        pygame.display.update()


main()
