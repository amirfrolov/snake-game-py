from collections import deque
from Timer import Timer
import pygame
import random

DIRECTION_RIGHT = 'r'
DIRECTION_LEFT = 'l'
DIRECTION_UP = 'u'
DIRECTION_DOWN = 'd'

#           height / width
SCREEN_SIZE = (1200, 800)
TABLE_SIZE = [42, 28]
#colors
BLACK = (0,0,0)
HEAD_COLOR = (255, 0, 0)    #red
APPLE_COLOR = (0,255,0)     #green
#sizes
BODY_SIZE = 0.9
APPLE_SIZE = 0.8

APPLE_ID = -1

def block(win, place, relative_size = 1, color = None):
    # set x
    x_size = (SCREEN_SIZE[0]/TABLE_SIZE[0])
    x_hist = x_size * (1 - relative_size)
    x = x_size* place[0]
    # set y
    y_size = (SCREEN_SIZE[1]/TABLE_SIZE[1])
    y_hist = y_size * (1 - relative_size)
    y = y_size * place[1]
    #draw
    pygame.draw.rect(win, BLACK, (x, y, x_size, y_size))
    if color:
        pygame.draw.rect(win, color, (x + x_hist/2, y+ y_hist/2, x_size * relative_size, y_size * relative_size))

get_random_point = lambda : (random.randrange(0,TABLE_SIZE[0]), random.randrange(0,TABLE_SIZE[1]))
def new_apple(win, game_table, color = APPLE_COLOR):
    new_apple = get_random_point()
    while game_table[new_apple[0]][new_apple[1]]:
        new_apple = get_random_point()
    game_table[new_apple[0]][new_apple[1]] = APPLE_ID
    #draws the apple
    block(win, new_apple, APPLE_SIZE, color)

class Snake:
    def __init__(self, game_table, values_list, body_color, speed = 10, snake_id = 1):
        self.id = snake_id
        self.game_table = game_table
        #set the snake in the game_table
        for i in values_list:
            self.game_table[i[0]][i[1]] = self.id
        self.size = len(values_list)
        self.deque_list = deque(values_list)
        self.direction_list = deque()
        self.direction = None
        #TODO replace with get_head 
        self.timer = Timer()
        self.speed = speed
        self.body_color = body_color
        #flages
        self.alive = True
        self.apple_eaten = False
    
    def draw_all(self, win):
        head = self.deque_list.pop()
        for i in self.deque_list:
            block(win, i, BODY_SIZE, self.body_color)
        block(win, head, BODY_SIZE, HEAD_COLOR)
        self.deque_list.append(head)
    
    def get_head(self):
        return list(self.deque_list[-1])
    
    def add_direction(self, new_direction):
        #set direction if there is not
        if not self.direction:
            new_head = self.get_head()
            if new_direction == DIRECTION_UP:
                new_head[1]-=1
            elif new_direction == DIRECTION_DOWN:
                new_head[1]+=1
            elif new_direction == DIRECTION_LEFT:
                new_head[0]-=1
            elif new_direction == DIRECTION_RIGHT:
                new_head[0]+=1
            if new_head != self.deque_list[-2]:
                self.direction = new_direction
                self.direction_list.append(new_direction)
            return None
        if self.direction_list:
            tmp_direction = self.direction_list[-1]
        else:
            tmp_direction = self.direction
        #if the snake trys to move in the direction he is moving
        if (new_direction == 'r' or new_direction == 'l') and (tmp_direction == 'r' or tmp_direction == 'l'):
            return None
        elif (new_direction == 'u' or new_direction == 'd') and (tmp_direction == 'u' or tmp_direction == 'd'):
            return None
        self.direction_list.append(new_direction)
    
    def stop(self):
        self.direction = None

    def move(self, win, borders = False):
        """returns if the snake moved"""
        if self.direction and self.speed:
            if self.timer.loop(1/self.speed):
                if self.size == len(self.deque_list):
                    #delete the last place
                    last_place = self.deque_list.popleft()
                    self.game_table[last_place[0]][last_place[1]] = 0
                    #draw on the last place
                    block(win, last_place)
                #remove the last head
                head = self.get_head()
                block(win, head, BODY_SIZE, self.body_color)
                #set the new direction
                if self.direction_list:
                    self.direction = self.direction_list.popleft()
                #set the new head
                if self.direction == DIRECTION_UP:
                    head[1]-=1
                elif self.direction == DIRECTION_DOWN:
                    head[1]+=1
                elif self.direction == DIRECTION_LEFT:
                    head[0]-=1
                elif self.direction == DIRECTION_RIGHT:
                    head[0]+=1
                #borders
                if not borders:
                    for i in range(2):
                        if head[i] < 0:
                            head[i] = TABLE_SIZE[i] - 1
                        elif head[i] == TABLE_SIZE[i]:
                            head[i] = 0
                #check if the snake got out of the borders
                if borders:
                    self.alive = not (head[0] < 0 or head[0] == TABLE_SIZE[0] or head[1] < 0 or head[1] == TABLE_SIZE[1])
                if not borders or (borders and self.alive):
                    #draw the new head
                    block(win, head, BODY_SIZE, HEAD_COLOR)
                    #eat apple
                    self.apple_eaten = self.game_table[head[0]][head[1]] == APPLE_ID
                    if self.apple_eaten:
                        self.size += 1
                    else:
                        #check if alive
                        self.alive = self.game_table[head[0]][head[1]] == 0
                    #add the new head
                    self.game_table[head[0]][head[1]] = self.id
                    self.deque_list.append(head)
                return True
        else:
            self.timer.reset()
        return False


