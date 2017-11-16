# -*- coding: utf-8 -*-
"""
Gruppuppgift: Asteroids - Objektorienterad Programmering
Nackademin IOT 17

Medverkande:
Isa Sand
Felix Edenborgh
Christopher Bryant

Stomme källkod:
Mark Dixon
"""
from polygon import Polygon
from point import Point


SMALL_ASTEROID = [Point(10,20), Point(12,12),Point(20,10), Point(28,12),Point(30,20), Point(28,30),Point(20,30)]
MEDIUM_ASTEROID = [Point(20,0), Point(30,0), Point(40,10), Point(50,10), Point(55, 20), Point(60,30),
                   Point(55,35), Point(50,37), Point(42, 36),Point(30, 36), Point(20,34), Point(20,32),
                   Point(10,30), Point(10,20)]
BIG_ASTEROID = [Point(40,0), Point(70,0), Point(80,30), Point(90,40), Point(70,80), Point(40,80),
                Point(30,60), Point(20,60), Point(10,40), Point(22,30), Point(20,20)]

class Astreoid(Polygon):
        def __init__(self,points, x, y, rotation, pull, angular_velocity, size):
            self.points = list(points)
            position = Point(x,y)
            self.position = position
            self.rotation = rotation
            self.pull = pull
            self.angular_velocity = angular_velocity
            self.size = size
             
        
        def set_size(self, size):
            self.size = size
        
        def get_size(self):
            return self.size 
        
        def explode(self):
            if self.size == "small":
                return True 
            elif self.size == "medium":
                self.set_size("small")
                self.points = SMALL_ASTEROID
               
                return False
            
            elif self.size == "big":
                self.set_size("medium")
                self.points = MEDIUM_ASTEROID
              
                return False