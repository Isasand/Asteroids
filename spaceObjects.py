# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 11:58:33 2017

@author: Isa
"""
from circle import Circle
import pygame
import random 
from point import Point 

from polygon import Polygon
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

class Alien(Polygon):
    
    def __init__(self):
        points = [ Point(10,10), Point(30,10), Point(50,10), Point(10,10), Point(20,2), 
                  Point(40,2), Point(50,10), Point(40,20), Point(30,20), Point(40,20), 
                  Point(37,30), Point(30,30), Point(23,30), Point(20,20), Point(30,20),
                  Point(20,20)]
        self.points = list(points)
        self.position = Point(200,200)
        self.rotation = 180
        self.pull = Point(0.02,0.02)
        self.angular_velocity = 0
        self.sound = pygame.mixer.Sound("AlienSound.wav")
        #self.accelerate(1)
        
    def appear(self):
        self.sound.play()