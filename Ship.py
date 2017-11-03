# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 12:41:23 2017

@author: Isa
"""
from polygon import Polygon
from point import Point
from circle import Circle
import random
import pygame

class Ship(Polygon):
    
    def __init__(self, sound):
        points=[ Point(0,0), Point(-10,10), Point(15,0), Point(-10,-10) ]
        self.points = list(points)
        position = Point(10,200)
        self.position = position
        self.rotation = 0
        self.pull = Point(0,0)
        self.angular_velocity = 0.0
        self.life = 5
        self.sound = sound


    def collide(self):
        self.life -= 1 
        
    def shoot(self):
        self.sound.play()
    #def shoot

class Bullet(Circle):
    
    def __init__(self, position, rotation):
        self.position = position
        self.rotation = rotation
        self.pull = Point(0,0)
        self.angular_velocity = 0
        self.radius = 3
        self.linewidth = 3
        self.accelerate(1)
    
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