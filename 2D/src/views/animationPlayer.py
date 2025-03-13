'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, os, utils.globals as globals
from views.dialogBox import DialogBox

class AnimationPlayer():
    def __init__(self, path, start, amount, event):
        super().__init__()
        self.screen = globals.game.screen
        self.clock =  globals.game.clock
        self.art_path =  globals.config.get_artpath()
        self.path = path
        self.frames = sorted(os.listdir(f"../Art/{self.art_path}/{path}"))
        self.frame_index = 0
        self.end = len(self.frames) 
        self.fps = 24
        self.running = True
        self.start = start # cuando sea mostrado el primer texto
        self.amount = amount
        self.get_boxes(event) # creamos los textos necesarios
    
    
    def get_boxes(self, event):
       self.boxes = []
       for i in range(event, event + self.amount): 
           self.boxes.append(DialogBox(event = i))  # Pasamos el número actual del loop

    
    def show_dialog(self):  
        if (self.frame_index >= self.start):
            if self.amount == 1 and self.frame_index <= (self.end - (50)):
                self.boxes[0].draw()
            else:          
                frames = ( (self.end - (self.start + 50)) / self.amount ) #350 frames   50 - 400 /2 = 125
                if (self.frame_index <= (self.end - (frames + 50))):  
                    self.boxes[0].draw()
                elif (self.frame_index <= (self.end - (50))):    
                    self.boxes[1].draw()
    
    def run(self):
        while(self.running):
            self.clock.tick(self.fps)
            self.frame_path = os.path.join(f"../Art/{self.art_path}/{self.path}", self.frames[self.frame_index])
            self.frame = pygame.image.load(self.frame_path)
            self.screen.blit(self.frame, (0, 0))
            self.show_dialog() 
            pygame.display.flip()
            self.frame_index += 1 
            
            # Manejar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            #end of the animation
            if self.frame_index == self.end:
                pygame.time.wait(3000)
                self.running = False  
                   
       