import sys, os
import time
import pygame
import Snake

import __main__
SCRIPT_FILE = __main__.__file__
PATH = "/".join(SCRIPT_FILE.replace("\\", "/").split("/")[:-1]) + '/'

#           height / width
SCREEN_SIZE = (800, 800)
TABLE_SIZE = [28, 28]

SNAKE_SPEED = 10
SNAKE_SPEED_RUN = 20
START_LEN = 50

APPLE_COLOR = (0,255,0)     #green

Snake.SCREEN_SIZE = SCREEN_SIZE
Snake.TABLE_SIZE = TABLE_SIZE

def main():
    print("Suonds from https://mixkit.co/free-sound-effects/game/")

    pygame.init()
    #set sounds
    eat_sound = pygame.mixer.Sound(PATH + 'mixkit-unlock-game-notification-253.wav')
    eat_sound.set_volume(0.5)
    eat_sound.play()
    #set the window
    win = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("snake game")
    #Snake.draw_background(win)
    #snake start location
    main_snake = Snake.Snake([(2, 3), (2, 4), (2, 5)],(255,255,255), 0)
    main_snake.draw_all(win)

    if START_LEN > main_snake.size:
        main_snake.size = START_LEN
    print("score:", main_snake.size, end = "\r")

    apple = Snake.new_apple(win, [main_snake], APPLE_COLOR)
    pygame.display.update()
    run = True
    while run:
        #manage the keyboard
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                main_snake.add_direction(event.key)
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_g:
                    main_snake.size += 1
            if event.type == pygame.QUIT:
                run = False
                break
        pressed_keys = pygame.key.get_pressed()
        
        #run if space is pressed
        if pressed_keys[pygame.K_SPACE]:
            main_snake.speed = SNAKE_SPEED_RUN
        else:
            main_snake.speed = SNAKE_SPEED
        
        #move the snake
        if main_snake.move(win, borders = False):
            run = main_snake.is_alive()
            #eat apple
            if main_snake.get_head() == apple:
                eat_sound.play()
                main_snake.size += 1
                apple = Snake.new_apple(win, [main_snake], APPLE_COLOR) 
            print("score:", main_snake.size,"speed:", main_snake.speed, "     ", end = "\r")
            pygame.display.update()
        time.sleep(0.01)
    time.sleep(0.3)
    pygame.quit()
    print("stopped, score:", main_snake.size, "     ")
    return None

if __name__ == "__main__":
    main()

#TODO
#credit https://mixkit.co/free-sound-effects/game/


