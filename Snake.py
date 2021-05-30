from collections import deque
from searchTable import Table
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
BODY_COLOR = (50,164,231)   #blue
HEAD_COLOR = (255, 0, 0)    #red

BACKGROUND_BLOCK_TOUNE = 0
BACKGROUND_BLOCK_COLOR = (BACKGROUND_BLOCK_TOUNE,BACKGROUND_BLOCK_TOUNE,BACKGROUND_BLOCK_TOUNE)
#sizes
BODY_SIZE = 0.9
BACKGROUND_SIZE = 0.8


def block(win, place, relative_size, color):
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
    pygame.draw.rect(win, color, (x + x_hist/2, y+ y_hist/2, x_size * relative_size, y_size * relative_size))

def draw_background(win):
    win.fill((0,0,0))
    """
    for x in range(TABLE_SIZE[0]):
        for y in range(TABLE_SIZE[1]):
            block(win, (x, y), BACKGROUND_SIZE, BACKGROUND_BLOCK_COLOR)
    """

def get_random_point():
    return (random.randrange(0,TABLE_SIZE[0]), random.randrange(0,TABLE_SIZE[1]))

def new_apple(win, snake_list, color):
    new_apple = get_random_point()
    while any([i.is_interappted(new_apple) for i in snake_list]):
        new_apple = get_random_point()
    #draws the apple
    block(win, new_apple, BACKGROUND_SIZE, color)
    return new_apple

class Snake:
    def __init__(self, values_list, body_color = BODY_COLOR, speed = 10, id = 0):
        self.id = id
        self.size = len(values_list)
        self.deque_list = deque(values_list)
        self.seach_table = Table(values_list)
        self.direction_list = deque()
        self.direction = None
        self.head = None
        self.timer = Timer()
        self.speed = speed
        #colors
        self.body_color = body_color
    
    def draw_all(self, win):
        head = self.deque_list.pop()
        for i in self.deque_list:
            block(win, i, BODY_SIZE, self.body_color)
        block(win, head, BODY_SIZE, HEAD_COLOR)
        self.deque_list.append(head)
    """
    def grow(self):
        self.size+=1
        last_body = self.deque_list[0]
        self.deque_list.appendleft(last_body)
    """
    def is_interappted(self, point):
        return self.seach_table.find(point) or point == self.head
    
    def get_head(self):
        return self.head
    
    def add_direction(self, key):
        if key == pygame.K_a or key == pygame.K_LEFT:
            new_direction = DIRECTION_LEFT
        elif key == pygame.K_d or key == pygame.K_RIGHT:
            new_direction = DIRECTION_RIGHT
        elif key == pygame.K_s or key == pygame.K_DOWN:
            new_direction = DIRECTION_DOWN
        elif key == pygame.K_w or key == pygame.K_UP:
            new_direction = DIRECTION_UP
        else:
            return None
        #set direction if there is not
        if not self.direction:
            self.direction = new_direction
            return None
        #check if the move is valid
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
    
    def move(self, win, borders = False):
        """returns if the snake moved"""
        if self.direction and self.speed:
            if self.timer.loop(1/self.speed):
                if self.head:
                    self.deque_list.append(self.head)
                    self.seach_table.insert(self.head)
                    
                if self.size == len(self.deque_list):
                    #delete the last place
                    last_place = self.deque_list.popleft()
                    self.seach_table.remove(last_place)
                    #draw on the last place
                    block(win, last_place, BACKGROUND_SIZE, BACKGROUND_BLOCK_COLOR)
                
                #remove the last head
                head = self.deque_list[-1]
                block(win, head, BODY_SIZE, self.body_color)
                #set the new direction
                if self.direction_list:
                    self.direction = self.direction_list.popleft()
                #set the new head
                head = list(head)
                if self.direction == 'u':
                    head[1]-=1
                elif self.direction == 'd':
                    head[1]+=1
                elif self.direction == 'l':
                    head[0]-=1
                elif self.direction == 'r':
                    head[0]+=1
                #borders
                if not borders:
                    for i in range(2):
                        if head[i] < 0:
                            head[i] = TABLE_SIZE[i] - 1
                        elif head[i] == TABLE_SIZE[i]:
                            head[i] = 0
                
                head = tuple(head)
                #draw the new head
                block(win, head, BODY_SIZE, HEAD_COLOR)
                #add the new head
                self.head = head
                return True
        else:
            self.timer.reset()
        return False
    
    def is_alive(self, borders = False):
        head = self.head
        alive = not self.seach_table.find(head)
        #check if the snake got out of the borders
        if borders and alive:
            alive = not (head[0] < 0 or head[0] == TABLE_SIZE[0] or head[1] < 0 or head[1] == TABLE_SIZE[1])
        return alive
        
        


