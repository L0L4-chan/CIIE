'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, os
from game.gameManager import GameManager
from game.configManager import ConfigManager
from views.scene import Scene
from classes.player import Player
from enemies.boss import Boss

from game.game import Game

class Start():

   def __init__(self, path, sound, event):
      super().__init__()
      self.gameManager = GameManager.get_instance()
      self.config = ConfigManager()
      self.frames = sorted(os.listdir(f"../Art/{self.config.get_artpath()}/{path}"))
      self.frame_index = 0
      self.fps = 24
      
      pygame.mixer.music.stop()
      pygame.mixer.music.load(sound)
      pygame.mixer.music.play()

      self.font =  self.config.get_font()
      self.dialog = next((d["text"] for d in self.gameManager.texts["dialogues"] if d["event"] == event), None)
      self.running = True
   
   def run(self):
      #de momento para probar.
      while(self.running):
         
         frame_path = os.path.join(f"../Art/{self.config.get_artpath()}/1animation", self.frames[self.frame_index])
         frame = pygame.image.load(frame_path)

      
         self.gameManager.screen.blit(frame, (0, 0))


         if self.frame_index >= 200 and self.frame_index < 450:    
            text = self.font.render(self.dialog, True, (255, 255, 255))
            self.gameManager.screen.blit(text, (50, (self.config.get_height()/6) - 50))
         
         pygame.display.flip()
         self.gameManager.clock.tick(self.fps)

         self.frame_index = (self.frame_index + 1) % len(self.frames)

         # Manejar eventos
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                  self.running = False
                  self.gameManager.running = False
         if self.frame_index == 590:
            self.running = False     

      self.gameManager.player = Player(400,300)
      self.gameManager.enemy = Boss(400,300)
      self.gameManager.scene = Game(Scene(background="cementerio.PNG", pt_skin= "../Art/varios/Tiles/Tile_a(7).png"), sound = "../Sound/BSO/levels-_2_.wav" )