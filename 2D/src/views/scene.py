'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''
import pygame, utils.auxiliar as auxiliar
from game.event import Event
from game.configManager import ConfigManager
from game.objects.decor.platforms import Platforms
from game.objects.decor.spikes import Spikes
from game.objects.decor.switch import Switch
from game.objects.decor.chest import Chest


class Scene():
    def __init__(self, background,file):
        super().__init__() 
        self.background = background
        self.items = auxiliar.load_json(f"../Art/{ConfigManager().get_instance().get_artpath()}/levels/{ConfigManager().get_instance().get_difficulty()}/{file}")
        self.sprites = pygame.sprite.Group()
        self.create_scene()
        
    def create_scene(self):    
        if self.items.get("platform"):
            for (x, y, w, h) in self.items["platform"]:
                platform = Platforms(x, y, w, h)
                self.sprites.add(platform)
                
        if self.items.get("spikes"):
            for (x, y, w, h) in self.items["spikes"]:
                spikes = Spikes(x, y, w, h)
                self.sprites.add(spikes)
        
        if self.items.get("switch"):
            for (x, y, dx,dy) in self.items["switch"]:
                switch = Switch(x, y, dx,dy)
                self.sprites.add(switch)
                self.sprites.add(switch.get_door())
                
        if self.items.get("chest"):
            for (x, y, pz) in self.items["chest"]:
                chest = Chest(x,y,pz)
                self.sprites.add(chest)
                self.sprites.add(chest.get_prize())
                
        if self.items.get("event"):
            for (x, y, h, w, path, lvl) in self.items["event"]:
                event = Event(x,y,h,w,path,lvl)
                self.sprites.add(event)

                
        #todo chest and traps
        #if self.items["chest"]:
            