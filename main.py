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
#snake 
SNAKE_SPEED = 10
SNAKE_SPEED_RUN = 20
START_LEN = 5
BORDERS = False
#colors
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
        win.fill((0,0,0))
        game_table = [[0 for i in range(TABLE_SIZE[1])] for j in range(TABLE_SIZE[0])]
        #snake start location
        main_snake = Snake.Snake(game_table, [[2, 3], [2, 4], [2, 5]],SNAKE_COLOR, 0)
        main_snake.draw_all(win)
        if "server" in sys.argv:
            second_snake = Snake.Snake(game_table, [[5, 3], [5, 4], [5, 5]],(0, 0, 255), 1)
            second_snake.draw_all(win)
        #set snake start length
        if START_LEN > main_snake.size:
            main_snake.size = START_LEN
        print("score:", main_snake.size, end = "\r")
        #set apple
        apple = Snake.new_apple(win, game_table, APPLE_COLOR)
        pygame.display.update()
        update_display = False
        game_loop = True
        while game_loop:
            #manage the keyboard
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        game_loop = False
                    elif event.key == pygame.K_r:
                        game_loop = False
                    elif event.key == pygame.K_g:
                        main_snake.size += 1
                    #snake direction keys
                    new_direction = False
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        new_direction = Snake.DIRECTION_LEFT
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        new_direction = Snake.DIRECTION_RIGHT
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        new_direction = Snake.DIRECTION_DOWN
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        new_direction = Snake.DIRECTION_UP
                    if new_direction:
                        main_snake.add_direction(new_direction)
                        if "server" in sys.argv and not second_snake.direction:
                            second_snake.direction = Snake.DIRECTION_DOWN
                    elif event.key == pygame.K_p:
                        main_snake.stop()
                if event.type == pygame.QUIT:
                    run = False
                    game_loop = False
            pressed_keys = pygame.key.get_pressed()
            #run if space is pressed
            if pressed_keys[pygame.K_SPACE]:
                main_snake.speed = SNAKE_SPEED_RUN
            else:
                main_snake.speed = SNAKE_SPEED
            #move the main snake
            if main_snake.move(win, borders = BORDERS):
                if game_loop:
                    game_loop = main_snake.alive
                if main_snake.apple_eaten:
                    Snake.new_apple(win, game_table)
                    eat_sound.play()
                #print the score
                print(LINE_CLEAR_LEN_STR, end="\r")
                print("score:", main_snake.size,"speed:", main_snake.speed , end = "\r")
                update_display = True
            #move the second snake
            if "server" in sys.argv and second_snake.move(win, borders = BORDERS):
                if game_loop:
                    game_loop = second_snake.alive
                if second_snake.apple_eaten:
                    Snake.new_apple(win, game_table)
                update_display = True
            #update the display
            if update_display:
                pygame.display.update()
                update_display = False
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