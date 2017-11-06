import sys
import random
import pygame
from pygame.locals import *
import math
from game import Game
from Ship import Ship
from spaceObjects import Bullet
from astreoid import Astreoid
from point import Point
from spaceObjects import Star
from spaceObjects import Alien
from button import Button

pygame.init()
class Asteroids( Game ):
    """
    Asteroids extends the base class Game to provide logic for the specifics of the game
    """
    def __init__(self, name, width, height):
        super().__init__( name, width, height )
        
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
        self.alien =[]
        self.state = "startmenu"
        self.buttons = []
        
    def handle_input(self):
        super().handle_input()
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[K_r] and self.ship.life == 0:
           self.restart_game()
        if keys_pressed[K_LEFT] and self.ship:
            self.ship.rotate(-0.5)
        if keys_pressed[K_RIGHT] and self.ship:
            self.ship.rotate(0.5)
        if keys_pressed[K_UP] and self.ship:
            self.ship.accelerate(0.0009)
        if keys_pressed[K_DOWN] and self.ship:
            self.ship.accelerate(0)
        if keys_pressed[K_p] and self.state == "running":
            self.state = "paused" 
        if keys_pressed[K_s] and self.state == "paused":
            self.state = "running"
        if keys_pressed[K_SPACE] and self.ship:
            if pygame.time.get_ticks() > self.timer:
                self.timer = pygame.time.get_ticks() + 300
                self.ship.shoot()
                if len(self.bullets) <= 5:
                    self.bullets.append(Bullet(self.ship.position,self.ship.rotation))
                else:
                    self.bullets.clear()
                    self.bullets.append(Bullet(self.ship.position,self.ship.rotation))
        
    
    def paused(self):
        pause_text = pygame.font.SysFont('Consolas', 32).render('Paused', True, pygame.color.Color('White'))
        self.screen.blit(pause_text,(240,240))
        
    def restart_game(self):
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
        self.alien =[]
        self.state = "running"
    
    def empty_screen(self):
        self.new_Level = False
        # Render all the stars, if any:
        for star in self.stars:
            self.stars.remove(star)
        # Render all the asteroids, if any:
        for asteroid in self.asteroids:
            self.asteroids.remove(asteroid)
        # Render all the bullet, if any:
        for bullet in self.bullets:
            self.bullets.remove(bullet)
        for alien in self.alien:
            self.alien.remove(alien)
        
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
                    
    
    def CreateAlien(self):
        self.alien.append(Alien())
        
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
            points= [ Point(10,30), Point(20,1), Point(30,10), Point(40,30), Point(30,40), Point(15,40)]
        elif size == "small":
            points= [ Point(10,20), Point(12,12),Point(20,10), Point(28,12),Point(30,20), Point(28,30),Point(20,30)]
        else:
            points= [ Point(0,40), Point(0,10),Point(10,0),Point(40,0), Point(50,30), Point(30,50)]
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
        if not self.ship.life == 0:
            self.screen.blit(nlabel,(5,450))
                
              
    def life_check(self):
        if self.ship.life == 0:
            self.empty_screen()
            myfont=pygame.font.SysFont("Britannic Bold", 40)
            self.screen.blit(self.background_image, [0, 0])
            gameover = myfont.render("Gameover!", 1, (255, 255, 255))
            respawn = myfont.render("Press R to Respawn",1, (255,255,255))
            self.screen.blit(gameover,(210,200))
            self.screen.blit(respawn,(160,250))
        
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
        if len(self.asteroids) ==0 and not self.ship.life == 0:
            if self.current_level == 5:
                boss = False 
                if not boss:
                    CreateAlien()
                    boss = True
                
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
                nlabel=myfont.render("YOU MADE IT TO THE NEXT LEVEL!", 1, (255, 255, 255))
                nlabel1=myfont.render("CLICK TO CONTINUE!", 1, (255,255,255))
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
        if len(self.stars)<100 and not self.ship.life ==0:
            self.stars.append(Star())
    
    def print_score_and_level(self):
         myfont=pygame.font.SysFont("Britannic Bold", 20)
         nlabel=myfont.render("Score:" + str(self.score), 1, (128, 120, 120))
         nlabel1=myfont.render("Level:" + str(self.current_level), 1, (128, 120, 120))
         self.screen.blit(nlabel,(10,10))
         self.screen.blit(nlabel1, (10, 25))
      
    def start_menu(self):
        self.screen.blit(self.background_image, [0, 0])
        myfont=pygame.font.SysFont("Britannic Bold", 40)
        nlabel=myfont.render("WELCOME", 1, (255, 255, 255))
        nlabel1=myfont.render("TO ASTEROIDS", 1, (255,255, 255))
        self.screen.blit(nlabel,(230,100))
        self.screen.blit(nlabel1, (195,150))
        #pygame.display.flip()
        start = Button((170, 200, 80,30), 'START')
        self.buttons.append(start)
        options  = Button((260, 200, 80,30), 'OPTIONS')
        self.buttons.append(options)
        bquit  = Button((350, 200, 80,30), 'QUIT')
        self.buttons.append(bquit)
        for b in self.buttons:
            b.draw(self.screen)
            
           
        
                
    def update_simulation(self):
        
        """
        update_simulation() causes all objects in the game to update themselves
        """
            
        
        super().update_simulation()
        if self.state== "running":
            black=(0,0,0)
            self.screen.fill(black)
            self.spawn_stars()
            self.spawn_asteroids()
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
            for alien in self.alien:
                alien.update(self.width, self.height)
        elif self.state == "paused":
            self.paused()
        elif self.state == "startmenu":
            
            
            for alien in self.alien:
                alien.update(self.width, self.height)
                
            self.start_menu()
            for event in pygame.event.get():
                for button in self.buttons:
                    if 'click' in button.handleEvent(event):
                        if button._propGetCaption() == "QUIT":
                            self.running= False
                        if button._propGetCaption() == "START":
                            self.state = "running"
                        if button._propGetCaption() == "OPTIONS":
                            pass
                            
        
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
        for alien in self.alien:
            alien.draw(self.screen)

