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
from circle import Circle

import pygame 

LIGHTBLUE = (0,255,255)
BLACK = (0,0,0)
myfont = 'Consolas'
RED = (204, 0, 0)
GREEN = (0, 255, 0)
pygame.init()

class Ship(Polygon):
    
    def __init__(self):
        points = [ Point(0,0), Point(-10,10), Point(15,0), Point(-10,-10) ]
        self.points = list(points)
        self.position = Point(50,250)
        self.rotation = 0
        self.pull = Point(0,0)
        self.angular_velocity = 0.0
        self.life = 5
        self.shield = Shield(self.rotation, self.pull, self.angular_velocity)
        self.shield_activated = False
        self.lifebar = "{}".format("♥") * self.life
        self.bullets = []

    def collide(self):
        if not self.shield_activated:
            self.life -= 1 
        else:
            if self.shield.health <= 0:
                self.shield_activated = False
                return
            self.shield.health -=50

    def show_lifebar(self,screen):
        lifebar=pygame.font.SysFont(myfont, 40, True).render(self.lifebar, 1, RED)
        screen.blit(lifebar,(5,10))
    
    def activate_shield(self):
        if self.shield.health == 200:
            self.shield_activated = True 
            self.shield.set_position(self.position)
        
class Shield(Circle):
    
    def __init__(self, rotation, pull, angular_velocity):
        self.timer = 0
        self.position = []
        self.rotation = rotation 
        self.pull = pull
        self.angular_velocity = angular_velocity
        self.life = 3
        self.health = 200 # max 200
        self.radius =30
        self.linewidth = 1
        self.timer = 0 
        
    def set_position(self, position):
        self.position = position
        
    def draw(self, screen):
        super().draw(screen)
        pos = (int(self.position.x), int(self.position.y) )
        pygame.draw.circle( screen, LIGHTBLUE, pos, self.radius, self.linewidth )