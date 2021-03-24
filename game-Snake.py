import sys, os
import pygame
import random
import time
from collections import deque
from searchTable import Table
from Timer import Timer

#           height / width
SCREEN_SIZE = (1200, 800)
TABLE_SIZE = [42, 28]
#colors
BLACK = (0,0,0)
BODY_COLOR = (50,164,231)   #blue
APPLE_COLOR = (0,255,0)     #green
HEAD_COLOR = (255, 0, 0)    #red
BACKGROUND_COLOR = (150,150,150)
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
    for x in range(TABLE_SIZE[0]):
        for y in range(TABLE_SIZE[1]):
            block(win, (x, y), BACKGROUND_SIZE, BACKGROUND_COLOR)

def get_random_point():
    return (random.randrange(0,TABLE_SIZE[0]), random.randrange(0,TABLE_SIZE[1]))

def new_apple(win, snake_list):
    new_apple = get_random_point()
    while any([i.is_interappted(new_apple) for i in snake_list]):
        new_apple = get_random_point()
    #draws the apple
    block(win, new_apple, BACKGROUND_SIZE, APPLE_COLOR)
    return new_apple

class Snake:
    def __init__(self, values_list):
        self.size = len(values_list)
        self.deque_list = deque(values_list)
        self.seach_table = Table(values_list)
        self.direction_list = deque()
        self.direction = None
    
    def draw(self, win):
        head = self.deque_list.pop()
        for i in self.deque_list:
            block(win, i, BODY_SIZE, BODY_COLOR)
        block(win, head, BODY_SIZE, HEAD_COLOR)
        self.deque_list.append(head)
    
    def grow(self):
        self.size+=1
        last_body = self.deque_list[0]
        self.deque_list.appendleft(last_body)
    
    def is_interappted(self, point):
        return self.seach_table.find(point)
    
    def get_head(self):
        return self.deque_list[-1]

    def add_direction(self, key):
        if key == pygame.K_a:
            new_direction = 'l'
        elif key == pygame.K_d:
            new_direction = 'r'
        elif key == pygame.K_s:
            new_direction = 'd'
        elif key == pygame.K_w:
            new_direction = 'u'
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
        
        if (new_direction == 'r' or new_direction == 'l') and (tmp_direction == 'r' or tmp_direction == 'l'):
            return None
        elif (new_direction == 'u' or new_direction == 'd') and (tmp_direction == 'u' or tmp_direction == 'd'):
            return None
        self.direction_list.append(new_direction)
        
    def move(self, win):
        """returns True if the snake dies"""
        #delete the last place
        last_place = self.deque_list.popleft()
        self.seach_table.remove(last_place)
        #draw on the last place
        block(win, last_place, BACKGROUND_SIZE, BACKGROUND_COLOR)
        
        #remove the last head
        head = self.deque_list[-1]
        block(win, head, BODY_SIZE, BODY_COLOR)
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
        head = tuple(head)
        is_dead = self.seach_table.find(head)
        #draw the new head
        block(win, head, BODY_SIZE, HEAD_COLOR)
        #add the new head
        self.deque_list.append(head)
        self.seach_table.insert(head)
        if not is_dead:
            if head[0] not in range(0, TABLE_SIZE[0]) or head[1] not in range(0, TABLE_SIZE[1]):
                is_dead = True
        return is_dead



#play music
def play_mp3(path):
    import subprocess
    subprocess.Popen(['mpg123', '-q', path])

def main():
    pygame.init()
    win = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("snake game")
    draw_background(win)

    snake = Snake([(2, 3), (2, 4), (2, 5)])
    snake.draw(win)
    apple = None

    main_game_timer = Timer()
    run = True
    while run:
        #manage the keyboard
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                snake.add_direction(event.key)
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_g:
                    snake.grow()
            if event.type == pygame.QUIT:
                run = False
                break
        #   >>game loop<<
        if(main_game_timer.loop(0.25)):
            #move the snake
            if snake.direction:
                #returns if the snake is dead
                run = not snake.move(win)
            #set apple
            if snake.get_head() == apple:
                #play_mp3('/home/amir/Desktop/eat.mp3')
                snake.grow()
                apple = None
            if apple == None:
                apple = new_apple(win, [snake])
            pygame.display.update()
        
        time.sleep(0.01)
    pygame.quit()
    print("stopped, score:", snake.size)
    return None

if __name__ == "__main__":
    main()
