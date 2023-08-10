import numpy as np
import pygame
from random import randint

class Ball:
    _color = (196,217,255)
    next_x = None
    next_y = None
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.last_x = self.x
        self.last_y = self.y
        self.radius = 0.017 # This number represents a ratio of the WIDTH of the screen.
        self.angle = None
        self.inter_y = None
        self.up = True
        self.rect = None
        self.activated = False

    # Calculates in radians
    def set_angle(self, x, y):
        if y > self.y:
            y = self.y - 1
        dx = x- self.x
        dy = self.y - y
        self.angle = np.arctan2(dy, dx)

    def set_inter_y(self):
        self.inter_y = self.y - -1*np.tan(self.angle) * self.x

    def update_rect(self, screen):
        screen_width = screen.get_size()[0]
        radius  = int(self.radius * screen_width)
        self.rect = pygame.Rect(self.x - radius, self.y -radius, radius*2, radius*2)

# Moves the ball
    def move(self, dist):
        dx_ = dist * np.cos(self.angle)
        dy_ = dist * np.sin(self.angle)

        new_x = self.x + dx_
        if self.up:
            new_x = self.x + dx_
            new_y = self.y - dy_
        else:
            new_x = self.x - dx_
            new_y = self.y + dy_
        self.x = new_x
        self.y = new_y

    # If the ball is about to pass a wall, and go outside the map, this function will snap it back to the wall.
    # If the ball is touching one of the boundaries, it will change the angle of the ball. If the ball is touching the bottom boundary, it will delete it at the end.
    def check_wall(self, screen):
        screen_width = screen.get_size()[0]
        screen_height = screen.get_size()[1]
        radius = int(self.radius * screen_width)

        # Left
        if self.x-radius < 0:
            self.x = int(radius)
            self.y = int(-np.tan(self.angle) * self.x + self.inter_y)
        if self.x-radius == 0:
            self.bounce()

        # Right
        if self.x+radius > screen_width:
            self.x = int(screen_width - radius)
            self.y = int(-np.tan(self.angle) * self.x + self.inter_y)
        if self.x+radius == screen_width:
            self.bounce()

        # Top
        if self.y-radius < 0 :
            self.y = int(radius)
            self.x = int((self.y - self.inter_y)/-np.tan(self.angle))
        if self.y-radius == 0:
            self.up = False
            self.bounce()


        # Bottom
        if int(self.y+radius) > screen_height:
            self.y = int(screen_height - radius)
            self.x = int((self.y - self.inter_y)/-np.tan(self.angle))
        if int(self.y+radius) == screen_height:
            if Ball.next_x is None and Ball.next_y is None:
                Ball.next_x = self.x
                Ball.next_y = self.y
            else:
                self.x = Ball.next_x
                self.y = Ball.next_y
            self.activated = False
            return True


    # Renders the ball on the screen
    def display(self, screen):
        screen_width = screen.get_size()[0]
        pygame.draw.circle(screen, Ball._color, (self.x, self.y), self.radius*screen_width)

    def erase(self, screen):
        screen_width = screen.get_size()[0]
        radius  = int(self.radius * screen_width)
        last_rect = pygame.Rect(self.last_x-radius, self.last_y-radius, radius*2, radius*2)
        surface = screen.subsurface(last_rect)
        for x in range(last_rect.left, last_rect.left + last_rect.width):
            for y in range(last_rect.top, last_rect.top + last_rect.height):
                pixel_color = surface.get_at((x - last_rect.left, y - last_rect.top))
                if pixel_color == Ball._color:
                    surface.set_at((x - last_rect.left, y - last_rect.top), (0, 0, 0))

# Changes the angle by multiplying it by -1, and the y intercept by updating it
    def bounce(self):
        if self.up:
            self.angle = np.pi - self.angle
            self.inter_y = self.y - -np.tan(self.angle) * self.x
        else:
            self.angle = np.pi - self.angle
            self.inter_y = self.y - -np.tan(self.angle) * self.x

class Block:
    colors = ((128, 238, 255),(224, 129, 252),(132, 247, 109),(247, 247, 15),(245, 167, 22),(247, 15, 228),(15, 130, 0), (118, 145, 245), (252, 3, 36), (143, 143, 143), (255, 150, 59))
    length = 0.1 #The number 0.1 represents a 0.1 of the screen WIDTH.
    def __init__(self, x, y):
        self.x = x 
        self.y = y 
        self.hp = None 
        self.color = None 
        self.rect = None
        self.activated = True


    def set_rect(self, screen):
        screen_width = screen.get_size()[0]
        self.rect = pygame.Rect(self.x, self.y, Block.length*screen_width, Block.length*screen_width)

