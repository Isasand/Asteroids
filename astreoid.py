# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 15:06:28 2017

@author: Isa
"""
from polygon import Polygon
from point import Point
import pygame 
pygame.mixer.init()

class Astreoid(Polygon):
        def __init__(self,points, x, y, rotation, pull, angular_velocity, size):
            self.points = list(points)
            position = Point(x,y)
            self.position = position
            self.rotation = rotation
            self.pull = pull
            self.angular_velocity = angular_velocity# 0.2
            self.size = size
            self.sound = pygame.mixer.Sound("explosion.wav")
            #self.accelerate(0.9)
        
        def explode(self):
            self.sound.play()
            if self.size == "small":
                return True 
            elif self.size == "medium":
                self.size = "small"
                self.points = [ Point(10,20), Point(20,10), Point(30,20), Point(20,30) ]
         
                return False
            elif self.size == "big":
                self.size = "medium"
                self.points = [ Point(10,30), Point(30,10), Point(40,30), Point(30,40) ]
              
                return False
       