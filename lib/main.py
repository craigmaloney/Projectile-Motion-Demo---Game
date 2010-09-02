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

    def update(self):
        if self.alive:
            rad_angle = math.radians(self.angle)
            # FIXME - Need to figure out how to get time into this formula for y
            #proj_y = ((pow(self.velocity, 2 )) * (pow(math.sin(rad_angle), 2))) / (2 * self.gravity)
            #print "projectile y: " + str(proj_y)
            (curr_x, curr_y) = self.pos
            self.t = self.t + 1
            tx = self.t/10.0
            proj_y = self.h0 + (tx * self.velocity * math.sin(rad_angle)) - (self.gravity * tx * tx)/2
            print "y: " + str(proj_y)
            size = ((proj_y / 20) + self.min_size)
            self.image = pygame.Surface((size,size))
            self.image.fill([255,255,0])
            proj_x = self.velocity * math.cos(rad_angle) * tx
            print "x: " + str(proj_x)
            self.pos = (curr_x, curr_y - proj_x / 20)
            self.rect.center = self.pos
            if proj_y < 0:
                self.alive = 0
                self.image.fill([0,0,0])

def game():

    screen = pygame.display.set_mode((1024, 768), DOUBLEBUF|HWSURFACE, 32)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Projectile Motion")
    background = pygame.image.load(data.filepath('images','background.png')).convert()

    tanks = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    all = pygame.sprite.OrderedUpdates()

    Tank.containers = all, tanks
    Projectile.containers = all, projectiles
    Tank.image = pygame.image.load(data.filepath('images', 'tank.png'))
    screen.blit(background,(0,0))
    pygame.display.flip()

    for i in range(100,900,100):
        Tank((i,700))
        Projectile((i,700),(i/10),40)
        Projectile((i,700),(i/10),50)
        Projectile((i,700),(i/10),60)
        Projectile((i,700),(i/10),70)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

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
