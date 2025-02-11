'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, sys, gameManager


class Game():

    def __init__(self):
       pygame.init()


    def main():

        while gameManager.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False




            # game code

            # update frame
            pygame.display.update()
            gameManager.clock.tick(gameManager.FPS)


        pygame.quit()
        sys.exit()