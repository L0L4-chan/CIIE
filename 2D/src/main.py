'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''
import pygame, sys, utils.globals as globals, utils.auxiliar as auxiliar

from game.gameManager import GameManager
# Main class comienzo del juego
if __name__ == "__main__":
    pygame.init()
    globals.game = GameManager()
    icon = pygame.image.load(auxiliar.get_path(globals.config.get_iconpath())) # carga del icono
    pygame.display.set_icon(icon)# asignación del icono
    globals.game.run()
    pygame.quit()
    sys.exit()
    