'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''
import pygame, sys , random
import config as c

class Player():
    #variables

    #conxtructor
    def __init__(self, x, y):
        super().__init__()
        self.pos = c.vec(0.0)
        self.vel = c.vec(0,0)

        self.jumping = False
        self.speed = 5
        self.score = 0 
        

    def jump(self):
        self.pos.y += 1

    #update function
    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE]:
            self.jump(self) 
