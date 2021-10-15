import os
from time import sleep
import socket #for the online
import pygame
from os.path import abspath #for opening files
os.chdir(os.path.dirname(__file__)) #set the path for opening files
#local imports
import Snake
import Canvas
import GameEvents
import PrintManager
from settings import SETTINGS
#define
RUN = SETTINGS != None
#---------- main ----------#
def main():
    print_obj = PrintManager.PrintManager()
    print_obj.new_line("Suonds from: https://mixkit.co/free-sound-effects/game/")
    if SETTINGS["online"]:
        socket_port = SETTINGS["defult_port"]
    #set pygame
    pygame.init()
    #set sounds
    eat_sound = pygame.mixer.Sound(abspath(SETTINGS['eat_sound']))
    eat_sound.set_volume(0.5)
    eat_sound.play()
    #set canvas
    game_canvas = Canvas.Canvas(SETTINGS["game_table"], SETTINGS["game_screen"], "snake game")
    #set game
    game_count = 1
    run = True
    while run:
        game_canvas.reset()
        main_snake = Snake.Snake(game_canvas, SETTINGS["snake_start_posotions"], SETTINGS['snake_color'])
        """
        if SETTINGS["online"]:
            second_snake = Snake(game_canvas, [[5, 3], [5, 4], [5, 5]],(0, 0, 255), 2)
        """
        #set snake start length
        if SETTINGS["snake_start_length"] > main_snake.size:
            main_snake.size = SETTINGS["snake_start_length"]
        
        print("score:", main_snake.size, end = "\r")
        game_canvas.new_apple()
        game_canvas.update()
        #the game loop
        game_loop = True
        while game_loop:
            #manage the keyboard
            game_event = GameEvents.handle_pygame_events(pygame.event.get(), pygame.key.get_pressed())
            
            if game_event.close_game:
                run = False
                game_loop = False
            elif game_event.restart:
                game_loop = False
            else: #continue the game
                if game_event.pause:
                    main_snake.stop()
                if game_event.new_direction:
                    main_snake.add_direction(game_event.new_direction)
                    """
                    if SETTINGS["online"] and not second_snake.direction:
                        second_snake.direction = Snake.DIRECTION_DOWN
                    """

                if game_event.sprint:
                    main_snake.speed = SETTINGS["snake_speed_run"]
                else:
                    main_snake.speed = SETTINGS["snake_speed"]
                
                #move the main snake
                if main_snake.move(borders = SETTINGS["game_borders"]): # the snake moved
                    if main_snake.alive:
                        if main_snake.apple_eaten:
                            game_canvas.new_apple()
                            eat_sound.play()
                            game_event.grow = True
                        if game_event.grow:
                            main_snake.size += 1
                        #print the score
                        print_obj.on_line(f"score: {main_snake.size} speed: {main_snake.speed}")
                    if SETTINGS["god_mode"]:
                        main_snake.draw_all()
                    elif not main_snake.alive:
                        game_loop = False
                #move the second snake
                """
                if SETTINGS["online"] and second_snake.move(borders = SETTINGS["game_borders"]):
                    if not second_snake.alive:
                        game_loop = False
                    if second_snake.apple_eaten:
                        game_canvas.new_apple()
                """
                #update the display
                game_canvas.update()
                sleep(0.01)
        sleep(0.3)
        print_obj.new_line(f"game {game_count}, score: {main_snake.size}")
        game_count += 1
    pygame.quit()
    return None

if __name__ == "__main__" and RUN:
    main()