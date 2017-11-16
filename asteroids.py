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

import sys
import random
import pygame,pygame.font, pygame.event, pygame.draw
from pygame.locals import *

import math
from game import Game
from Ship import Ship
from spaceObjects import Bullet
from astreoid import Astreoid
from astreoid import SMALL_ASTEROID, MEDIUM_ASTEROID, BIG_ASTEROID

from point import Point
from spaceObjects import Star
from spaceObjects import Alien
from button import Button
from Highscore import Highscoreboard 

#variable for testing 
#highscore starts with one life and highscore
#gameover starts with 0 lifes
#lastlevel starts at last level 
#testvictory starts at 5th level with 0 asteroids (winning state)
TEST_HIGHSCORE = False
TEST_GAMEOVER = False
TEST_LASTLEVEL = False
TEST_VICTORY = False

pygame.mixer.init()
pygame.init()
 
HEIGHT = 600
WIDTH = 800
#some colors to use
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (204,0,0)
YELLOW = (255,255,51)
ORANGE = (225, 158, 0)
LIGHTBLUE = (0,255,255)
LIFEBARBLUE = (0,102,102)
GREEN = (0,255,0)


#load sounds
shoot_sound = pygame.mixer.Sound("shoot.wav")
pygame.mixer.music.load("gameplay.wav")

myfont = 'Consolas'
welcome_text=pygame.font.SysFont(myfont, 40).render('Welcome', 1, WHITE)
welcome_text_two=pygame.font.SysFont(myfont, 40).render('To Asteroids', 1, WHITE)

pause_text = pygame.font.SysFont(myfont, 32).render('Paused', 1, WHITE)
return_text = pygame.font.SysFont(myfont, 32).render('Press R to return to menu', 1, WHITE)
start_text = pygame.font.SysFont(myfont, 32).render('or SPACE to continue', 1, WHITE)
victory_text= pygame.font.SysFont(myfont, 100).render("WINNER", 1, WHITE)

next_level_text = pygame.font.SysFont(myfont, 32).render('You made it to the next level!', 1, WHITE)
continue_text = pygame.font.SysFont(myfont, 32).render('Press C to continue', 1, WHITE)
respawn = pygame.font.SysFont(myfont, 32).render('Press R to Respawn', 1, WHITE)

#buttons for start menu
start_button = Button((290, 190, 170,50), 'START',BLACK, WHITE)
highscore_button  = Button((300, 245, 150,40), 'HIGHSCORE', BLACK, WHITE)
help_button  = Button((300, 290, 150,40), 'HELP', BLACK, WHITE)
options_button = Button((300, 335, 150, 40), 'OPTIONS',BLACK, WHITE)
quit_button = Button((300, 380, 150, 40), 'QUIT', BLACK, WHITE)

