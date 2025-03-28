'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, os, utils.globals as globals, utils.auxiliar as auxiliar
from views.dialogBox import DialogBox

#Clase encargada de la reproducción de las animaciones
class AnimationPlayer():
    def __init__(self, path, start, amount, event):
        """
        Constructor de la clase AnimationPlayer.
        
        :param path: Ruta de la animación.
        :param start: Frame en el que se muestra el primer texto.
        :param amount: Cantidad de textos a mostrar.
        :param event: Número de evento.
        
        :return: None
        """
        super().__init__()
        self.screen = globals.game.screen
        self.clock =  globals.game.clock
        self.art_path =  globals.config.get_artpath()
        self.path = path
        self.frames = sorted(os.listdir(auxiliar.get_path(f"{self.art_path}/{path}")))
        self.frame_index = 0
        self.end = len(self.frames) 
        self.fps = 24
        self.running = True
        self.start = start # cuando sea mostrado el primer texto
        self.amount = amount
        self.get_boxes(event) # creamos los textos necesarios
    
    #Obtener los cuadros de diálogo
    def get_boxes(self, event):
       self.boxes = []
       for i in range(event, event + self.amount): 
           self.boxes.append(DialogBox(event = i))  # Pasamos el número actual del loop

    #Mostrar el diálogo
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
    
    #Ejecutar la animación
    def run(self):
        while(self.running):
            self.clock.tick(self.fps)
            self.frame_path = os.path.join(auxiliar.get_path(f"{self.art_path}/{self.path}"), self.frames[self.frame_index])
            self.frame = pygame.image.load(self.frame_path)
            self.screen.blit(self.frame, (0, 0))
            self.show_dialog() 
            pygame.display.flip()
            self.frame_index += 1 
            
            # Manejar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            #final de la animacion
            if self.frame_index == self.end:
                pygame.time.wait(3000) #esperamos 3 segundos para que se muestre las teclas funcionales
                self.running = False  
                   
       