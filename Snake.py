from collections import deque
from Timer import Timer
import pygame
import Canvas

DIRECTION_RIGHT = 1
DIRECTION_LEFT = 2
DIRECTION_UP = 3
DIRECTION_DOWN = 4

HEAD_COLOR = (255, 0, 0)    #red
#sizes
BODY_SIZE = 0.9
APPLE_ID = 2
SNAKE_ID = 1

class Snake:
    def __init__(self, game_canvas, values_list, body_color, start_length = 5, speed = 10):
        """[summary]TODO
        
        Args:
            game_canvas (Canvas): the game canvas
            values_list ([type]): [description]
            body_color ([type]): [description]
            speed (int, optional): [description]. Defaults to 10.
            snake_id (int, optional): [description]. Defaults to 1.
        """
        self.canvas = game_canvas
        self.game_table = game_canvas.game_table
        #set the snake in the game_table
        for i in values_list:
            self.game_table[i[0]][i[1]] = SNAKE_ID
        self.size = len(values_list)
        if self.size < start_length:
            self.size = start_length
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
        self.draw_all()
    
    def draw_all(self):
        self.canvas.draw_snake(self.deque_list, self.body_color)
    
    def get_draw_data(self):
        #for online info
        return f"({str(self.deque_list)[6:-1]},{str(self.body_color)})"

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
                self.direction_list.clear()
                self.direction_list.append(new_direction)
            return None
        if self.direction_list:
            tmp_direction = self.direction_list[-1]
        else:
            tmp_direction = self.direction
        #if the snake trys to move in the direction he is moving
        if (new_direction == DIRECTION_LEFT or new_direction == DIRECTION_RIGHT) and (tmp_direction == DIRECTION_LEFT or tmp_direction == DIRECTION_RIGHT):
            return None
        elif (new_direction == DIRECTION_UP or new_direction == DIRECTION_DOWN) and (tmp_direction == DIRECTION_UP or tmp_direction == DIRECTION_DOWN):
            return None
        self.direction_list.append(new_direction)
    
    def stop(self):
        self.direction = None

    def move(self, borders = False):
        """returns if the snake moved"""
        if self.direction and self.speed:
            if self.timer.loop(1/self.speed):
                if self.size == len(self.deque_list):
                    #delete the last place
                    last_place = self.deque_list.popleft()
                    self.game_table[last_place[0]][last_place[1]] = 0
                    #draw on the last place
                    self.canvas.block(last_place)
                #remove the last head
                head = self.get_head()
                self.canvas.block(head, BODY_SIZE, self.body_color)
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
                            head[i] = self.canvas.table_size[i] - 1
                        elif head[i] == self.canvas.table_size[i]:
                            head[i] = 0
                #check if the snake got out of the borders
                if borders:
                    self.alive = not (head[0] < 0 or head[0] == self.canvas.table_size[0] or head[1] < 0 or head[1] == self.canvas.table_size[1])
                if not borders or (borders and self.alive):
                    #draw the new head
                    self.canvas.block(head, BODY_SIZE, HEAD_COLOR)
                    #eat apple
                    self.apple_eaten = self.game_table[head[0]][head[1]] == APPLE_ID
                    
                    if self.apple_eaten:
                        self.canvas.remove_apple(head)
                        #self.size += 1
                        pass
                    else: #if the snake has eaten an apple the squere is not 0
                        #check if alive
                        self.alive = self.game_table[head[0]][head[1]] == 0
                    #add the new head
                    self.game_table[head[0]][head[1]] = SNAKE_ID
                    self.deque_list.append(head)
                return True
        else:
            self.timer.reset()
        return False