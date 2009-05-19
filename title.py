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
        self.frame = 0
        
        import rooms.test
        self.next = rooms.test.Room(self.game,'title')

        
    def update(self,screen):
        self.paint(screen)
        
    def paint(self,screen):
		screen.blit(self.bkgr,(0,0))
		pygame.display.flip()
        
    def event(self,e):
        if e.type is KEYDOWN:
            return self.next
            
        
    def loop(self):
        self.frame += 1
        
        if self.frame > (FPS*8):
            return self.next

        
    
