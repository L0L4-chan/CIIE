'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''
import  utils.globals as globals

class Base():
 
    def __init__(self):
        super().__init__()
        self.screen = globals.game.screen
        self.screen_width =  globals.config.get_width()
        self.screen_height =   globals.config.get_height()
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