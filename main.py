#!/usr/bin/env python3
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
from settings import SETTINGS, ARGV
#define
RUN = SETTINGS != None
if RUN:
    if "server" in ARGV:
        SETTINGS["server"] == True
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)

def manage_snake(snake, game_events, god_mode=False):
    if game_events.pause:
        snake.stop()
    if game_events.new_direction:
        snake.add_direction(game_events.new_direction)
    if game_events.sprint:
        snake.speed = SETTINGS["snake_speed_run"]
    else:
        snake.speed = SETTINGS["snake_speed"]
    
    grow = game_events.grow
    snake_moved = snake.move()
    if snake_moved:
        if snake.alive:
            if snake.apple_eaten:
                snake.canvas.new_apple()
                grow = True
            if grow:
                snake.size += 1
        if god_mode:
            snake.draw_all()
            snake.alive = True
    return snake_moved

#---------- main ----------#
def main():
    print_obj = PrintManager.PrintManager()
    print_obj.new_line("Suonds from: https://mixkit.co/free-sound-effects/game/")
    #set online
    if SETTINGS["server"]: # server socket
        online_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        online_socket.bind((HOST, SETTINGS["port"]))
        online_socket.listen()
        print("waitting for connection...")
        socket_conn, addr = online_socket.accept()
        socket_conn.settimeout(1/50)
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
        main_snake = Snake.Snake(game_canvas,\
            SETTINGS["snake_start_posotions"],\
            SETTINGS['snake_color'],\
            SETTINGS["snake_start_length"],\
            SETTINGS["snake_speed"])
        #set the client snake
        if SETTINGS["server"] or "test" in ARGV:
            client_snake = Snake.Snake(game_canvas,\
                [[5, 3], [5, 4], [5, 5]],\
                (0, 0, 255),\
                SETTINGS["snake_start_length"],\
                SETTINGS["snake_speed"])
        #set game
        print_obj.on_line(f"score: {main_snake.size}")
        game_canvas.new_apple()
        game_canvas.update()
        win = False
        #the game loop
        game_loop = True
        while game_loop:
            #manage online
            socket_client_data = None
            if SETTINGS["server"]: #get data from client
                try:
                    socket_client_data = socket_conn.recv(1024).decode()
                except socket.timeout:
                    pass
            #manage the keyboard
            game_events = GameEvents.handle_pygame_events(pygame.event.get(), pygame.key.get_pressed())
            if game_events.close_game:
                run = False
                game_loop = False
            elif game_events.restart:
                game_loop = False
            else:#       continue the game - the game is playing
                update_flag = False
                #move the main snake
                if manage_snake(main_snake, game_events, SETTINGS["god_mode"]):
                    update_flag = True
                    #print the score
                    print_obj.on_line(f"score: {main_snake.size} speed: {main_snake.speed}")
                    if main_snake.apple_eaten:
                        eat_sound.play()
                    if not main_snake.alive:
                        game_loop = False
                
                #move the second snake
                game_events.pause = False
                if (SETTINGS["server"] or "test" in ARGV) and manage_snake(client_snake, game_events):
                    update_flag = True
                    if not client_snake.alive:
                        game_loop = False
                
                if update_flag: #if snake moved
                    game_canvas.update()
                    if not game_loop:
                        win = main_snake.alive
                sleep(0.01)
        if run: # time to see the game before reset
            sleep(0.3)
        #log the game
        to_print = f"game {game_count}, score: {main_snake.size}"
        if game_events.close_game:
            to_print += ", Game closed"
        elif game_events.restart:
            to_print += ", Game restarted"
        elif SETTINGS["server"] or "test" in ARGV:
            if win:
                to_print += ", I won"
            else:
                to_print += ", I lost"
        print_obj.new_line(to_print)
        
        game_count += 1
    return None

if __name__ == "__main__" and RUN:
    pygame.init() #set pygame
    try:
        main()
    except KeyboardInterrupt:
        print(" -proggram sttoped")
    pygame.quit()