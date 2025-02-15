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
from ui.button import Button
from game.objects.platforms import Platforms


class Game():

    def __init__(self, scene = None, sound = None):
       
       self.gameManager = GameManager.get_instance() #proporciona el screen, textos, reloj...
       self.config = ConfigManager().get_instance() #esto te dara el path el ancho y alto....       
       #cuando se trate del nivel en lugar de una escena se pasara la lista de escenas que debera gestionar los cambios de momento tiene una 
       self.scene = scene
       self.bg = pygame.image.load(f"../Art/{self.config.get_artpath()}/background/{self.scene.background}")
       self.sound = sound

       self.platforms = pygame.sprite.Group()
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

    #funcion de generación de suelo
    def generate_floor(self):
        platform_width = 80
        platform_height = 18
        num_platforms = self.config.get_width() // platform_width + 1
        floor_y =  self.config.get_height() - 50 

        for i in range(num_platforms):
            platform = Platforms(i * platform_width, floor_y, platform_width, platform_height, self.scene.pt_skin)
            self.platforms.add(platform)
            self.floor.add(platform)

    #game loop se modificara si es necesario cuando se tengan los niveles
    def run(self):
        running = True
        
        while running:
            self.gameManager.clock.tick(self.config.get_fps())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.buttons["pause"].checkForInput(pygame.mouse.get_pos()):
                        #todo menu pausa 
                        print("pause has been press")
                    if self.buttons["quit"].checkForInput(pygame.mouse.get_pos()):
                        running = False    
                
                if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_SPACE and not self.gameManager.player.shooting:
                        self.gameManager.player.shooting = True
                        self.gameManager.player.index = 0
                
            stone = self.gameManager.player.shoot()
            if stone:
                self.stones.add(stone)
            else:
                if not self.gameManager.player.shooting:
                    self.gameManager.player.update(self.floor)
            
            self.gameManager.enemy.move()


            
            self.gameManager.screen.blit(self.bg, (0, 0))
            for btn in self.buttons.values():
                btn.update(self.gameManager.screen)
            
            for platform in self.platforms:
                platform.update(self.gameManager.screen)
            
            for stn in self.stones:
                stn.update(self.gameManager.screen)
            
            self.gameManager.screen.blit(self.gameManager.player.surf, self.gameManager.player.rect.topleft)
            
            self.gameManager.screen.blit(self.gameManager.enemy.surf, self.gameManager.enemy.rect.topleft)


            pygame.display.flip()

        self.gameManager.running = False


        