'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''
import pygame, utils.auxiliar as auxiliar, utils.globals as globals
from game.objects.decor.event import Event
from game.objects.decor.platforms import Platforms
from game.objects.decor.breakable import Breakable
from game.objects.decor.spikes import Spikes
from game.objects.decor.switch import Switch
from game.objects.decor.chest import Chest
from enemies.devil import Devil
from enemies.ghost import Ghost
from enemies.bat import Bat
from enemies.boss import Boss




class Scene():
    def __init__(self, background,file):
        super().__init__() 
        self.background = background
        self.items = auxiliar.load_json(auxiliar.get_path(f"../Art/{ globals.config.get_artpath()}/levels/{ globals.config.get_difficulty()}/{file}"))
        self.platform = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.it = pygame.sprite.Group()
  
        self.create_scene()
        
    def create_scene(self):    
        if self.items.get("platform"):
            for (x, y, w, h) in self.items["platform"]:
                platform = Platforms(x, y, w, h)
                self.platform.add(platform)
                
        if self.items.get("spikes"):
            for (x, y, w, h) in self.items["spikes"]:
                spikes = Spikes(x, y, w, h)
                self.platform.add(spikes)
        
        if self.items.get("switch"):
            for (x, y, dx,dy) in self.items["switch"]:
                switch = Switch(x, y, dx,dy)
                self.platform.add(switch)
                self.platform.add(switch.get_door())
                
        if self.items.get("chest"):
            for (x, y, pz) in self.items["chest"]:
                chest = Chest(x,y,pz)
                self.it.add(chest)
                self.it.add(chest.get_prize())
        
        if self.items.get("breakable"):
            for (x, y) in self.items["breakable"]:
                breakable = Breakable(x,y)
                self.platform.add(breakable)
                
        if self.items.get("event"):
            for (x, y, h, w, path, lvl) in self.items["event"]:
                event = Event(x,y,h,w,path,lvl)
                self.platform.add(event)
        
        if self.items.get("devil"):
            for (x,y) in self.items["devil"]:
                devil = Devil(x,y)
                self.enemies.add(devil)
  
                self.it.add(devil.projectiles)

        if self.items.get("bat"):
            for (x,y) in self.items["bat"]:
        
                self.enemies.add(Bat(x,y))

        if self.items.get("ghost"):
            for (x,y) in self.items["ghost"]:
               
                self.enemies.add(Ghost(x,y))

        if self.items.get("boss"):
            for (x,y) in self.items["boss"]:
        
                boss = Boss(x,y)
                self.enemies.add(boss)
                self.it.add(boss.group)
     