import sys
import random
import pygame
from pygame.locals import *
import math
from game import Game
from Ship import Ship
from Ship import Bullet
from astreoid import Astreoid
from point import Point
from Ship import Star
              
class Asteroids( Game ):
    """
    Asteroids extends the base class Game to provide logic for the specifics of the game
    """
    def __init__(self, name, width, height):
        super().__init__( name, width, height )
        pygame.init()
        self.ship = Ship()
        self.asteroids= []
        self.stars=[]
        self.bullets = []
        self.score = 0
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background_image =pygame.image.load("skyy.jpg").convert()
        self.max_num_asteroids = 5
        self.current_level = 1
        self.new_level = True
        self.lifebar= "[][][][][]"
        self.timer = 0
        self.explosions=set([])
    
        
    def handle_input(self):
        super().handle_input()
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[K_LEFT] and self.ship:
            self.ship.rotate(-0.5)
        if keys_pressed[K_RIGHT] and self.ship:
            self.ship.rotate(0.5)
        if keys_pressed[K_UP] and self.ship:
            self.ship.accelerate(0.0009)
        if keys_pressed[K_DOWN] and self.ship:
            self.ship.accelerate(0)
        if keys_pressed[K_SPACE] and self.ship:
            if pygame.time.get_ticks() > self.timer:
                self.timer = pygame.time.get_ticks() + 300
                self.ship.shoot()
                if len(self.bullets) <= 5:
                    self.bullets.append(Bullet(self.ship.position,self.ship.rotation))
                else:
                    self.bullets.clear()
                    self.bullets.append(Bullet(self.ship.position,self.ship.rotation))
    
    def calc_distance(self,p, q):
        return math.sqrt((p.x-q.x)**2 + (p.y-q.y)**2)
    
    def collision_detect(self):
        found = False
        if len(self.bullets)>0:
            for bullet in self.bullets:
                for asteroid in self.asteroids:
                    if self.calc_distance(bullet.position, asteroid.position)<30:
                        if asteroid.explode():
                            self.asteroids.remove(asteroid)
                            self.score += 20
                        else:
                            found = True
                            newsize = asteroid.get_size()
                            position= asteroid.position
                            self.asteroids.remove(asteroid)
                            self.score +=10
                            
                        if bullet in self.bullets:
                            self.bullets.remove(bullet) 
        
        if found:
            ast = self.CreateAsteroid(position, newsize)
            asttwo = self.CreateAsteroid(position, newsize)
            self.asteroids.append(ast)
            self.asteroids.append(asttwo)
                     
        if len(self.asteroids)>0 and self.ship.life >0:
            for asteroid in self.asteroids:
                if self.calc_distance(self.ship.position, asteroid.position)<30:
                    asteroid.explode()
                    self.asteroids.remove(asteroid)
                    self.ship.life -= 1
                    self.lifebar = self.lifebar[:-2]
                    
    
    
    def CreateAsteroid(self, pos, size):
        if pos == "random" :
            x = random.randint(0,600)
            y = random.randint(0,430)
        else:
            x = pos.x
            y = pos.y
       
        rotation=random.randint(0,5)
        point_x= random.uniform(-0.001,0.5)
        point_y = random.uniform(-0.001,0.5)
        angular_velocity = random.uniform(0.1, 0.8)
        if size == "medium":
            points= [ Point(10,30), Point(30,10), Point(40,30), Point(30,40) ]
        elif size == "small":
            points= [ Point(10,20), Point(20,10), Point(30,20), Point(20,30) ]
        else:
            points= [ Point(0,40), Point(40,0), Point(50,30), Point(30,50) ]
        return Astreoid(points, x, y, rotation,Point(point_x, point_y), angular_velocity,size)
            
                                        
    def spawn_asteroids(self):
        sizes = ["small", "medium", "big"]
        
        if self.new_level:
            if len(self.asteroids)<self.max_num_asteroids:
            
                for i in range(0,self.max_num_asteroids):
                    size = sizes[random.randint(0,2)]
                    asteroid = self.CreateAsteroid("random", size)
                    self.asteroids.append(asteroid)
                    self.new_level = False
                           
                    
    def show_lifebar(self):
        myfont=pygame.font.SysFont("Britannic Bold", 40)
        nlabel=myfont.render(self.lifebar+str(self.ship.life), 1, (255, 128, 0))
        self.screen.blit(nlabel,(5,450))
                
              
    def life_check(self):
        if self.ship.life == 0:
             self.screen.blit(self.background_image, [0, 0])
             myfont=pygame.font.SysFont("Britannic Bold", 40)
             nlabel=myfont.render("YOU DIE!", 1, (255, 128, 0))
             self.screen.blit(nlabel,(220,100))
             for event in pygame.event.get():
                 if event.type==MOUSEBUTTONDOWN:
                     break
        
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
            
    def check_victory(self):
        if len(self.asteroids) ==0:
            if self.current_level == 5:  
                self.screen.blit(self.background_image, [0, 0])
                myfont=pygame.font.SysFont("Britannic Bold", 40)
                nlabel=myfont.render("YOU WIN!", 1, (255, 128, 0))
                self.screen.blit(nlabel,(220,100))
                for event in pygame.event.get():
                    if event.type==MOUSEBUTTONDOWN:
                        break
            else:
                self.screen.blit(self.background_image, [0, 0])
                myfont=pygame.font.SysFont("Britannic Bold", 40)
                nlabel=myfont.render("YOU MADE IT TO THE NEXT LEVEL!", 1, (255, 128, 0))
                nlabel1=myfont.render("CLICK TO CONTINUE!", 1, (255, 128, 0))
                self.screen.blit(nlabel,(30,100))
                self.screen.blit(nlabel1,(30,140))
                for event in pygame.event.get():
                    if event.type==MOUSEBUTTONDOWN:
                        self.new_level = True
                        self.current_level += 1
                        self.check_max_asteroids()
            
    def spawn_stars(self):
        if self.new_level:
            self.stars.clear()
        if len(self.stars)<100:
            self.stars.append(Star())
            
        
    def start_screen(self):
        start=False
        while (start==False):
            
            self.screen.blit(self.background_image, [0, 0])
            myfont=pygame.font.SysFont("Britannic Bold", 40)
            nlabel=myfont.render("WELCOME", 1, (128, 128, 128))
            nlabel1=myfont.render("TO ASTEROIDS", 1, (128, 128, 128))
            nlabel2=myfont.render("CLICK TO START", 1, (128,128,128))
            for event in pygame.event.get():
                if event.type==MOUSEBUTTONDOWN:
                    start=True
            self.screen.blit(nlabel,(220,100))
            self.screen.blit(nlabel1, (195,150))
            self.screen.blit(nlabel2, (185, 200))
            pygame.display.flip()
    
    def print_score_and_level(self):
         myfont=pygame.font.SysFont("Britannic Bold", 20)
         nlabel=myfont.render("Score:" + str(self.score), 1, (128, 120, 120))
         nlabel1=myfont.render("Level:" + str(self.current_level), 1, (128, 120, 120))
         self.screen.blit(nlabel,(10,10))
         self.screen.blit(nlabel1, (10, 25))
         
    def update_simulation(self):
        
        black=(0,0,0)
        self.screen.fill(black)
        self.spawn_stars()
        self.spawn_asteroids()
        """
        update_simulation() causes all objects in the game to update themselves
        """
        super().update_simulation()
        self.collision_detect()
        self.check_victory()
        self.print_score_and_level()
        self.show_lifebar()
        self.life_check()
        if self.ship:
            self.ship.update( self.width, self.height )
        for asteroid in self.asteroids:
            asteroid.update( self.width, self.height )
        for star in self.stars:
            star.update( self.width, self.height )
        for bullets in self.bullets:
            bullets.update( self.width, self.height)
        # TODO: should probably call update on our bullet/bullets here
        # TODO: should probably work out how to remove a bullet when it gets old
        
        
    def render_objects(self):
        """
        render_objects() causes all objects in the game to draw themselves onto the screen
        """
        super().render_objects()
        # Render the ship:
        if self.ship:
            self.ship.draw( self.screen )
        # Render all the stars, if any:
        for star in self.stars:
            star.draw( self.screen )
        # Render all the asteroids, if any:
        for asteroid in self.asteroids:
            asteroid.draw( self.screen )
        # Render all the bullet, if any:
        for bullet in self.bullets:
            bullet.draw( self.screen )

