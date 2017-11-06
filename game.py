import sys
import pygame
from pygame.locals import *

from abc import ABC, abstractmethod
#from ship import Ship

class Game( ABC ):
    """
    Game is an abstract base class to manage basic game concepts
    """
    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height

        # Running game state
        self.running = True

        # Keep track of how many times we have drawn a frame in the game:
        self.frame = 0

        # create graphical frame
        pygame.display.init()
        pygame.font.init()
        pygame.display.set_caption(name)

        # Store the screen object for drawing too
        self.screen = pygame.display.set_mode([width,height])

    def runGame(self):
        # Our "infinite" loop for the game logic and drawing
        while self.running:
            # WARNING: the following code is very important, if we don't loop
            # through all the events then the game window will never be drawn!
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.handle_input()
            self.update_simulation()
            self.paint()
        pygame.quit()

    def paint(self):
        #self.screen.fill( (0,0,0) )
        self.render_objects()
        pygame.display.flip()

    def handle_input(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[K_q]:
            print("User initiated a QUIT")
            self.running = False  # So the user can close the program

    def update_simulation(self):
        self.frame += 1

    @abstractmethod
    def render_objects(self):
        pass

