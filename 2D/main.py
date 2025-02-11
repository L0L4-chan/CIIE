'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

from gameManager import GameManager

if __name__ == "__main__":
    game = GameManager() 
    game.load_menu()
    game.run()