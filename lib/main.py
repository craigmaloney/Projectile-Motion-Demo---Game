#!/usr/bin/env python
import pygame
from pygame.locals import *
from sys import exit
import os
import data
import math
import random

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 750

class Tank(pygame.sprite.Sprite):
    def __init__(self, pos, angle = 0, velocity = 0):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.pos = pos
        self.rect = self.image.get_rect(center = pos)
        self.angle = angle
        self.velocity = velocity
        self.position_x = 18

    def update(self):
        pass

    def move_left(self):
        self.position_x = self.position_x - 1
        (curr_x, curr_y) = self.pos
        curr_x = curr_x - 20
        if (curr_x <= 10):
            curr_x = 10
        if (self.position_x < 1):
            self.position_x = 1
        self.pos = (curr_x, curr_y)
        self.rect = self.image.get_rect(center = self.pos)

    def move_right(self):
        self.position_x = self.position_x + 1
        (curr_x, curr_y) = self.pos
        curr_x = curr_x + 20
        if (curr_x >= 690):
            curr_x = 690
        if (self.position_x > 35):
            self.position_x = 35
        self.pos = (curr_x, curr_y)
        self.rect = self.image.get_rect(center = self.pos)

    def fire(self):
        (curr_x, curr_y) = self.pos
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

    def get_position(self):
        return self.position_x
        

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, angle = 0, velocity = 0):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.min_size = 10 
        self.image = pygame.Surface((self.min_size,self.min_size))
        self.color = [255,0,0]
        self.image.fill(self.color)
        self.pos = pos
        self.rect = self.image.get_rect(center = pos)
        self.angle = angle
        self.velocity = velocity
        self.gravity = 9.8
        self.h0 = 0
        self.t = 1
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
            (curr_x, curr_y) = self.pos
            tx = self.t/50.0
            proj_y = self.h0 + (tx * self.velocity * math.sin(self.rad_angle)) - (self.gravity * tx * tx) / 2
            size = ((proj_y / 2) + self.min_size)
            self.image = pygame.Surface((size,size))
            self.image.fill(self.color)
            proj_x = self.velocity * math.cos(self.rad_angle) * tx
            #print "proj_x:" + str(proj_x)
            if proj_y < 0:
                self.hit_ground()
            if (proj_x > 11 and proj_x < 12):
                if (proj_y < 10):
                    self.bounce = True 
                    print "proj_y: " + str(proj_y)
            if (self.bounce == False):
                self.pos = (curr_x, (SCREEN_WIDTH - ((proj_x * 20)) + 20))
            else: 
                self.pos = (curr_x,curr_y)
            self.rect.center = self.pos
            self.t = self.t + 1

    def hit_ground(self):
        # position on the grid so the explosion doesn't span 5 grid points
        (curr_x, curr_y) = self.rect.center
        curr_x = curr_x - (curr_x % 10)
        curr_y = curr_y - (curr_y % 10)

        self.alive = False
        x_list = (curr_x - 20, curr_x, curr_x + 20)
        y_list = (curr_y - 20, curr_y, curr_y + 20)
        for x in (x_list):
            for y in (y_list):
                Explosion((x,y))
        self.image.fill([0,0,0])
     
class Grid(pygame.sprite.Sprite):
    def __init__(self):
        print "Hello"
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.Surface([SCREEN_WIDTH,SCREEN_HEIGHT],SRCALPHA)
        self.image.fill([255,255,255])
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

class Wall (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.Surface((SCREEN_WIDTH,20))
        self.image.fill([106,75,00])
        self.rect = self.image.get_rect(topleft = (0,480))

    def update(self):
        pass

class Explosion (pygame.sprite.Sprite):
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.pos = pos
        self.image = pygame.Surface((20,20),SRCALPHA).convert()
        self.image.fill([255,255,0])
        self.rect = self.image.get_rect()
        self.rect.center = (self.pos)
        self.dissipate = 255
    def update(self):
        self.rect.center = (self.pos)
        self.image.fill([255,random.randint(0,255),random.randint(0,255)])
        self.image.set_alpha(self.dissipate)
        self.dissipate = self.dissipate - 10
        if (self.dissipate < 0):
            self.kill()

class Enemy (pygame.sprite.Sprite):
    def __init__(self,coordinates):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.coordinates = coordinates
        offset = 10
        (coordinate_x, coordinate_y) = self.coordinates
        self.pos = ((coordinate_x * 20 - offset), (700 - (coordinate_y * 20)) + offset)
        self.image = pygame.Surface((20,20),SRCALPHA).convert()
        self.image.fill([255,0,0])
        self.rect = self.image.get_rect()
        self.rect.center = (self.pos)
        self.alpha = 50
        self.image.set_alpha(self.alpha)
        self.hit = False
    def update(self):
        if (self.hit):
            if (self.alpha <= 255):
                self.alpha = self.alpha + 5
                self.image.set_alpha(self.alpha)

    def collide(self):
        self.hit = True



class Notice (pygame.sprite.Sprite):
    def __init__(self,little_tank):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.tank = little_tank
        self.font = pygame.font.Font(data.filepath('fonts','LiberationMono-Regular.ttf'),24)
        self.image = pygame.Surface([200,26])
        self.angle = little_tank.get_angle()
        self.velocity = little_tank.get_velocity()
        self.position = little_tank.get_position()
        self.rect = self.image.get_rect()
        self.text = 'Position: ' + str(self.position) + '   Angle: ' + str(self.angle) + '   Velocity: ' + str(self.velocity) 
        self.image = self.font.render(self.text,1,(0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = ((350,720))

    def update(self):
        self.angle = self.tank.get_angle()
        self.velocity = self.tank.get_velocity()
        self.position = self.tank.get_position()
        self.image = self.font.render(self.text,1,(0,0,0))
        self.text = 'Position: ' + str(self.position) + '   Angle: ' + str(self.angle) + '   Velocity: ' + str(self.velocity) 
        self.rect = self.image.get_rect()
        self.rect.center = ((350,720))

def game():

    screen = pygame.display.set_mode((SCREEN_WIDTH,750))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Projectile Motion")
    background = pygame.image.load(data.filepath('images','background.png')).convert()

    enemy_list = []
    enemy_list.extend([(26,20), (27,20), (28,20)])
    enemy_list.extend([(5,15),(5,16)])
    enemy_list.extend([(18,16),(18,17)])
    enemy_list.extend([(9,26),(10,26),(11,26)])
    enemy_list.extend([(30,30),(31,30),(32,30),(33,30)])


    tanks = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    grid = pygame.sprite.Group()
    notice = pygame.sprite.Group()
    wall = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    all = pygame.sprite.OrderedUpdates()

    Tank.containers = all, tanks
    Projectile.containers = all, projectiles
    Grid.containers = all, grid 
    Notice.containers = all, notice
    Wall.containers = all, wall
    Explosion.containers = all, explosions
    Enemy.containers = all, enemies
    Tank.image = pygame.image.load(data.filepath('images', 'tank.png'))
    screen.blit(background,(0,0))
    pygame.display.flip()
    Grid()
    Wall()


    little_tank = Tank((SCREEN_WIDTH / 2,SCREEN_WIDTH),55,15)
    notices = Notice(little_tank)

    for i in (enemy_list):
        Enemy(i)

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

        for enemy in (pygame.sprite.groupcollide(enemies,explosions,False,False)):
            enemy.collide()

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
