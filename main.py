#!/usr/bin/python3
import os
import sys
from os.path import abspath #for opening files
os.chdir(os.path.dirname(__file__)) #set the path for opening files
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
from settings import settings_obj
#define
STATE_SERVER = 2
STATE_MULTYPLAYER = 1
SETTINGS_FILE_NAME = "settings.json"

print_obj = PrintManager.PrintManager()
PROG_SETTINGS = settings_obj(abspath(SETTINGS_FILE_NAME))

def manage_snake(snake, game_events, god_mode=False):
    """apply the game_events and move the snake acord

    Args:
        snake (Snake): the snake object
        game_events (): [description]
        god_mode (bool, optional): [description]. Defaults to False.

    Returns:
        bool: if the snake moved
    """
    if game_events.pause:
        snake.stop()
    if game_events.new_direction:
        snake.add_direction(game_events.new_direction)
    if game_events.sprint:
        snake.speed = PROG_SETTINGS.data["snake_speed_run"]
    else:
        snake.speed = PROG_SETTINGS.data["snake_speed"]
    
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
    """logs the game with the variables"""
    to_print = f"game {game_count}, score: {score}"
    if game_events.close_game:
        to_print += ", Game closed"
    elif game_events.restart:
        to_print += ", Game restarted"
    elif not PROG_SETTINGS.data['state']:
        if win_flag:
            to_print += ", I won"
        else:
            to_print += ", I lost"
    print(to_print)

def set_server():
    """sets the server 

    Returns:
        TCP_manager.TCP_manager: tcp server object
    """
    online_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    online_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #set socket as reusable
    online_socket.bind((MY_IP, PROG_SETTINGS.data["port"]))
    TCP_manager.SOCKETS_TO_CLOSE.append(online_socket)
    online_socket.listen()
    print_obj.title("server")
    print("Server ip:", MY_IP)
    print("To connect run the 'client.py' file with the server ip. Example:")
    print(f"python3 client.py {MY_IP}")
    if "test" in PROG_SETTINGS.argv:
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
    if PROG_SETTINGS.get_argv(0) == "1" or PROG_SETTINGS.in_argv("multy"):
        PROG_SETTINGS.data["state"] = STATE_MULTYPLAYER
    elif PROG_SETTINGS.get_argv(0) == "2" or PROG_SETTINGS.in_argv("server"):
        PROG_SETTINGS.data["state"] = STATE_SERVER
    
    #print credits section
    print("Suonds from: https://mixkit.co/free-sound-effects/game/")
    print("Icon from: https://iconarchive.com/show/button-ui-requests-13-icons-by-blackvariant/Snake-icon.html")
    #print instructions section
    print_obj.title("help")
    print_obj.print_file(abspath("help.txt"))
    print_obj.title("instructions")
    if PROG_SETTINGS.data["state"] == STATE_MULTYPLAYER:
        print_obj.print_file("multyplayer_instructions.txt")
    else:
        print_obj.print_file("one_snake_instructions.txt")
    
    #help mode
    if any([i in sys.argv[1:] for i in ["-h", "--help"]]):
        run = False
    
    if run:
        window_title_adder = ""
        #set online
        if PROG_SETTINGS.data['state'] == STATE_SERVER: # server socket
            window_title_adder += " - Server"
            client_sock = set_server()
        print_obj.title("game log")
        #set sounds
        eat_sound = pygame.mixer.Sound(abspath(PROG_SETTINGS.data['eat_sound']))
        eat_sound.set_volume(PROG_SETTINGS.data["sound_volume"])
        eat_sound.play()
        #set canvas
        game_canvas = Canvas.Canvas(\
            PROG_SETTINGS.data["game_table"],\
            PROG_SETTINGS.data["game_screen"],\
            "Snake Game" + window_title_adder,\
            abspath(PROG_SETTINGS.data["game_icon"]))
        #set game
        game_count = 1
        while run:
            game_canvas.reset()
            main_snake = Snake.Snake(game_canvas,\
                PROG_SETTINGS.data["snake_start_posotions"],\
                PROG_SETTINGS.data['snake_color'],\
                PROG_SETTINGS.data["snake_start_length"],\
                PROG_SETTINGS.data["snake_speed"])
            #set the client snake
            if PROG_SETTINGS.data["state"]:
                client_snake = Snake.Snake(game_canvas,\
                    [[5, 3], [5, 4], [5, 5]],\
                    [0, 0, 255],\
                    PROG_SETTINGS.data["snake_start_length"],\
                    PROG_SETTINGS.data["snake_speed"])
                client_events = GameEvents.GameEvents()
            #set game
            print_obj.on_line(f"score: {main_snake.size}")
            for i in range(PROG_SETTINGS.data["apples_number"]):
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
                if PROG_SETTINGS.data["state"] == STATE_SERVER: #get data from client
                    connected, socket_client_data = client_sock.recv()
                    if not connected:
                        run = False
                        print_obj.new_line("Client disconnected.")
                    elif socket_client_data:
                        client_events = GameEvents.GameEvents(socket_client_data)
                elif PROG_SETTINGS.data["state"] == STATE_MULTYPLAYER:
                    client_events = GameEvents.handle_pygame_events(\
                        pygame_events,\
                        pygame_pressed_keys,\
                        letter_keys=False)
                #manage the keyboard
                game_events = GameEvents.handle_pygame_events(\
                    pygame_events,\
                    pygame_pressed_keys,\
                    arrow_keys = PROG_SETTINGS.data["state"] != STATE_MULTYPLAYER)
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
                    if manage_snake(main_snake, game_events, PROG_SETTINGS.data["god_mode"]):
                        update_flag = True
                        if main_snake.apple_eaten:
                            eat_sound.play()
                        if not main_snake.alive:
                            game_loop = False
                    
                    #move the second snake
                    if PROG_SETTINGS.data["state"] and manage_snake(client_snake, client_events, PROG_SETTINGS.data["god_mode"]):
                        update_flag = True
                        if not client_snake.alive:
                            game_loop = False
                    
                    if update_flag:
                        game_canvas.update()
                        if PROG_SETTINGS.data["state"] == STATE_SERVER:#send data to client
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