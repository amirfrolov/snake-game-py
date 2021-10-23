#!/usr/bin/env python3

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 42069        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
    conn.connect((HOST, PORT))
    i = 1
    while True:
        print(i)
        conn.sendall(str.encode(str(i)))
        sleep(1)
        i+=1


#!/usr/bin/env python3
import os
from os.path import abspath #for opening files
os.chdir(os.path.dirname(__file__)) #set the path for opening files
from time import sleep
import socket #for the online
import pygame
#local imports
import Snake
import Canvas
import GameEvents
import PrintManager
from settings import SETTINGS, ARGV
#define
RUN = SETTINGS != None
if RUN:
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
#---------- main ----------#
def main():
    print_obj = PrintManager.PrintManager()
    print_obj.new_line("Suonds from: https://mixkit.co/free-sound-effects/game/")
    #set online
    online_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    online_socket.connect((HOST, PORT))
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
        main_snake = Snake.Snake(game_canvas, SETTINGS["snake_start_posotions"], SETTINGS['snake_color'], speed = SETTINGS["snake_speed"])
        #set snake start length
        if SETTINGS["snake_start_length"] > main_snake.size:
            main_snake.size = SETTINGS["snake_start_length"]
        #set the client snake
        if SETTINGS["server"]:
            client_snake = Snake.Snake(game_canvas, [[5, 3], [5, 4], [5, 5]],(0, 0, 255), 2)
            if SETTINGS["snake_start_length"] > client_snake.size:
                client_snake.size = SETTINGS["snake_start_length"]
        #set game
        print_obj.on_line(f"score: {main_snake.size}")
        game_canvas.new_apple()
        game_canvas.update()
        #the game loop
        game_loop = True
        while game_loop:
            #manage online
            socket_client_data = None
            if SETTINGS["server"]:
                try:
                    socket_client_data = socket_conn.recv(1024).decode()
                except socket.timeout:
                    pass
            #manage the keyboard
            game_event = GameEvents.handle_pygame_events(pygame.event.get(), pygame.key.get_pressed())
            if game_event.close_game:
                run = False
                game_loop = False
            elif game_event.restart:
                game_loop = False
            else: 
                #       continue the game - the game is playing
                #manage main_snake monement
                if game_event.pause:
                    main_snake.stop()
                if game_event.new_direction:
                    main_snake.add_direction(game_event.new_direction)
                if game_event.sprint:
                    main_snake.speed = SETTINGS["snake_speed_run"]
                else:
                    main_snake.speed = SETTINGS["snake_speed"]
                #manage client_snake movement
                if SETTINGS["server"] and socket_client_data:
                    if not client_snake.direction:
                        client_snake.direction = Snake.DIRECTION_DOWN
                    """
                    if not int(socket_client_data)%3:
                        client_snake.direction = Snake.DIRECTION_DOWN
                    else:
                        client_snake.direction = Snake.DIRECTION_LEFT
                    """
                    if not int(socket_client_data)%10:
                        client_snake.speed = SETTINGS["snake_speed_run"]
                
                #       --- game logics ---
                #move the main snake
                if main_snake.move(): # the snake moved
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
                if SETTINGS["server"] and client_snake.move():
                    if not client_snake.alive:
                        game_loop = False
                    if client_snake.apple_eaten:
                        game_canvas.new_apple()
                        #send sound play cmd
                        client_snake.size += 1
                #update the display
                game_canvas.update()
                sleep(0.01)
        if run: # time to see the game before reset
            sleep(0.3)
        print_obj.new_line(f"game {game_count}, score: {main_snake.size}")
        game_count += 1
    return None

if __name__ == "__main__" and RUN:
    pygame.init() #set pygame
    try:
        main()
    except KeyboardInterrupt:
        print(" -proggram sttoped")
    pygame.quit()