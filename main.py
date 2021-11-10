#!/usr/bin/python3
import os
import sys
from os.path import abspath #for opening files
os.chdir(os.getcwd()) #set the path for opening files
from time import sleep
import socket #for the online
import pygame
from collections import deque
#local imports
import Snake
import Canvas
import GameEvents
import PrintManager
import TCP_manager
from TCP_manager import MY_IP
from settings import get_settings_and_argv
#get the settings from settings.json file
SETTINGS, ARGV = get_settings_and_argv(abspath("settings.json"))
#define
STATE_SERVER = 2
STATE_MULTYPLAYER = 1
print_obj = PrintManager.PrintManager()

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

def log_game(game_events, game_count, score, win_flag):
    to_print = f"game {game_count}, score: {score}"
    if game_events.close_game:
        to_print += ", Game closed"
    elif game_events.restart:
        to_print += ", Game restarted"
    elif not SETTINGS['state']:
        if win_flag:
            to_print += ", I won"
        else:
            to_print += ", I lost"
    print(to_print)

def set_server_and_get_client():
    online_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    online_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #set socket as reusable
    online_socket.bind((MY_IP, SETTINGS["port"]))
    TCP_manager.SOCKETS_TO_CLOSE.append(online_socket)
    online_socket.listen()
    print_obj.title("server")
    print("Server ip:", MY_IP)
    print("To connect run the 'client.py' file with the server ip. Example:")
    print(f"python3 client.py {MY_IP}")
    if "test" in ARGV:
        print("Connecting to the server localy... ('test' flag)")
        os.popen(f"sleep 0.5 && python3 client.py {MY_IP} >> client_out.txt")
    else:
        print("Waitting for connection...")
    return TCP_manager.TCP_manager(online_socket.accept()[0])

#---------- main ----------#
def main():
    run = True
    pygame.init() #set pygame
    #manage argv
    if "multy" in ARGV:
        SETTINGS["state"] = STATE_MULTYPLAYER
    elif "server" in ARGV:
        SETTINGS["state"] = STATE_SERVER
    
    #print credits section
    print("Suonds from: https://mixkit.co/free-sound-effects/game/")
    print("Icon from: https://iconarchive.com/show/button-ui-requests-13-icons-by-blackvariant/Snake-icon.html")
    #print instructions section
    print_obj.title("help")
    print_obj.print_file(abspath("help.txt"))
    print_obj.title("instructions")
    if SETTINGS["state"] == STATE_MULTYPLAYER:
        print_obj.print_file("multyplayer_instructions.txt")
    else:
        print_obj.print_file("one_snake_instructions.txt")
    
    #help mode
    if any([i in sys.argv[1:] for i in ["-h", "--help"]]):
        run = False
    
    if run:
        window_title_adder = ""
        #set online
        if SETTINGS['state'] == STATE_SERVER: # server socket
            window_title_adder += " - Server"
            client_sock = set_server_and_get_client()
        print_obj.title("game log")
        #set sounds
        eat_sound = pygame.mixer.Sound(abspath(SETTINGS['eat_sound']))
        eat_sound.set_volume(SETTINGS["sound_volume"])
        eat_sound.play()
        #set canvas
        game_canvas = Canvas.Canvas(\
            SETTINGS["game_table"],\
            SETTINGS["game_screen"],\
            "Snake Game" + window_title_adder,\
            abspath(SETTINGS["game_icon"]))
        #set game
        game_count = 1
        while run:
            game_canvas.reset()
            main_snake = Snake.Snake(game_canvas,\
                SETTINGS["snake_start_posotions"],\
                SETTINGS['snake_color'],\
                SETTINGS["snake_start_length"],\
                SETTINGS["snake_speed"])
            #set the client snake
            if SETTINGS["state"]:
                client_snake = Snake.Snake(game_canvas,\
                    [[5, 3], [5, 4], [5, 5]],\
                    [0, 0, 255],\
                    SETTINGS["snake_start_length"],\
                    SETTINGS["snake_speed"])
                client_events = GameEvents.GameEvents()
            #set game
            print_obj.on_line(f"score: {main_snake.size}")
            for i in range(SETTINGS["apples_number"]):
                game_canvas.new_apple()
            update_flag = True
            win_flag = False
            #the game loop
            game_loop = True
            while game_loop:
                #set pygame values
                pygame_events = pygame.event.get()
                pygame_pressed_keys = pygame.key.get_pressed()
                #manage online
                if SETTINGS["state"] == STATE_SERVER: #get data from client
                    connected, socket_client_data = client_sock.recv()
                    if not connected:
                        run = False
                        print_obj.new_line("Client disconnected.")
                    elif socket_client_data:
                        client_events = GameEvents.GameEvents(socket_client_data)
                elif SETTINGS["state"] == STATE_MULTYPLAYER:
                    client_events = GameEvents.handle_pygame_events(\
                        pygame_events,\
                        pygame_pressed_keys,\
                        letter_keys=False)
                #manage the keyboard
                game_events = GameEvents.handle_pygame_events(\
                    pygame_events,\
                    pygame_pressed_keys,\
                    arrow_keys = SETTINGS["state"] != STATE_MULTYPLAYER)
                if game_events.close_game:
                    run = False
                elif game_events.restart:
                    game_loop = False
                #exit game_loop if run is False
                if not run:
                    game_loop = False
                #       continue the game - the game is playing
                if game_loop:
                    #move the main snake
                    if manage_snake(main_snake, game_events, SETTINGS["god_mode"]):
                        update_flag = True
                        if main_snake.apple_eaten:
                            eat_sound.play()
                        if not main_snake.alive:
                            game_loop = False
                    
                    #move the second snake
                    if SETTINGS["state"] and manage_snake(client_snake, client_events, SETTINGS["god_mode"]):
                        update_flag = True
                        if not client_snake.alive:
                            game_loop = False
                    
                    if update_flag:
                        game_canvas.update()
                        if SETTINGS["state"] == STATE_SERVER:#send data to client
                            data_to_send = f'[[{main_snake.get_draw_data()},{client_snake.get_draw_data()}],{str(game_canvas.apples)[6:-1]}]'
                            client_sock.send(data_to_send)
                        print_obj.on_line(f"score: {main_snake.size} speed: {main_snake.speed}")
                        win_flag = main_snake.alive
                        update_flag = False
                if game_loop:
                    #time to sleep before every frame
                    sleep(0.01)
            if run:
                # time to see the game before reset
                sleep(0.3)
            log_game(game_events, game_count, main_snake.size, win_flag)
            game_count += 1
    return None

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(" -proggram sttoped")
    except BrokenPipeError:
        print("BrokenPipeError")
    pygame.quit()
    TCP_manager.close_all()