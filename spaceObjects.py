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

from circle import Circle
import pygame
import random
import math
from point import Point


myfont = 'Consolas'
RED = (204, 0, 0)
GREEN = (0, 255, 0)

from polygon import Polygon


class Bullet(Circle):
    def __init__(self, position, rotation):
        self.position = position
        self.rotation = rotation
        self.pull = Point(0, 0)
        self.angular_velocity = 0
        self.radius = 3
        self.linewidth = 3
        self.accelerate(3)

    def draw(self, screen):
        super().draw(screen)
        pos = (int(self.position.x), int(self.position.y))
        pygame.draw.circle(screen, (255, 153, 255), pos, self.radius, self.linewidth)

    def draw_a(self, screen):
        super().draw(screen)
        pos = (int(self.position.x), int(self.position.y))
        pygame.draw.circle(screen, RED, pos, self.radius, self.linewidth)


class Star(Circle):
    def __init__(self):
        x = random.randint(1, 800)
        y = random.randint(1, 600)
        self.position = Point(x, y)
        self.rotation = 0
        self.pull = Point(0, 0)
        self.angular_velocity = 0
        self.radius = 2
        self.linewidth = 1
        self.accelerate(0)


class Alien(Polygon):
    def __init__(self, x, y):
        points = [Point(10, 10), Point(30, 10), Point(50, 10), Point(10, 10), Point(20, 2),
                  Point(40, 2), Point(50, 10), Point(40, 20), Point(30, 20), Point(40, 20),
                  Point(37, 30), Point(30, 30), Point(23, 30), Point(20, 20), Point(30, 20),
                  Point(20, 20)]
        self.points = list(points)
        self.position = Point(x, y)
        self.rotation = 180
        self.pull = Point(0, 0)
        self.angular_velocity = 0
        self.life = 3
        self.accelerate(0)
        self.lifebar = "{}".format("♥") * self.life
        self.bullets = []
        self.timer = 0
        self.timer_collide = 0

    def collide(self):
        self.life -= 1

    def calc_distance(self, p, q):
        return math.sqrt((p.x - q.x) ** 2 + (p.y - q.y) ** 2)

    def alien_in_game(self, ship, width, height, screen):
        self.ship = ship

        if self.life > 0:
            # if the ship and an alien bullet collides
            for bullet in self.bullets:
                if self.calc_distance(self.ship.position, bullet.position) < 10:
                    if self.ship.life > 0:
                        self.bullets.remove(bullet)
                        self.ship.collide()
                        self.ship.lifebar = self.ship.lifebar[:-1]
                        # if the alien and ship bullet collides
            for bullet in self.ship.bullets:
                if self.calc_distance(self.position, bullet.position) < 20:
                    if self.life > 0:
                        self.ship.bullets.remove(bullet)
                        self.collide()
                        self.lifebar = self.lifebar[:-1]

            self.alien_acceleration(self.pull.x)
            self.update(width, height)

            if self.shoot_ship(self.ship) < 30:
                if pygame.time.get_ticks() > self.timer:
                    self.timer= pygame.time.get_ticks() + 500
                    if len(self.bullets) >= 6:
                        self.bullets.remove(self.bullets[0])
                    self.bullets.append(Bullet(self.position, self.rotation + 90))
            
            if self.calc_distance(self.ship.position, self.position) < 10:
                if pygame.time.get_ticks() > self.timer_collide:
                    self.timer_collide = pygame.time.get_ticks() + 1000
                    if self.ship.life > 0:
                        self.ship.collide()
                        self.ship.lifebar = self.ship.lifebar[:-1]

                    if self.life > 0:
                        self.collide()
                        self.lifebar= self.lifebar[:-1]

        else:
            self.is_alien = False

    def calc_alien_acceleration(self):
        return self.position.x - self.ship.position.x

    def alien_acceleration(self, acc):
        if self.calc_alien_acceleration() < 0:
            if acc < 0:
                self.accelerate(0)
            self.accelerate(-0.003)
        else:
            if acc > 0:
                self.accelerate(0)
            self.accelerate(0.003)

    def show_lifebar(self, screen):
        lifebar = pygame.font.SysFont(myfont, 40, True).render(self.lifebar, 1,GREEN)
        screen.blit(lifebar, (670, 550))

    def shoot_ship(self, ship):
        shoot = self.position.x - ship.position.x
        if shoot < 0:
            shoot = shoot * (-1)
        return shoot
