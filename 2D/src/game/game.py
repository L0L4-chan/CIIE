'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame
from game.gameManager import GameManager
from game.configManager import ConfigManager
from game.objects.platforms import Platforms
from ui.button import Button
from ui.pausa import Pausa



class Game():

    def __init__(self, scene = None, sound = None):
       
       self.gameManager = GameManager.get_instance() #proporciona el screen, textos, reloj...
       self.config = ConfigManager().get_instance() #esto te dara el path el ancho y alto....       
       #cuando se trate del nivel en lugar de una escena se pasara la lista de escenas que debera gestionar los cambios de momento tiene una 
       self.scene = scene
       self.bg = pygame.image.load(f"../Art/{self.config.get_artpath()}/background/{self.scene.background}")
       self.sound = sound
       self.running = False
       self.sprites = pygame.sprite.Group()
       self.floor = pygame.sprite.Group()
       self.stones = pygame.sprite.Group()
       #generamos suelo (funcion que debera ser modificada cuando se tengan los niveles)
       self.generate_floor()
       
       self.buttons = {
            "pause": Button(pos=(self.config.get_width() - 100, self.config.get_height() / 8), 
                text_input=self.config.get_text_button(key ="PAUSE")),

            "quit": Button(pos=(self.config.get_width()/ 16, self.config.get_height() / 8), 
                text_input=self.config.get_text_button(key ="QUIT")),

        }
       #empieza la musica del nivel
       pygame.mixer.music.stop() #paramos la anterior
       pygame.mixer.music.load(self.sound)
       pygame.mixer.music.play(-1) #indicamos loop infinito

       self.sprites.add(self.gameManager.player)
       self.sprites.add(self.gameManager.enemy)
        
    #funcion de generación de suelo
    def generate_floor(self):
        platform_width = 80
        platform_height = 18
        num_platforms = self.config.get_width() // platform_width + 1
        floor_y =  self.config.get_height() - 50 

        for i in range(num_platforms):
            platform = Platforms(i * platform_width, floor_y, platform_width, platform_height, self.scene.pt_skin)
            self.floor.add(platform)
            self.sprites.add(platform)
    #game loop se modificara si es necesario cuando se tengan los niveles
    def run(self):
        
        self.running = True
 
        while self.running:
            
            self.gameManager.clock.tick(self.config.get_fps()) # indicamos el numero de frames por segundo

            # Se manejan los eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.buttons["pause"].checkForInput(pygame.mouse.get_pos()):
                        #todo menu pausa 
                        Pausa(self.gameManager.screen)
                    if self.buttons["quit"].checkForInput(pygame.mouse.get_pos()):
                        self.running = False    
            
                
            
            self.gameManager.player.update(self.floor, self.gameManager.screen) #actualiza al player
            self.stones.add(self.gameManager.player.projectiles)  #añade piedras al grupo de piedras para su visualizacion
            self.gameManager.enemy.move() #actualiza al enemigo

            self.gameManager.screen.blit(self.bg, (0, 0)) #carga el fondo (en la escena completa el 0,0 tendra que varias con los movimientos del personaje TODO)
            
            for btn in self.buttons.values(): #carga botones
                btn.update(self.gameManager.screen)
            
            for platform in self.floor: #carga plataformas
                platform.update(self.gameManager.screen)
            
            for stn in self.stones: #carga piedrass
                stn.update(self.gameManager.screen)
            
            self.gameManager.screen.blit(self.gameManager.player.surf, self.gameManager.player.rect.topleft) #carga player
            
            self.gameManager.screen.blit(self.gameManager.enemy.surf, self.gameManager.enemy.rect.topleft) # carga al enemigo 

            #Muestra por pantalla
            pygame.display.flip()
        
        #maneja la salida y cierre para que todos los bucles finalicen correctamente
        self.gameManager.running = False


        