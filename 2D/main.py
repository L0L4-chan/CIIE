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
import player


pygame.init()

FramePerSec = pygame.time.Clock()




#Game Loop

while(True):



   # game code

    # update frame
    pygame.display.update()
    FramePerSec.tick(c.FPS)
