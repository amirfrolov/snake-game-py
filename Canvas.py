import pygame
import random
from collections import deque
get_random_point = lambda range_x, range_y: (random.randrange(0,range_x), random.randrange(0,range_y))

APPLE_SIZE = 0.8
BODY_SIZE = 0.9
HEAD_COLOR = (255, 0, 0)    #red
APPLE_ID = 2
BLACK = (0,0,0)
APPLE_COLOR = (0,255,0)     #green

class Canvas:
    def __init__(self, table_size, screen_size, window_title):
        pygame.display.set_caption(window_title)
        self.table_size = table_size
        self.__screen_size = screen_size
        self.__window = pygame.display.set_mode(screen_size)
        self.clear()
        self.game_table = [[0 for i in range(table_size[1])] for j in range(table_size[0])]
        self.apples = deque()
        self.update_flag = False
    
    def update(self):
        if self.update_flag:
            pygame.display.update()
            self.update_flag = False
    
    def clear(self):
        self.__window.fill((0,0,0))
    
    def reset(self):
        self.game_table = [[0 for i in range(self.table_size[1])] for j in range(self.table_size[0])]
        self.clear()
        self.apples = deque()
        self.update_flag = False
    
    def block(self, place, relative_size = 1, color = None):
        self.update_flag = True
        # set x
        x_size = (self.__screen_size[0]/self.table_size[0])
        x_hist = x_size * (1 - relative_size)
        x = x_size* place[0]
        # set y
        y_size = (self.__screen_size[1]/self.table_size[1])
        y_hist = y_size * (1 - relative_size)
        y = y_size * place[1]
        #draw
        pygame.draw.rect(self.__window, BLACK, (x, y, x_size, y_size))
        if color:
            pygame.draw.rect(self.__window, color, (x + x_hist/2, y+ y_hist/2, x_size * relative_size, y_size * relative_size))
    
    def draw_apple(self, place):
        self.block(place, APPLE_SIZE, APPLE_COLOR)
    
    def new_apple(self):
        new_apple = get_random_point(self.table_size[0], self.table_size[1])
        while self.game_table[new_apple[0]][new_apple[1]]:
            new_apple = get_random_point(self.table_size[0], self.table_size[1])
        self.game_table[new_apple[0]][new_apple[1]] = APPLE_ID
        self.apples.append(tuple(new_apple))
        self.draw_apple(new_apple)

    def remove_apple(self, apple):
        self.apples.remove(tuple(apple))
    
    def draw_snake(self, snake_list, body_color):
        for i in snake_list:
            self.block(i, BODY_SIZE, body_color)
        head = snake_list[-1]
        self.block(head, BODY_SIZE, HEAD_COLOR)