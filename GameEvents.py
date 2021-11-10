import pygame
import Snake

class GameEvents:
    close_game = False      #flag
    restart = False         #flag
    grow = False            #flag
    pause = False           #flag
    sprint = False
    new_direction = 0    #a new direction

    def __init__(self, data = None):
        if type(data) == str:
            self.close_game =   bool(int(data[0]))
            self.restart =      bool(int(data[1]))
            self.grow =         bool(int(data[2]))
            self.pause =        bool(int(data[3]))
            self.sprint =       bool(int(data[4]))
            self.new_direction= int(data[5])
    def export_to_str(self):
        return \
            str(int(self.close_game)) + \
            str(int(self.restart)) + \
            str(int(self.grow)) + \
            str(int(self.pause)) + \
            str(int(self.sprint)) + \
            str(self.new_direction) 

# retrun the GameEvents object with the actions to do
def handle_pygame_events(event_list, pressed_keys, letter_keys = True ,arrow_keys = True):
    key_event = GameEvents()
    for event in event_list:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                key_event.close_game = True
            elif event.key == pygame.K_r:
                key_event.restart = True
            elif event.key == pygame.K_p:
                key_event.pause = True
            
            #snake direction keys
            if letter_keys:
                if event.key == pygame.K_a:
                    key_event.new_direction = Snake.DIRECTION_LEFT
                elif event.key == pygame.K_d:
                    key_event.new_direction = Snake.DIRECTION_RIGHT
                elif event.key == pygame.K_s:
                    key_event.new_direction = Snake.DIRECTION_DOWN
                elif event.key == pygame.K_w:
                    key_event.new_direction = Snake.DIRECTION_UP
            if arrow_keys:
                if event.key == pygame.K_LEFT:
                    key_event.new_direction = Snake.DIRECTION_LEFT
                elif event.key == pygame.K_RIGHT:
                    key_event.new_direction = Snake.DIRECTION_RIGHT
                elif event.key == pygame.K_DOWN:
                    key_event.new_direction = Snake.DIRECTION_DOWN
                elif event.key == pygame.K_UP:
                    key_event.new_direction = Snake.DIRECTION_UP
                
        if event.type == pygame.QUIT:
            key_event.close_game = True
    if letter_keys and pressed_keys[pygame.K_SPACE]:
        key_event.sprint = True
    if arrow_keys and pressed_keys[pygame.K_RSHIFT]:
        key_event.sprint = True
    if pressed_keys[pygame.K_g]:
        key_event.grow = True
    
    return key_event

