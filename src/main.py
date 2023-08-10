import random
import pygame
from objects import *
from random import randint
import sys

pygame.init()

# Screen properties
screen = pygame.display.set_mode((480, 624))
screen_width = screen.get_size()[0]
screen_height = screen.get_size()[1]

white = (255, 255, 255)
black = (0, 0, 0)

REDCODE = "\x1b[31m"
GREENCODE = "\x1b[32m"
RESETCODE = "\x1b[0m"

# PREPARATION OF THE STARTING BALLS #############################################################################################################

# "default" is a Ball instance that will be used in the main, and will be the 'skeleton' of other Ball instances.
# It is important to have it in order to use certain class attributes that cannot be accessed in the creating of the instance.
default = Ball(0,0)

num_balls = random.randint(45, 55)
startX = randint(int(default.radius*screen_width),int(screen_width - default.radius*screen_width))
startY = int(screen_height - default.radius*screen_width)-1
balls_list = [Ball(x=startX, y=startY) for _ in range(num_balls)]

for ball in balls_list:
    ball.display(screen)
pygame.display.update()


# PREPARATION OF THE STARTING BLOCKS ############################################################################################################

blocks_list = [[None] * int(screen_height / (Block.length * screen_width)) for j in range(int(1 / Block.length))]

#Prepare starting blocks
allowed_area = 0.75
blocks_column = screen_height / (Block.length * screen_width)

for i in range(int(blocks_column*allowed_area)+1):
    for j in range(int(len(blocks_list))):
        if random.random() < 0.3:
            obj=Block(x=i*Block.length*screen_width, y=j*Block.length*screen_width)
            obj.set_rect(screen)
            obj.set_hp(screen)
            obj.update_color()
            obj.display(screen)
            obj.display_hp(screen)
            blocks_list[i][j] = obj
pygame.display.update()

# The functions that run on each ball
def ball_run(ball1: Ball):
    counter = 0
    for _ in range(40):
        ball1.update_rect(screen)
        ball1.move(dist=1)
        ball1.check_wall(screen)
        for sublist in blocks_list:
            for block in sublist:
                if isinstance(block, Block):
                    if block.activated:
                        check2(ball1, block, screen)
                        block.if_die(screen)
                else:
                    continue
        if counter == 30:
            ball1.erase(screen)
            ball1.display(screen)
            ball1.last_x = ball1.x
            ball1.last_y = ball1.y
            counter = 0
        else:
            counter += 1

block_len = Block.length * screen_width


# THE WHILE LOOP ################################################################################################################################
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse = mouse_press()
    for ball in balls_list:
        ball.set_angle(mouse[0], mouse[1])
        ball.set_inter_y()

    balls_list[0].activated = True
    while any(ball.activated for ball in balls_list):
        for ball in balls_list:
            ball.activated = True
            for ball2 in balls_list:
                if ball2.activated:
                    ball_run(ball2)
            pygame.display.update()

    if any(isinstance(block, Block) and block.activated for sublist in blocks_list for block in sublist):
        ball = None
        del ball2
        del mouse
        Ball.next_x = None
        Ball.next_y = None
        for ball in balls_list:
            ball.y = 616
            ball.up = True
            ball.inter_y = None
            ball.angle = None
            ball.last_x = ball.x
            ball.last_y = ball.y
    else:
        print(GREENCODE + "You win!" + RESETCODE)
        mouse_press()
        sys.exit()

    for sublist in blocks_list:
        for item in sublist:
            if isinstance(item, Block):
                item.erase(screen)
                item.move(screen)

    for sublist in blocks_list:
        for item in sublist:
            if isinstance(item, Block):
                if item.activated:
                    item.set_rect(screen)
                    item.display(screen)
                    item.display_hp(screen)
    pygame.display.update()

    for sublist in blocks_list:
        for item in sublist:
            if isinstance(item, Block):
                if item.activated:
                    if item.if_die(screen):
                        print(REDCODE + "You lose!" + RESETCODE)
                        mouse_press()
                        sys.exit()

    continue

pygame.quit()
