import sys, os
import time
import pygame
import Snake

PATH = os.path.dirname(__file__)
if PATH:
    PATH += '/'

LINE_CLEAR_LEN_STR = " "*30
#           height / width
SCREEN_SIZE = (800, 800)
TABLE_SIZE = [28, 28]

SNAKE_SPEED = 10
SNAKE_SPEED_RUN = 20
START_LEN = 50

APPLE_COLOR = (0,255,0)     #green
SNAKE_COLOR = (255,255,255)

Snake.SCREEN_SIZE = SCREEN_SIZE
Snake.TABLE_SIZE = TABLE_SIZE

def main():
    print("Suonds from: https://mixkit.co/free-sound-effects/game/")
    pygame.init()
    #set sounds
    eat_sound = pygame.mixer.Sound(PATH + 'mixkit-unlock-game-notification-253.wav')
    eat_sound.set_volume(0.5)
    eat_sound.play()
    #set the window
    win = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("snake game")
    run = True
    while run:
        Snake.draw_background(win)
        #snake start location
        main_snake = Snake.Snake([(2, 3), (2, 4), (2, 5)],SNAKE_COLOR, 0)
        main_snake.draw_all(win)
        #set snake start length
        if START_LEN > main_snake.size:
            main_snake.size = START_LEN
        print("score:", main_snake.size, end = "\r")
        #set apple
        apple = Snake.new_apple(win, [main_snake], APPLE_COLOR)
        pygame.display.update()
        game_loop = True
        while game_loop:
            #manage the keyboard
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    main_snake.add_direction(event.key)
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        game_loop = False
                    elif event.key == pygame.K_r:
                        game_loop = False
                    elif event.key == pygame.K_g:
                        main_snake.size += 1
                if event.type == pygame.QUIT:
                    run = False
                    game_loop = False
            pressed_keys = pygame.key.get_pressed()
            #run if space is pressed
            if pressed_keys[pygame.K_SPACE]:
                main_snake.speed = SNAKE_SPEED_RUN
            else:
                main_snake.speed = SNAKE_SPEED
            #move the snake
            if main_snake.move(win, borders = False):
                game_loop = main_snake.is_alive()
                #eat apple
                if main_snake.get_head() == apple:
                    eat_sound.play()
                    main_snake.size += 1
                    apple = Snake.new_apple(win, [main_snake], APPLE_COLOR) 
                #print the score
                print(LINE_CLEAR_LEN_STR, end="\r")
                print("score:", main_snake.size,"speed:", main_snake.speed , end = "\r")
                pygame.display.update()
            time.sleep(0.01)
        time.sleep(0.3)
        if run:
            print(LINE_CLEAR_LEN_STR, end="\r")
            print("restarted, score:", main_snake.size)
    pygame.quit()
    print(LINE_CLEAR_LEN_STR, end="\r")
    print("stopped, score:", main_snake.size)
    return None

if __name__ == "__main__":
    main()