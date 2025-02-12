'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

from game.gameManager import GameManager
# Main class start of the game
if __name__ == "__main__":
    game = GameManager()  #create the singleton
    game.load_menu() #load first screen
    game.run() # start loop