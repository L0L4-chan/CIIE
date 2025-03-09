'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''
import pygame, sys

from game.gameManager import GameManager
# Main class start of the game
if __name__ == "__main__":
    pygame.init()
    path_icon = f"../Art/varios/life2.png"
    icon = pygame.image.load(path_icon)
    pygame.display.set_icon(icon)
    game = GameManager()  #create the singleton
    game.run()
    pygame.quit()
    sys.exit()
    