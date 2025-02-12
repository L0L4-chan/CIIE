'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, sys
from gameManager import GameManager
from platform import Platform
from button import Button


class Game():

    def __init__(self, scene = None, sound = None):
       
       self.gameManager = GameManager.get_instance()
       self.screen = self.gameManager.screen

       self.clock = self.gameManager.clock         

       self.scene = scene
       self.bg = pygame.image.load(f"Art/{self.gameManager.artpath}/background/{self.scene.background}")
       self.sound = sound

       self.platforms = pygame.sprite.Group()
       self.floor = pygame.sprite.Group()
       
       self.generate_floor()
       
       self.buttons = {
            "pause": Button(pos=(self.gameManager.WIDTH - 100, self.gameManager.HEIGTH / 8), 
                text_input=self.gameManager.btn_text["PAUSE"], 
                size=self.gameManager.btn_lettering),

            "quit": Button(pos=(self.gameManager.WIDTH / 16, self.gameManager.HEIGTH / 8), 
                text_input=self.gameManager.btn_text["QUIT"], 
                size=self.gameManager.btn_lettering),

        }
       
       pygame.mixer.music.stop()
       pygame.mixer.music.load(self.sound)
       pygame.mixer.music.play()

    def generate_floor(self):
        platform_width = 80
        num_platforms = self.gameManager.WIDTH // platform_width + 1
        floor_y = self.gameManager.HEIGTH - 50  

        for i in range(num_platforms):
            platform = Platform(i * platform_width, floor_y, platform_width, self.scene.pt_skin)
            self.platforms.add(platform)
            self.floor.add(platform)

    def run(self):
        running = True
        while running:
            self.clock.tick(self.gameManager.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.buttons["pause"].checkForInput(pygame.mouse.get_pos()):
                        #todo menu pausa 
                        print("pause has been press")
                    if self.buttons["quit"].checkForInput(pygame.mouse.get_pos()):
                        self.gameManager.running = False
                        pygame.quit()
                        sys.exit()
                
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.gameManager.player.jump(self.floor)

            self.gameManager.player.move()
            self.gameManager.player.update(self.floor)

            
            self.screen.blit(self.bg, (0, 0))
            for btn in self.buttons.values():
                btn.update(self.screen)
            
            for platform in self.platforms:
                platform.update(self.screen)
            self.screen.blit(self.gameManager.player.surf, self.gameManager.player.rect.topleft)

            pygame.display.flip()

        pygame.quit()


        