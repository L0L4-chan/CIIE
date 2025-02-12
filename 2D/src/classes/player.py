'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''
import pygame, sys , random
from game.gameManager import GameManager
vec = pygame.math.Vector2 #2 for two dimensional

class Player(pygame.sprite.Sprite):
    #variables
    ACC = 0.5
    FRIC = -0.12


    #constructor
    def __init__(self, x, y):
        super().__init__()
        self.gameManager = GameManager.get_instance()
        self.surf = pygame.image.load(f"Art/{self.gameManager.artpath}/skelly/skeleton_1.png")
        self.rect = self.surf.get_rect()
        self.pos = vec(x,y)
        self.vel = vec(0,0)

        self.jumping = False
        self.speed = 5
        

    def move(self):
        self.acc = vec(0,0.5)
    
        pressed_keys = pygame.key.get_pressed()
                
        if pressed_keys[pygame.K_LEFT]:
            self.acc.x = - self.ACC
        if pressed_keys[pygame.K_RIGHT]:
            self.acc.x = self.ACC
                 
        self.acc.x += self.vel.x * self.FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        if self.pos.x > self.gameManager.WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = self.gameManager.WIDTH
             
        self.rect.midbottom = self.pos
 
    def jump(self, platforms): 
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
           self.jumping = True
           self.vel.y = -15
 
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
 
    def update(self, platforms):
        hits = pygame.sprite.spritecollide(self ,platforms, False)
        if self.vel.y > 0:        
            if hits:
                if self.pos.y < hits[0].rect.bottom:         
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False

