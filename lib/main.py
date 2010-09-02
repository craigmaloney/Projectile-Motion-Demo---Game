#!/usr/bin/env python
import pygame
from pygame.locals import *
from sys import exit
import os
import data
import math

class Tank(pygame.sprite.Sprite):
    def __init__(self, pos, angle = 0, velocity = 0):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect(center = pos)
        self.angle = angle
        self.velocity = velocity
    def update(self):
        pass

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, angle = 0, velocity = 0):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.min_size =10 
        self.image = pygame.Surface((self.min_size,self.min_size))
        self.image.fill([255,255,0])
        self.pos = pos
        self.rect = self.image.get_rect(center = pos)
        self.angle = angle
        self.velocity = velocity
        self.gravity = 9.8
        self.h0 = 0
        self.t = 0
        self.alive = 1
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
            self.image.fill([255,255,0])
            proj_x = self.velocity * math.cos(self.rad_angle) * tx
            if proj_y < 0:
                print "proj_x:" + str(proj_x)
                self.hit_ground()
            self.pos = (curr_x, (700 - ((proj_x * 20)) ))
            self.rect.center = self.pos
            self.t = self.t + 1

    def hit_ground(self):
        self.alive = 0
        self.image.fill([0,0,0])
     
class Grid(pygame.sprite.Sprite):
    def __init__(self):
        print "Hello"
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.Surface((700,750)).convert()
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect(topleft = (0,0))
        # Draw the smaller lines first
        for x in range(0,700,20):
            for y in range(0,700,20):
                pygame.draw.line(self.image, (0,0,220), (0,y), (700,y),1)
                pygame.draw.line(self.image, (0,0,220), (x,0), (x,700),1)
        # Now the larger lines
        for x in range(0,700,100):
            for y in range(0,700,100):
                pygame.draw.line(self.image, (0,0,0), (0,y), (700,y),3)
                pygame.draw.line(self.image, (0,0,0), (x,0), (x,700),3)

    def update(self):
        pass

def game():

    screen = pygame.display.set_mode((700,750), DOUBLEBUF|HWSURFACE, 32)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Projectile Motion")
    background = pygame.image.load(data.filepath('images','background.png')).convert()

    tanks = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    grid = pygame.sprite.Group()
    all = pygame.sprite.OrderedUpdates()

    Tank.containers = all, tanks
    Projectile.containers = all, projectiles
    Grid.containers = all, grid 
    Tank.image = pygame.image.load(data.filepath('images', 'tank.png'))
    screen.blit(background,(0,0))
    pygame.display.flip()
    Grid()

    for i in range(50,700,100):
        Tank((i,700))
        Projectile((i,700),((i+50)/10),5)
        Projectile((i,700),((i+50)/10),6)
        Projectile((i,700),((i+50)/10),7)
        Projectile((i,700),((i+50)/10),20)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        all.clear(screen,background)
        all.update()
        dirty = all.draw(screen)
        pygame.display.update(dirty)
        clock.tick(5)


def main():
    pygame.init()
    pygame.font.init()
    game()
    exit()

if __name__ == '__main__':
    main()