class Asteroids( Game ):
    """
    Asteroids extends the base class Game to provide logic for the specifics of the game
    """
    def __init__(self, name, width, height):
        super().__init__( name, width, height )
        self.ship = Ship()
        self.asteroids= []
        self.stars=[]
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.max_num_asteroids = 5
        self.current_level = 1
        self.new_level = True
        self.timer = 0
        self.state = "startmenu"
        self.background_image = self.image_handle()
        self.buttons = []
        self.highscore = Highscoreboard()
        self.newhighscore = False
        self.score = 0
        self.timer_ship_alien_collide = 0
        self.is_alien = False
        self.alien = Alien(self.ship.position.x+300, HEIGHT-40)
        self.sound = True
        self.testing()
        
    def testing(self):
        if TEST_LASTLEVEL:
            self.current_level = 5 
            self.check_max_asteroids()
        if TEST_HIGHSCORE:
            self.score = (self.highscore.get_min_score()+10)
            self.ship.life = 1
            self.ship.lifebar= "{}".format("♥")*self.ship.life
        if TEST_GAMEOVER:
            self.ship.life = 0
            self.ship.lifebar= "{}".format("♥")*self.ship.life
        if TEST_VICTORY:
            self.current_level = 5
            self.max_num_asteroids = 0 
            
        
    def image_handle(self):
        if self.state == "startmenu" :
            return pygame.image.load("menu.jpg").convert()
        if self.state == "gameover":
            return pygame.image.load("gameover.png").convert()
        if self.state == "menuoption":
            return pygame.image.load("help.jpg").convert()
        if self.state == "victory":
            return pygame.image.load("victory.jpg").convert()
        else:
            return False
        
    def handle_input(self):
        super().handle_input()
        keys_pressed = pygame.key.get_pressed()
        if self.state == "playing":
            if keys_pressed[K_s]:
                self.ship.activate_shield()
            if keys_pressed[K_p]:
                self.state = "paused" 
            if keys_pressed[K_SPACE]:
                if pygame.time.get_ticks() > self.timer:
                    pygame.mixer.Channel(1).play(shoot_sound)
                    self.timer = pygame.time.get_ticks() + 300
                    if len(self.ship.bullets)>=5:
                        self.ship.bullets.clear()
                    self.ship.bullets.append(Bullet(self.ship.position, self.ship.rotation))
            if keys_pressed[K_LEFT] and self.ship:
                self.ship.rotate(-0.6)
                if self.ship.shield_activated:
                    self.ship.shield.rotate(-0.6)
            if keys_pressed[K_RIGHT] and self.ship:
                self.ship.rotate(0.6)
                if self.ship.shield_activated:
                    self.ship.shield.rotate(0.6)
            if keys_pressed[K_UP] and self.ship:
                self.ship.accelerate(0.003)
                if self.ship.shield_activated:
                    self.ship.shield.accelerate(0.003)
            if keys_pressed[K_DOWN] and self.ship:
                self.ship.accelerate(0)
                if self.ship.shield_activated:
                    self.ship.shield.accelerate(0)
            
        if keys_pressed[K_r] and self.state in {"playing", "gameover"}:  
            self.restart_game()
                
        if self.state == "paused":
            if keys_pressed[K_SPACE]:
                self.state = "playing"
            if keys_pressed[K_r]:
                pygame.mixer.music.stop()
                self.state = "startmenu"
        
        if keys_pressed[K_RETURN] and self.state == "menuoption":
            pygame.mixer.music.stop()
            self.state = "startmenu"
        
        if self.state == "middlescreen":
            if keys_pressed[K_c]:
                self.new_level = True
                self.current_level += 1
                self.check_max_asteroids()
                self.state  = "playing"
        
    def restart_game(self):
        self.ship.life = 5
        self.ship.lifebar = "{}".format("♥") * self.ship.life
        self.max_num_asteroids = 5
        self.score = 0
        self.current_level = 1
        self.new_level = True
        self.is_alien = False
        self.state = "playing"
        self.newhighscore = False
        
    def calc_distance(self,p, q):
        return math.sqrt((p.x-q.x)**2 + (p.y-q.y)**2)
    
    def collision_handle(self):
        transform_asteroid = False
        #if you shoot
        if len(self.ship.bullets)>0:
            for bullet in self.ship.bullets:
                for asteroid in self.asteroids:
                    if (self.calc_distance(bullet.position, asteroid.position)<70 and asteroid.size == "big") or (self.calc_distance(bullet.position, asteroid.position)<30):
                        if asteroid.explode():
                            self.asteroids.remove(asteroid)
                            self.score += 10
                        else:
                            transform_asteroid = True                           
                            newsize = asteroid.get_size()
                            position= asteroid.position
                            self.asteroids.remove(asteroid)
                            self.score +=5
                            
                        if bullet in self.ship.bullets:
                            self.ship.bullets.remove(bullet)
        
        if transform_asteroid:
            self.asteroids.extend((self.CreateAsteroid(position, newsize), self.CreateAsteroid(position, newsize)))
                
        #if the ship and an astreoid collides
        if len(self.asteroids)>0 and self.ship.life >0:
            for asteroid in self.asteroids:
                if self.calc_distance(self.ship.position,asteroid.position)<70 and asteroid.size == "big" or self.calc_distance(self.ship.position, asteroid.position)<30:
                    asteroid.explode()
                    self.asteroids.remove(asteroid)
                    self.ship.collide()
                    if not self.ship.shield_activated:
                        self.ship.lifebar = self.ship.lifebar[:-1]
    
    def CreateAsteroid(self, pos, size):
        if pos == "random" :
            x = random.randint(0,600)
            y = random.randint(0,430)
            
            while self.calc_distance(Point(x,y), self.ship.position)<80:
                x = random.randint(0,600)
                y = random.randint(0,430)
        else:
            x = pos.x
            y = pos.y
       
        rotation=random.randint(0,5)
        point_x = random.uniform(-0.001,0.5)
        point_y = random.uniform(-0.001,0.5)
        angular_velocity = random.uniform(0.1, 0.8)
        
        if size == "medium":
            points= MEDIUM_ASTEROID 
        elif size == "small":
            points= SMALL_ASTEROID
        else:
            points= BIG_ASTEROID
            
        return Astreoid(points, x, y, rotation,Point(point_x, point_y), angular_velocity,size)
                                        
    def spawn_asteroids(self):
        sizes = ["small", "medium", "big"]
        
        if self.new_level:
            self.asteroids.clear()
            for i in range(0,self.max_num_asteroids):
                size = sizes[random.randint(0,2)]
                self.asteroids.append(self.CreateAsteroid("random", size))
                self.new_level = False
                    
    def show_lifebar(self):
        self.ship.show_lifebar(self.screen)
        if self.is_alien:
           self.alien.show_lifebar(self.screen)
             
    def shield_bar(self):
        pygame.draw.rect(self.screen, (LIFEBARBLUE), (10,50,self.ship.shield.health,20), 0)
        
        if not self.ship.shield_activated:
            if pygame.time.get_ticks() > self.ship.shield.timer and not self.ship.shield.health == 200:
                self.ship.shield.timer = pygame.time.get_ticks() + 190
                pygame.draw.rect(self.screen, (0,102,102), (10,50,self.ship.shield.health,20), 0)
                self.ship.shield.health+=5
                
        pygame.draw.rect(self.screen, (WHITE),(8,48,204,24), 1)
        
    def death_handler(self):
        self.highscorecheck()
        name = ""
        output = "INPUT YOUR INITIALS"
        if self.newhighscore == False:
            self.background_image = self.image_handle()
            self.screen.blit(self.background_image, [0, 0])
            self.screen.blit(respawn,(250,100))
        else:
            pygame.mixer.music.stop()
            # while not self.highscore.right_lenght_string(name):
            name=self.highscore.ask_for_input(self.screen, output)
            # output = "MUST BE 3 LETTERS OR CHARACTERS"
            self.highscore.newname = name.upper()
            self.highscore.newscore = self.score
            self.highscore.update_board()
            self.highscore.printboard(self.screen)
            self.state = "menuoption"
        
    def check_max_asteroids(self):
        if self.current_level == 1:
            self.max_num_asteroids = 5
        elif self.current_level == 2:
            self.max_num_asteroids = 10
        elif self.current_level == 3:
            self.max_num_asteroids = 15
        elif self.current_level == 4:
            self.max_num_asteroids = 20
        elif self.current_level == 5:
            self.max_num_asteroids = 20
            self.is_alien = True
    
    def highscorecheck(self):
        if self.score > self.highscore.get_min_score():
            self.newhighscore = True      
        
    def next_level_check(self):
        if len(self.asteroids) ==0 and not self.state == "gameover":
            if self.current_level == 5:
                self.state = "victory"
                pygame.display.flip()
                self.screen.blit(self.image_handle(), [0,0])
                self.screen.blit(victory_text,(230,200))
            else:
                self.state = "middlescreen"
                self.screen.fill(BLACK)
                self.screen.blit(next_level_text,(120,200))
                self.screen.blit(continue_text,(120,240))
            
    def spawn_stars(self):
        if self.new_level:
            self.stars.clear()
        if len(self.stars)<100 and not self.ship.life ==0:
            self.stars.append(Star())
    
    def print_score_and_level(self):
         score_text=pygame.font.SysFont(myfont, 20).render("Score:" + str(self.score), 1, WHITE)
         stage_text=pygame.font.SysFont(myfont, 20).render("Stage:" + str(self.current_level), 1, WHITE)
         self.screen.blit(score_text,(700,10))
         self.screen.blit(stage_text, (700, 25))
      
    def start_menu(self):
        self.screen.fill(BLACK)
        self.background_image = self.image_handle()
        self.screen.blit(self.background_image, [0, 0])
        self.screen.blit(welcome_text,(300,70))
        self.screen.blit(welcome_text_two, (240,120))
        self.buttons.extend((start_button, options_button, quit_button, help_button, highscore_button))
        for b in self.buttons:
            b.draw(self.screen)

    
    def paused(self):
        self.screen.blit(return_text,(180,200))
        self.screen.blit(start_text,(215,240))
        self.screen.blit(pause_text,(335,100))
        
    def bhelp(self):
        self.background_image = self.image_handle()
        self.screen.blit(self.background_image, [0,0])
                
    def runGame(self):
        super().runGame()
                     
    def life_check(self):
        if self.ship.life == 0:
            self.state = "gameover"
            
    def update_simulation(self):
        """
        update_simulation() causes all objects in the game to update themselves
        """
        super().update_simulation()
        if self.ship:
            self.ship.update( self.width, self.height )
            if self.ship.shield_activated:
                self.ship.shield.update(self.width,self.height)
        for asteroid in self.asteroids:
            asteroid.update( self.width, self.height )
        for star in self.stars:
            star.update( self.width, self.height )
        for bullets in self.ship.bullets:
            bullets.update( self.width, self.height)
        if self.is_alien:
            self.alien.alien_in_game(self.ship,self.width,self.height,self.screen)
            for bullets in self.alien.bullets:
                bullets.update(self.width, self.height)
            if self.alien.life == 0:
                self.is_alien = False
       
    def handle_state(self):
        if self.state == "gameover":
            self.death_handler()
        if self.state == "playing":
            
            self.screen.fill(BLACK)
            self.life_check()
            self.spawn_stars()
            self.spawn_asteroids()
            self.collision_handle()
            self.next_level_check()
            self.print_score_and_level()
            self.show_lifebar()
            
        if self.state == "paused":
            self.paused()
        elif self.state == "startmenu":
            self.start_menu()
        for event in pygame.event.get():
            for button in self.buttons:
                if 'click' in button.handleEvent(event):
                    if button._propGetCaption() == "QUIT":
                        self.running= False
                    if button._propGetCaption() == "START":
                        if self.sound:
                            pygame.mixer.music.play(-1)
                        self.state = "playing"
                    if button._propGetCaption() == "OPTIONS":
                        self.state = "menuoption"
                    if button._propGetCaption() == "HELP":
                        self.state = "menuoption"
                        self.bhelp()
                    if button._propGetCaption() == "HIGHSCORE":
                        self.state = "menuoption"
                        self.highscore.printboard(self.screen)
                        
    def render_objects(self):
        """
        render_objects() causes all objects in the game to draw themselves onto the screen
        """
        super().render_objects()
        # Render the ship:
        if self.state == "playing":
            if self.ship.shield_activated:
                self.ship.shield.draw(self.screen)
            self.ship.draw( self.screen )
            self.shield_bar()
            # Render all the stars, if any:
            for star in self.stars:
                star.draw( self.screen )
                # Render all the asteroids, if any:
            for asteroid in self.asteroids:
                asteroid.draw( self.screen )
                # Render all the bullet, if any:
            for bullet in self.ship.bullets:
                bullet.draw( self.screen )
            if self.is_alien:
                self.alien.draw(self.screen)
                for bullet in self.alien.bullets:
                    bullet.draw_a(self.screen)
                    if bullet.position.x >= self.width - 5 or bullet.position.y >= self.height - 5:
                        self.alien.bullets.remove(bullet)