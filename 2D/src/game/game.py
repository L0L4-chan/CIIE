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
from game.platforms import Platforms


class Game():

    def __init__(self, scene = None, sound = None):
       
       self.gameManager = GameManager.get_instance()
       self.config = ConfigManager().get_instance() #esto te dara el path el ancho y alto....
       self.clock = self.gameManager.clock         

       self.scene = scene
       self.bg = pygame.image.load(f"../Art/{self.config.get_artpath()}/background/{self.scene.background}")
       self.sound = sound

       self.platforms = pygame.sprite.Group()
       self.floor = pygame.sprite.Group()
       
       self.generate_floor()
       
       self.buttons = {
            "pause": Button(pos=(self.config.get_width() - 100, self.config.get_height() / 8), 
                text_input=self.gameManager.btn_text["PAUSE"]),

            "quit": Button(pos=(self.config.get_width()/ 16, self.config.get_height() / 8), 
                text_input=self.gameManager.btn_text["QUIT"]),

        }
       
       pygame.mixer.music.stop()
       pygame.mixer.music.load(self.sound)
       pygame.mixer.music.play(-1)

    def generate_floor(self):
        platform_width = 80
        num_platforms = self.config.get_width() // platform_width + 1
        floor_y =  self.config.get_height() - 50 

        for i in range(num_platforms):
            platform = Platforms(i * platform_width, floor_y, platform_width, self.scene.pt_skin)
            self.platforms.add(platform)
            self.floor.add(platform)

    def run(self):
        running = True
        while running:
            self.clock.tick(self.config.get_fps())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.buttons["pause"].checkForInput(pygame.mouse.get_pos()):
                        #todo menu pausa 
                        print("pause has been press")
                    if self.buttons["quit"].checkForInput(pygame.mouse.get_pos()):
                        running = False
                
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.gameManager.player.jump(self.floor)

            self.gameManager.player.move()
            self.gameManager.player.update(self.floor)

            self.gameManager.enemy.move()


            
            self.gameManager.screen.blit(self.bg, (0, 0))
            for btn in self.buttons.values():
                btn.update(self.gameManager.screen)
            
            for platform in self.platforms:
                platform.update(self.gameManager.screen)
            self.gameManager.screen.blit(self.gameManager.player.surf, self.gameManager.player.rect.topleft)
            
            self.gameManager.screen.blit(self.gameManager.enemy.surf, self.gameManager.enemy.rect.topleft)


            pygame.display.flip()

        self.gameManager.running = False


        