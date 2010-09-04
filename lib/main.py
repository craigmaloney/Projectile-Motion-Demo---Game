#!/usr/bin/env python
import pygame
from pygame.locals import *
from sys import exit
import os
import data
import math

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 750

class Tank(pygame.sprite.Sprite):
    def __init__(self, pos, angle = 0, velocity = 0):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.pos = pos
        self.rect = self.image.get_rect(center = pos)
        self.angle = angle
        self.velocity = velocity
    def update(self):
        pass
    def move_left(self):
        (curr_x, curr_y) = self.pos
        curr_x = curr_x - 100
        if (curr_x <= 50):
            curr_x = 50
        self.pos = (curr_x, curr_y)
        self.rect = self.image.get_rect(center = self.pos)
    def move_right(self):
        (curr_x, curr_y) = self.pos
        curr_x = curr_x + 100
        if (curr_x >= 650):
            curr_x = 650
        self.pos = (curr_x, curr_y)
        self.rect = self.image.get_rect(center = self.pos)

    def fire(self):
        (curr_x, curr_y) = self.pos
        print curr_y
        Projectile(self.pos,self.angle,self.velocity)

    def gun_raise(self):
        self.angle = self.angle + 1
        if self.angle > 90:
            self.angle = 90

    def gun_lower(self):
        self.angle = self.angle - 1
        if self.angle < 0:
            self.angle = 0

    def velocity_increase(self):
        self.velocity = self.velocity + 1
        if self.velocity > 90:
            self.velocity = 90

    def velocity_decrease(self):
        self.velocity = self.velocity - 1
        if self.velocity < 0:
            self.velocity = 0

    def get_velocity(self):
        return self.velocity

    def get_angle(self):
        return self.angle
        

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, angle = 0, velocity = 0):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.min_size =10 
        self.image = pygame.Surface((self.min_size,self.min_size))
        self.color = [255,0,0]
        self.image.fill(self.color)
        self.pos = pos
        self.rect = self.image.get_rect(center = pos)
        self.angle = angle
        self.velocity = velocity
        self.gravity = 9.8
        self.h0 = 0
        self.t = 0
        self.alive = True
        self.bounce = False
        self.rad_angle = math.radians(self.angle)
        projected_y = ((pow(self.velocity, 2 )) * (pow(math.sin(self.rad_angle), 2))) / (2 * self.gravity)
        projected_time = ((self.velocity * math.sin(self.rad_angle)) / self.gravity)
        projected_x = (self.velocity * math.cos(self.rad_angle) * projected_time) * 2
        print "-----------------------------"
        print "Angle = " + str(self.angle)
        print "Velocity = " + str(self.velocity)
        print "y: " + str(projected_y)
        print "time: " + str(projected_time)
        print "x: " + str(projected_x)

    def update(self):
        if self.alive:
            # FIXME - Need to figure out how to get time into this formula for y
            #print "projectile y: " + str(proj_y)
            (curr_x, curr_y) = self.pos
            tx = self.t/10.0
            proj_y = self.h0 + (tx * self.velocity * math.sin(self.rad_angle)) - (self.gravity * tx * tx) / 2
            size = ((proj_y / 20) + self.min_size)
            self.image = pygame.Surface((size,size))
            self.image.fill(self.color)
            proj_x = self.velocity * math.cos(self.rad_angle) * tx
            if proj_y < 0:
                print "proj_x:" + str(proj_x)
                self.hit_ground()
            if (curr_y >= 500 and curr_y <= 600):
                if (proj_y < 10):
                    self.bounce = True 
                    print proj_y
            if (self.bounce == False):
                self.pos = (curr_x, (SCREEN_WIDTH - ((proj_x * 20)) + 20 ))
            else: 
                self.pos = (curr_x, (curr_y + (tx*10)))
            self.rect.center = self.pos
            self.t = self.t + 1

    def hit_ground(self):
        self.alive = False
        self.image.fill([0,0,0])
     
class Grid(pygame.sprite.Sprite):
    def __init__(self):
        print "Hello"
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT)).convert()
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect(topleft = (0,0))
        # Draw the smaller lines first
        for x in range(0,701,20):
            for y in range(0,701,20):
                pygame.draw.line(self.image, (0,0,220), (0,y), (SCREEN_WIDTH,y),1)
                pygame.draw.line(self.image, (0,0,220), (x,0), (x,SCREEN_WIDTH),1)
        # Now the larger lines
        for x in range(0,701,100):
            for y in range(0,701,100):
                pygame.draw.line(self.image, (0,0,0), (0,y), (SCREEN_WIDTH,y),3)
                pygame.draw.line(self.image, (0,0,0), (x,0), (x,SCREEN_WIDTH),3)

    def update(self):
        pass

class Notice (pygame.sprite.Sprite):
    def __init__(self,little_tank):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.tank = little_tank
        self.font = pygame.font.Font(data.filepath('fonts','LiberationMono-Regular.ttf'),24)
        self.image = pygame.Surface([200,26])
        self.angle = little_tank.get_angle()
        self.velocity = little_tank.get_velocity()
        self.rect = self.image.get_rect()
        self.text = 'Angle: ' + str(self.angle) + '   Velocity: ' + str(self.velocity) 
        self.image = self.font.render(self.text,1,(0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = ((350,720))

    def update(self):
        self.angle = self.tank.get_angle()
        self.velocity = self.tank.get_velocity()
        self.text = 'Angle: ' + str(self.angle) + '   Velocity: ' + str(self.velocity) 
        self.image = self.font.render(self.text,1,(0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = ((350,720))

def game():

    screen = pygame.display.set_mode((SCREEN_WIDTH,750), DOUBLEBUF|HWSURFACE, 32)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Projectile Motion")
    background = pygame.image.load(data.filepath('images','background.png')).convert()

    tanks = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    grid = pygame.sprite.Group()
    notice = pygame.sprite.Group()
    all = pygame.sprite.OrderedUpdates()

    Tank.containers = all, tanks
    Projectile.containers = all, projectiles
    Grid.containers = all, grid 
    Notice.containers = all, notice
    Tank.image = pygame.image.load(data.filepath('images', 'tank.png'))
    screen.blit(background,(0,0))
    pygame.display.flip()
    Grid()

    little_tank = Tank((SCREEN_WIDTH / 2,SCREEN_WIDTH),55,15)
    notices = Notice(little_tank)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                if event.key == K_LEFT:
                    little_tank.move_left()
                if event.key == K_RIGHT:
                    little_tank.move_right()
                if event.key == K_SPACE:
                    little_tank.fire()
                if event.key == K_UP:
                    little_tank.gun_raise()
                if event.key == K_DOWN:
                    little_tank.gun_lower()
                if event.key == K_EQUALS:
                    little_tank.velocity_increase()
                if event.key == K_MINUS:
                    little_tank.velocity_decrease()

        all.clear(screen,background)
        all.update()
        dirty = all.draw(screen)
        pygame.display.update(dirty)
        clock.tick(30)


def main():
    pygame.init()
    pygame.font.init()
    game()
    exit()

if __name__ == '__main__':
    main()
