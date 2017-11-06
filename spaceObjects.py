# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 11:58:33 2017

@author: Isa
"""
from circle import Circle
import pygame
import random 
from point import Point 

class Bullet(Circle):
    
    def __init__(self, position, rotation):
        self.position = position
        self.rotation = rotation
        self.pull = Point(0,0)
        self.angular_velocity = 0
        self.radius = 3
        self.linewidth = 3
        self.accelerate(2)
    
class Star(Circle):
    
     def __init__(self):
        x = random.randint(1,640)
        y= random.randint(1,480)
        self.position = Point(x,y)
        self.rotation = 0
        self.pull = Point(0,0)
        self.angular_velocity = 0
        self.radius = 2
        self.linewidth = 1
        self.accelerate(0)
    
    
#TODO add sprites 
class Sprites (pygame.sprite.Sprite):
    
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        
        self.rect = self.image.get.rect()