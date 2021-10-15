import pygame
import Snake

class GameEvents:
    close_game = False      #flag
    restart = False         #flag
    grow = False            #flag
    pause = False           #flag
    sprint = False
    new_direction = None    #a new direction

# retrun the GameEvents object with the actions to do
def handle_pygame_events(event_list, pressed_keys):
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
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                key_event.new_direction = Snake.DIRECTION_LEFT
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                key_event.new_direction = Snake.DIRECTION_RIGHT
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                key_event.new_direction = Snake.DIRECTION_DOWN
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                key_event.new_direction = Snake.DIRECTION_UP
            
        if event.type == pygame.QUIT:
            key_event.close_game = True
    
    if pressed_keys[pygame.K_SPACE]:
        key_event.sprint = True
    if pressed_keys[pygame.K_g]:
        key_event.grow = True
    
    return key_event

