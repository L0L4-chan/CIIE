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
from views.dialogBox import DialogBox

class AnimationPlayer():
    def __init__(self, path, start, amount, event):
        super().__init__()
        self.gameManager = GameManager.get_instance()
        self.config = ConfigManager().get_instance()
        self.path = path
        self.frames = sorted(os.listdir(f"../Art/{self.config.get_artpath()}/{path}"))
        self.frame_index = 0
        self.end = len(self.frames) -1
        self.fps = 24
        self.running = True
        self.start = start # cuando sea mostrado el primer texto
        self.amount = amount
        self.get_boxes(event) # creamos los textos necesarios
    
    
    def get_boxes(self, event):
       self.boxes = []
       
       for i in range(event, event + self.amount): 
        self.boxes.append(DialogBox(bg_image = "../Art/varios/dialog.png" ,event = i))  # Pasamos el número actual del loop

    
    def show_dialog(self):
        
        frames = (self.start - (self.end + 50)) / self.amount 
        for i in range(self.amount):
            if (self.frame_index >= (self.start + (frames * i))) and (self.frame_index <= (self.end - 50)):  
                self.boxes[i].draw()
    
    
    def run(self):
      #de momento para probar.
      while(self.running):
          
        self.frame_path = os.path.join(f"../Art/{self.config.get_artpath()}/{self.path}", self.frames[self.frame_index])
        self.frame = pygame.image.load(self.frame_path)
        self.gameManager.screen.blit(self.frame, (0, 0))
        self.show_dialog() 
        
        pygame.display.flip()
        self.gameManager.clock.tick(self.fps)
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        
        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.gameManager.running = False
        #end of the animation
        if self.frame_index == self.end:
            self.running = False     