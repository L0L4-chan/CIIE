'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, sys
from gameManager import GameManager


class Game():

    def __init__(self):
       pygame.init()
       self.gameManager = GameManager.get_instance()


    def main(self):

        while self.gameManager.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False




            # game code

            # update frame
            pygame.display.update()
            self.gameManager.clock.tick(self.gameManager.FPS)


        pygame.quit()
        sys.exit()