import pygame
import random
get_random_point = lambda range_x, range_y: (random.randrange(0,range_x), random.randrange(0,range_y))

APPLE_SIZE = 0.8
APPLE_ID = -1
BLACK = (0,0,0)
APPLE_COLOR = (0,255,0)     #green

class Canvas:
    def __init__(self, table_size, screen_size, caption):
        self.table_size = table_size
        self.__screen_size = screen_size
        self.__window = pygame.display.set_mode(screen_size)
        self.clear()
        pygame.display.set_caption(caption)
        self.game_table = [[0 for i in range(table_size[1])] for j in range(table_size[0])]
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

    def new_apple(self, color = APPLE_COLOR):
        new_apple = get_random_point(self.table_size[0], self.table_size[1])
        while self.game_table[new_apple[0]][new_apple[1]]:
            new_apple = get_random_point(self.table_size[0], self.table_size[1])
        self.game_table[new_apple[0]][new_apple[1]] = APPLE_ID
        #draws the apple
        self.block(new_apple, APPLE_SIZE, color)
