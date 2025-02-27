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
    #pygame.mixer.pre_init(44100,16,2,4096) #initialize the mixer (sound)
    #pygame.mixer.init()
    #pygame.mixer.set_num_channels(8)
    game = GameManager()  #create the singleton
    game.load_menu() #load first screen
    pygame.quit()
    sys.exit()
    