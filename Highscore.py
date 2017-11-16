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

#this class reads and write to highscore.txt 
#sorts the scores and detects a highscore 

import pygame
from heapq import nsmallest
from pygame.locals import *
pygame.init()
pygame.font.init()
pygame.display.init()

WHITE = (255,255,255)
BLACK = (0,0,0)

class Highscoreboard(object):
    
    def __init__(self):
        self.newscore = 0
        self.newname = ""
        self.highscorelist = self.filetolist()
    
    #returns the smallest score from hidhscorelist
    def get_min_score(self):
        lst = []
        for a,b in self.highscorelist:
            lst.append(a+","+b)
        return min(list(map(int, [line[4:] for line in lst])))

    #reads file to list of tuples 
    def filetolist(self):
        f = open("highscore.txt", "r")
        highscorelist = [(tuple((x.strip("\n")).split(":"))) for x in f.readlines()]
        f.close()
        return highscorelist
        
    def get_key(self):
        while 1:
            event = pygame.event.poll()
            if event.type == KEYDOWN:
                return event.key
            else:
                pass
    
    def printboard(self, screen):
        reversedlist = reversed(self.highscorelist)
        i = 0
        j = 1
        screen.fill((0,0,0))
        fontobject =  pygame.font.SysFont('Consolas',30)
        titles = "RANK     NAME SCORE"
        screen.blit(fontobject.render(titles, 1, WHITE),( 100, 80))
        for line in reversedlist:
            screen.blit(fontobject.render(str(j)+ (" "*7 if j >9 else " "*8) + str(line[0])+ " "*3+str(line[1]), 1, WHITE),(100, 120+i))
            i+=32
            j+=1
            
        screen.blit(fontobject.render("return to menu (RETURN)", 1, WHITE), (100,460))
        
        pygame.display.flip()
        
        while 1:
            inkey = self.get_key()
            if inkey == K_RETURN:
                break
            screen.blit(fontobject.render(str(self.highscorelist), 1, WHITE),
                                         ((screen.get_width() / 2) - 100, (200) - 10))
            pygame.display.flip()
    
    def update_board(self):
        newlist= []
        for a, b in self.highscorelist:
            if not b == str(self.get_min_score()):
                newlist.append((a,b))

        newlist.append((self.newname, str(self.newscore)))
        newlist = sorted(newlist, key=lambda x: int(x[1]))
        self.highscorelist = newlist 
        result =[]
        for a,b in newlist:
            result.append(a+":"+str(b))
        
        string = "" 
        for word in result:
            string += str(word)+"\n"
        
        f = open("highscore.txt", 'w')
        f.write(string)
        f.close()
        
    #display output
    def display_output(self, screen, message):
        "Print a message in a box in the middle of the screen"
        fontobject = pygame.font.SysFont('Consolas',18)
  
        if len(message) != 0:
            screen.blit(fontobject.render(message, 1, WHITE),
                (100, (200) - 10))
        pygame.display.flip()

    #ask for input
    def ask_for_input(self, screen, output):
        screen.fill(BLACK)
        current_string = []
        return_string = ""
        highscore_text = pygame.font.SysFont('Consolas', 32).render("CONGRATZ, YOU GOT A HIGHSCORE!", 1, WHITE)
        screen.blit(highscore_text, (100,80))
        while not self.right_lenght_string(return_string):


            self.display_output(screen, output + ": "+ (" ".join(current_string)).upper())
            while 1:
                screen.fill(BLACK)
                inkey = self.get_key()
                if inkey == K_BACKSPACE:
                    current_string = current_string[:-1]
                elif inkey == K_RETURN:
                    break
                elif inkey <= 127:
                    current_string.append(chr(inkey))

                screen.blit(highscore_text, (100,80))
                self.display_output(screen,output + ": " + ("".join(current_string)).upper())
            output = "MUST BE 3 LETTERS OR CHARACTERS"
            return_string = "".join(current_string)
        return return_string

    def right_lenght_string(self,str):
        if len(str) != 3:
            return False
        else:
            return True

