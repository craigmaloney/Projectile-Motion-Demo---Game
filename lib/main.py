#!/usr/bin/env python
import pygame
from pygame.locals import *
from sys import exit

def game():

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()


def main():
    pygame.init()
    screen = pygame.display.set_mode((1024, 768), DOUBLEBUF|HWSURFACE, 32)
    pygame.display.set_caption("Projectile Motion")
    game()
    exit()

if __name__ == '__main__':
    main()
