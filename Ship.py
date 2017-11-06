# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 12:41:23 2017

@author: Isa
"""
from polygon import Polygon
from point import Point
import pygame

pygame.mixer.init()

class Ship(Polygon):
    
    def __init__(self):
        points = [ Point(0,0), Point(-10,10), Point(15,0), Point(-10,-10) ]
        self.points = list(points)
        self.position = Point(50,250)
        self.rotation = 0
        self.pull = Point(0,0)
        self.angular_velocity = 0.0
        self.life = 5
        self.sound = pygame.mixer.Sound("shoot.wav")


    def collide(self):
        self.life -= 1 
        
    def shoot(self):
        self.sound.play()
        
