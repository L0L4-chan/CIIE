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
from game.lastevent import LastEvent
from game.configManager import ConfigManager
from game.objects.decor.platforms import Platforms
from game.objects.decor.breakable import Breakable
from game.objects.decor.spikes import Spikes
from game.objects.decor.switch import Switch
from game.objects.decor.chest import Chest
from enemies.devil import Devil
from enemies.bug import Bug
from enemies.ghost import Ghost
from enemies.bat import Bat
from enemies.boss import Boss




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
        
        if self.items.get("breakable"):
            for (x, y) in self.items["breakable"]:
                breakable = Breakable(x,y)
                self.sprites.add(breakable)
                
        if self.items.get("event"):
            for (x, y, h, w, path, lvl) in self.items["event"]:
                event = Event(x,y,h,w,path,lvl)
                self.sprites.add(event)
        
        if self.items.get("devil"):
            for (x,y) in self.items["devil"]:
                self.sprites.add(Devil(x,y))

        if self.items.get("bat"):
            for (x,y) in self.items["bat"]:
                self.sprites.add(Bat(x,y))
        
        if self.items.get("bug"):
            for (x,y) in self.items["bug"]:
                self.sprites.add(Bug(x,y))

        if self.items.get("ghost"):
            for (x,y) in self.items["ghost"]:
                self.sprites.add(Ghost(x,y))

        if self.items.get("boss"):
            for (x,y) in self.items["boss"]:
                self.sprites.add(Boss(x,y))
        
            