# Moves the block 1 row down
    def move(self, screen):
        screen_width = screen.get_size()[0]
        self.y = self.y + Block.length * screen_width

# Renders the block (without the HP value) on the screen
    def display(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, width=6)

    def erase(self, screen):
        screen.fill((0,0,0), self.rect)

# Sets the HP value depends on what row it is.
    def set_hp(self, screen):
        screen_width = screen.get_size()[0]
        screen_height = screen.get_size()[1]
        count = 0
        min_num = 0
        max_num = 10

        for num in range(screen_height, -1, int(-Block.length*screen_width)):
            count += 1
            if num <= self.y:
                min_num += (count+1)*6
                max_num += (count+1)*6
                break
        max_num = randint(max_num-10, max_num+5)
        self.hp = randint(min_num, max_num)

# Renders the HP value on the screen (in the middle of the block)    
    def display_hp(self, screen):
        font = pygame.font.SysFont('arial', 20)
        text = font.render(str(self.hp), True, (255, 255, 255))
        if len(str(self.hp)) == 1:
            screen.blit(text, (self.x + 19, self.y + 15))
        elif len(str(self.hp)) == 2:
            screen.blit(text, (self.x + 13, self.y + 15))
        else:
            screen.blit(text, (self.x + 7, self.y + 15))


    # Updates the color value of the blocks depends on its HP value.
    def update_color(self):
        for i in range(0, 15*len(Block.colors), 15):
            if self.hp <= i:
                self.color = Block.colors[i//15]
                break
        else:
            self.color = Block.colors[-1]
            
# Checks if the block is touching the floor or if its HP value is 0. If one of the options happens, the block
# delete itself. If the block touched the floor, it will return True, that will mark the end of the game
    def if_die(self, screen):
        screen_height = screen.get_size()[1]
        screen_width = screen.get_size()[0]
        length = screen_width*Block.length
        if np.ceil(self.y + length) >= screen_height:
            screen.fill((0,0,0), self.rect)
            self.activated = False
            return True

        if self.hp < 1:
            screen.fill((0,0,0), self.rect)
            self.activated = False
        return False

    def damage(self):
        self.hp -= 1



####################################################################################################################################################################################
# Waits until the next mouse left click press, and after that it returns the position of the mouse on the screen.
def mouse_press():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                return pos
            elif event.type == pygame.QUIT:
                running = False

def check2(ball, block, screen):
    screen_width = screen.get_size()[0]
    screen_height = screen.get_size()[1]
    radius = int(ball.radius * screen_width)
    block_len = Block.length * screen_width

    if block.rect.colliderect(ball.rect):
        if block.y <= ball.y <= block.y + block_len:
            # Right
            if ball.x >= block.x + block_len:

                ball.x = int(block.x + block_len + radius)
                ball.y = int(-np.tan(ball.angle) * ball.x + ball.inter_y)
            if ball.x - radius == int(block.x + block_len):
                ball.bounce()
                block.damage()
                block.erase(screen)
                block.update_color()
                block.display(screen)
                block.display_hp(screen)

            # Left
            if ball.x <= block.x:

                ball.x = int(block.x - radius)
                ball.y = int(-np.tan(ball.angle) * ball.x + ball.inter_y)
            if ball.x + radius == int(block.x):
                ball.bounce()
                block.damage()
                block.erase(screen)
                block.update_color()
                block.display(screen)
                block.display_hp(screen)

        if block.x <= ball.x <= block.x + block_len:
            # Bottom
            if ball.y >= block.y + block_len:

                ball.y = int(block.y + block_len + radius)
                ball.x = int((ball.y - ball.inter_y) / -np.tan(ball.angle))
            if ball.y - radius == int(block.y + block_len):
                ball.up = False
                ball.bounce()
                block.damage()
                block.erase(screen)
                block.update_color()
                block.display(screen)
                block.display_hp(screen)


            # Top
            if ball.y <= block.y:

                ball.y = int(block.y - radius)
                ball.x = int((ball.y - ball.inter_y) / -np.tan(ball.angle))
            if ball.y + radius == int(block.y):
                ball.up = True
                ball.bounce()
                block.damage()
                block.erase(screen)
                block.update_color()
                block.display(screen)
                block.display_hp(screen)
