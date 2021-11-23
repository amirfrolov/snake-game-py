#!/usr/bin/env python3
import os
from os.path import abspath #for opening files
os.chdir(os.getcwd()) #set the path for opening files
from time import sleep
import pygame
from ast import literal_eval
import socket
#local imports
import Snake
import Canvas
import GameEvents
import PrintManager
import TCP_manager
from settings import settings_obj
#define
print_obj = PrintManager.PrintManager()
#---------- main ----------#
def main():
    settings = settings_obj(abspath("settings.json"))
    run = True
    #set online
    try:
        if len(settings.argv):
            host_ip = settings.argv[0]
        else:
            print("Not found the server ip in the argumants.")
            print("To connect to the server instantly send the server ip in the argumants.")
            print("Example: python3 client.py [server ip]")
            host_ip = input("Enter the server ip: ")
        server_tcp_obj = TCP_manager.TCP_manager(connect_addr=(host_ip, settings.data["port"]))
    except socket.timeout:
        print(f"Server time out [{host_ip}]")
        return None
    #set sounds
    eat_sound = pygame.mixer.Sound(abspath(settings.data['eat_sound']))
    eat_sound.set_volume(settings.data["sound_volume"])
    eat_sound.play()
    #set canvas
    game_canvas = Canvas.Canvas(settings.data["game_table"], settings.data["game_screen"], "Snake Game - Client")
    #set game
    game_count = 1
    last_sent_data = ""
    while run:
        connected, socket_server_str = server_tcp_obj.recv()
        if not connected:
            print("disconnected")
            run = False
        elif socket_server_str: #handle server data
            flag = False
            try:
                server_data = literal_eval(socket_server_str)
                flag = True
            except ValueError:
                print("ValueError")
                print(socket_server_str)
            if flag:
                game_canvas.clear()
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

if __name__ == "__main__":
    print("Suonds from: https://mixkit.co/free-sound-effects/game/")
    pygame.init()  #set pygame
    print('-' * 20)
    print("ctrl+c to exit the proggram")
    try:
        main()
    except KeyboardInterrupt:
        print(" -proggram sttoped")
    except ConnectionRefusedError:
        print("ConnectionRefusedError")
    except BrokenPipeError:
        pass
    pygame.quit()
    TCP_manager.close_all()
