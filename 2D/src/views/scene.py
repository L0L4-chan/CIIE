'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''
import pygame, utils.auxiliar as auxiliar
from game.objects.decor.event import Event
from game.lastevent import LastEvent
from game.configManager import ConfigManager
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
        self.items = auxiliar.load_json(f"../Art/{ConfigManager().get_instance().get_artpath()}/levels/{ConfigManager().get_instance().get_difficulty()}/{file}")
        self.platform = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.it = pygame.sprite.Group()
        self.chest = 0
        self.num_enemies=0
        self.chest_list = []
        self.enemy_list = []
        self.chestgroup = pygame.sprite.Group()
        self.respawn_timer = {}
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
                self.chest +=1
                self.chest_list.append((x,y,pz))
        
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
                self.num_enemies +=1
                self.it.add(devil.projectiles)

        if self.items.get("bat"):
            for (x,y) in self.items["bat"]:
                self.num_enemies +=1
                self.enemies.add(Bat(x,y))

        if self.items.get("ghost"):
            for (x,y) in self.items["ghost"]:
                self.num_enemies +=1
                self.enemies.add(Ghost(x,y))

        if self.items.get("boss"):
            for (x,y) in self.items["boss"]:
                self.num_enemies +=1
                boss = Boss(x,y)
                self.enemies.add(boss)
                self.it.add(boss.group)
        
    
    def spawn_chest(self, x, y):
        chest = Chest(x, y, "lungs")
        self.chestgroup.add(chest)
        self.it.add(chest.get_prize())
        
    def update(self):
        self.check_chest()     
        
    def check_chest(self):
        if len(self.chestgroup) == self.chest:
            return
        current_chests = [(chest.rect.x, chest.rect.y) for chest in self.chestgroup]
        missing_chests = [(x, y, pz) for (x, y, pz) in self.chest_list if (x, y) not in current_chests]

        for x, y, pz in missing_chests:
            pos = (x, y)
            if pos not in self.respawn_timer:
                self.respawn_timer[pos] = pygame.time.get_ticks() + 60000

        current_time = pygame.time.get_ticks()
        for pos, respawn_time in list(self.respawn_timer.items()):
            if current_time >= respawn_time:
                x, y, pz = next((cx, cy, cpz) for cx, cy, cpz in self.chest_list if (cx, cy) == pos)
                self.spawn_chest(x, y)
                del self.respawn_timer[pos]