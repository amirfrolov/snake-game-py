#!/usr/bin/env python3
import os
from os.path import abspath #for opening files
os.chdir(os.getcwd()) #set the path for opening files
from time import sleep
import pygame
from ast import literal_eval
#local imports
import Snake
import Canvas
import GameEvents
import PrintManager
import TCP_manager
from settings import SETTINGS, ARGV
#define
RUN = SETTINGS != None
if RUN:
    if len(ARGV):
        HOST = ARGV[0]
    else:
        HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
#---------- main ----------#
def main():
    print_obj = PrintManager.PrintManager()
    print_obj.new_line("Suonds from: https://mixkit.co/free-sound-effects/game/")
    #set online
    server_tcp_obj = TCP_manager.TCP_manager()
    server_tcp_obj.connect(HOST, SETTINGS["port"])
    #set sounds
    eat_sound = pygame.mixer.Sound(abspath(SETTINGS['eat_sound']))
    eat_sound.set_volume(SETTINGS["sound_volume"])
    eat_sound.play()
    #set canvas
    game_canvas = Canvas.Canvas(SETTINGS["game_table"], SETTINGS["game_screen"], "Snake Game - Client")
    #set game
    game_count = 1
    run = True
    last_sent_data = ""
    while run:
        connected, socket_server_str = server_tcp_obj.recv()
        if not connected:
            print("disconnected")
            run = False
        elif socket_server_str: #handle server data
            game_canvas.clear()
            try:
                server_data = literal_eval(socket_server_str)
            except ValueError:
                print("ValueError")
                print(socket_server_str)
                run = False
                break
            #draw the snakes
            for i in server_data[0]:
                snake_list, body_color = i
                game_canvas.draw_snake(snake_list, body_color)
            #draw the apples
            for i in server_data[1]:
                game_canvas.draw_apple(i)
            game_canvas.update()
        
        #manage the keyboard
        if run:
            game_events = GameEvents.handle_pygame_events(pygame.event.get(), pygame.key.get_pressed())
            if game_events.close_game:
                run = False
            #send data to the server 
            game_events_str = game_events.export_to_str()
            if game_events_str != last_sent_data: #send only new data
                last_sent_data = game_events_str
                server_tcp_obj.send(game_events_str)
        
        sleep(1/100)
    return None

if __name__ == "__main__" and RUN:
    pygame.init() #set pygame
    try:
        main()
    except KeyboardInterrupt:
        print(" -proggram sttoped")
    except ConnectionRefusedError:
        print("ConnectionRefusedError")
    except BrokenPipeError:
        pass
    pygame.quit()
    print("Closed", len(TCP_manager.SOCKETS_TO_CLOSE), "sockets")
    TCP_manager.close_all()
