'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''
from game.configManager import ConfigManager
from game.gameManager import GameManager

class Base():
 
    def __init__(self):
        super().__init__()
        self.screen = GameManager().get_instance().screen
        self.screen_width = ConfigManager().get_instance().get_width()
        self.screen_height =  ConfigManager().get_instance().get_height()
        self.running = False
     
    def stop(self):
        self.running = False 
    
    def get_running(self):
        return self.running
         
    def cleanup(Self):
        pass
    
    def handle_events(self):
        pass
    
    def update(self):
        pass
    
    def render(self):
        pass
        
    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.render()