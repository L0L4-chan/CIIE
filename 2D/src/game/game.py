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
from game.objects.lives import Lives
from ui.button import Button
from ui.pausa import Pausa
vec = pygame.math.Vector2  


class Game():

    def __init__(self, scene = None, sound = None):      
       #cuando se trate del nivel en lugar de una escena se pasara la lista de escenas que debera gestionar los cambios de momento tiene una 
       self.scene = scene
       self.bg = pygame.image.load(f"../Art/{ConfigManager().get_instance().get_artpath()}/background/{self.scene.background}")
       self.sound = sound
       self.running = False
       self.sprites = pygame.sprite.Group()
       self.floor = pygame.sprite.Group()
       self.stones = pygame.sprite.Group()
       self.group_lives = pygame.sprite.Group()
       
       self.screen_width = ConfigManager().get_instance().get_width()
       self.screen_height =  ConfigManager().get_instance().get_height()
       
       self.screen = GameManager.get_instance().screen
       self.clock =  GameManager().get_instance().clock
       self.FPS = ConfigManager().get_instance().get_fps()
       
       self.buttons = {
            "pause": Button(pos=(ConfigManager().get_instance().get_width() - 100, ConfigManager().get_instance().get_height() / 8), 
                text_input=ConfigManager().get_instance().get_text_button(key ="PAUSE")),

            "quit": Button(pos=(ConfigManager().get_instance().get_width()/ 16, ConfigManager().get_instance().get_height() / 8), 
                text_input=ConfigManager().get_instance().get_text_button(key ="QUIT")),

        }
       
       self.player = GameManager().get_instance().player
       self.enemy =GameManager().get_instance().enemy
       
       #generamos suelo (funcion que debera ser modificada cuando se tengan los niveles)
       self.generate_floor()
       #empieza la musica del nivel
       pygame.mixer.music.stop() #paramos la anterior
       pygame.mixer.music.load(self.sound)
       pygame.mixer.music.play(-1) #indicamos loop infinito

       self.sprites.add(self.player)
       self.sprites.add(self.enemy)
        
    #funcion de generación de suelo
    def generate_floor(self):
        platform_width = 80
        platform_height = 18
        num_platforms = self.screen_width // platform_width + 1
        floor_y = self.screen_height - 50 

        for i in range(num_platforms):
            platform = Platforms(i * platform_width, floor_y, platform_width, platform_height, self.scene.pt_skin)
            self.floor.add(platform)
            self.sprites.add(platform)
    
    #game loop se modificara si es necesario cuando se tengan los niveles
    
    
    def run(self):
        
        self.running = True
 
        while self.running:
            
            self.clock.tick(self.FPS) # indicamos el numero de frames por segundo

            if self.player.get_lives() == 0:
                GameManager().get_instance().end_game()

            # Se manejan los eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    GameManager().get_instance().running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.buttons["pause"].checkForInput(pygame.mouse.get_pos()):
                        #todo menu pausa 
                        Pausa(GameManager().get_instance().screen)
                    if self.buttons["quit"].checkForInput(pygame.mouse.get_pos()):
                        self.running = False
                        GameManager().get_instance().running = False    

                
            
            self.player.update(self.floor) #actualiza al player
            self.stones = self.player.group  #añade piedras al grupo de piedras para su visualizacion
            self.enemy.move() #actualiza al enemigo
            
            self.screen.blit(self.bg, (0,0)) #carga el fondo (en la escena completa el 0,0 tendra que varias con los movimientos del personaje TODO)
            
            for btn in self.buttons.values(): #carga botones
                btn.update(self.screen)
            
            for i in range(self.player.get_lives()): 
                self.group_lives.add(Lives(path= "../Art/big/avatar/live.png", x = 400 + (i * 30), y = 50))#todo make dinamic

            self.group_lives.update(self.screen)
            
            for platform in self.floor: #carga plataformas
                platform.update(self.screen)
            
            for stn in self.stones: #carga piedrass
                stn.update(self.screen, self.sprites)
            
            self.screen.blit(self.player.surf, self.player.rect.topleft) #carga player
            
            self.screen.blit(self.enemy.surf, self.enemy.rect.topleft) # carga al enemigo 

            #Muestra por pantalla
            pygame.display.flip()
        
        


        