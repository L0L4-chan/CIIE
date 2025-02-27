'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''
import pygame, utils.auxiliar as auxiliar
from game.objects.decor.platforms import Platforms
from game.objects.decor.spikes import Spikes
from game.objects.decor.switch import Switch


class Scene():
    def __init__(self, background, pt_skin, file):
        super().__init__() 
        self.background = background
        self.pt_skin = pt_skin
        self.items = auxiliar.load_json(file)
        self.sprites = pygame.sprite.Group()
        self.create_scene()
        
    def create_scene(self):    
        if self.items["platform"]:
            for (x, y, w, h) in self.items["platform"]:
                platform = Platforms(x, y, w, h)
                self.sprites.add(platform)
                
        if self.items["spikes"]:
            for (x, y, w, h) in self.items["spikes"]:
                spikes = Spikes(x, y, w, h)
                self.sprites.add(spikes)
        
        if self.items["switch"]:
             for (x, y, dx,dy) in self.items["switch"]:
                switch = Switch(x, y, dx,dy)
                self.sprites.add(switch)
                self.sprites.add(switch.get_door())
                
       
                
        #todo chest and traps
        #if self.items["chest"]:
            