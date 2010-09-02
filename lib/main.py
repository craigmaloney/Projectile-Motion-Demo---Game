#!/usr/bin/env python
import pygame
from pygame.locals import *
from sys import exit
import os
import data

class Tank(pygame.sprite.Sprite):
    def __init__(self, pos, angle = 0, velocity = 0):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect(center = pos)
        self.angle = angle
        self.velocity = velocity

def game():

    while True:

        tanks = pygame.sprite.Group()
        all = pygame.sprite.OrderedUpdates()

        Tank.containers = all, tanks
        Tank.image = pygame.image.load(data.filepath('images', 'tank.png'))

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        Tank((300,200))
        all.clear(screen,background)
        all.update()
        dirty = all.draw(screen)
        pygame.display.update(dirty)
        clock.tick(30)


def main():
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1024, 768), DOUBLEBUF|HWSURFACE, 32)
    pygame.display.set_caption("Projectile Motion")
    game()
    exit()

if __name__ == '__main__':
    main()
