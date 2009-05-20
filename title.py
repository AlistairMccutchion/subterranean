import os

import pygame
from pygame.locals import *

from pgu import engine

from cnst import *

class Title(engine.State):
    def __init__(self,game):
        self.game = game
        
    def init(self):
        self.game.music('default')
        self.bkgr = pygame.image.load(os.path.join("data","title","title.png")).convert()
        self.elevator = pygame.image.load(os.path.join("data","title","elevator.png")).convert_alpha()
        self.darkness = pygame.image.load(os.path.join("data","title","darkness.png")).convert_alpha()
        self.logo = pygame.image.load(os.path.join("data","title","logo.png")).convert_alpha()
        self.frame = 0
        self.shake = 1
        
        import rooms.test
        self.next = rooms.test.Room(self.game,'title')

        
    def update(self,screen):
        self.paint(screen)
        
    def paint(self,screen):
        #KALLE: Me dont understand... :)
        f = self.frame
        n = FPS*3
        i = f-FPS*3
        y = SW*i/(FPS*1)
        if i > int(FPS*4.5) and f%5 == 0:
            screen.fill((0,0,0),(0,0,SW,485))
        else:
            if self.shake == 1: self.shake=2
            else: self.shake = 1
            screen.blit(self.bkgr,(self.shake,0))
            screen.blit(self.elevator,(286,y))
            screen.blit(self.darkness,(0,0))
            screen.blit(self.logo,(25,175))
        pygame.display.flip()
        
    def event(self,e):
        if e.type is KEYDOWN:
            return self.next            
        
    def loop(self):
        self.frame += 1
        
        if self.frame > (FPS*8):
            return self.next

        
    
