'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame
from game.gameManager import GameManager
from game.configManager import ConfigManager
from game.objects.platforms import Platforms
from game.objects.lives import Lives
from game.base import Base
from ui.button import Button
from ui.pausa import Pausa
vec = pygame.math.Vector2  


class Game(Base):

    def __init__(self, scene = None, sound = None):
       super().__init__()   
       #cuando se trate del nivel en lugar de una escena se pasara la lista de escenas que debera gestionar los cambios de momento tiene una 
       self.scene = scene
       self.bg = pygame.image.load(f"../Art/{ConfigManager().get_instance().get_artpath()}/background/{self.scene.background}")
       self.sound = sound
       self.running = False
       self.sprites = pygame.sprite.Group()
       self.floor = pygame.sprite.Group()
       self.items = pygame.sprite.Group()
       self.group_lives = pygame.sprite.Group()
       self.clock =  GameManager().get_instance().clock
       self.FPS = ConfigManager().get_instance().get_fps()
       self.buttons = {
            "pause": Button(pos=(self.screen_width - 100, self.screen_height / 8), 
                text_input=ConfigManager().get_instance().get_text_button(key ="PAUSE")),

            "quit": Button(pos=(self.screen_width / 16, self.screen_height / 8), 
                text_input=ConfigManager().get_instance().get_text_button(key ="QUIT")),

        } 
       self.player = GameManager().get_instance().player
       self.enemy =GameManager().get_instance().enemy
       
       #generamos suelo (funcion que debera ser modificada cuando se tengan los niveles)
       self.generate_floor()
       #empieza la musica del nivel
       pygame.mixer.music.stop() #paramos la anterior
       pygame.mixer.music.load(self.sound)
       pygame.mixer.music.play(-1) #indicamos loop infinito

       self.sprites.add(self.player)
       self.sprites.add(self.enemy)
       
       self.run()
        
    #funcion de generación de suelo
    def generate_floor(self):
        platform_width = 80
        platform_height = 18
        num_platforms = self.screen_width // platform_width + 1
        floor_y = self.screen_height - 50 

        for i in range(num_platforms):
            platform = Platforms(i * platform_width, floor_y, platform_width, platform_height, self.scene.pt_skin)
            self.floor.add(platform)
            self.sprites.add(platform)
    
    #game loop se modificara si es necesario cuando se tengan los niveles
    def handle_events(self):
        if self.player.get_lives() == 0:
            GameManager().get_instance().end_game()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttons["pause"].checkForInput(pygame.mouse.get_pos()):
                    Pausa()
                if self.buttons["quit"].checkForInput(pygame.mouse.get_pos()):
                    self.running = False
                    GameManager().get_instance().running = False  
    
    def update(self):
        #capa escenario se actualiza
        for platform in self.floor: #carga plataformas
                platform.update(self.screen)
                    
        #Capa jugador se actualiza
        self.player.update(self.floor) #actualiza al player
        self.items = self.player.group  #añade piedras al grupo de piedras para su visualizacion
        self.items.update(self.sprites)
        self.enemy.update()
        
        # Capa informacion se actualiza
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons.values(): #carga botones
            btn.changeColor(mouse_pos)
        self.group_lives.empty()  # Limpia las vidas actuales antes de agregar las nuevas
        for i in range(self.player.get_lives()): 
            self.group_lives.add(Lives(path= "../Art/big/avatar/live.png", x = 400 + (i * 30), y = 50))#todo make dinamic
        
        
        
    def render(self):
        
        self.screen.blit(self.bg, (0,0)) #carga el fondo (en la escena completa el 0,0 tendra que varias con los movimientos del personaje TODO)
        self.screen.blit(self.player.surf, self.player.rect.topleft) #carga player
        self.screen.blit(self.enemy.surf, self.enemy.rect.topleft) # carga al enemigo 
        self.group_lives.update(self.screen)
        for btn in self.buttons.values(): #carga botones
            btn.render(self.screen)
        self.items.draw(self.screen)
        #Muestra por pantalla
        pygame.display.flip()
    
    def cleanup(self):
        # Detener la música
        pygame.mixer.music.stop()
        # Vaciar grupos de sprites
        self.sprites.empty()
        self.floor.empty()
        self.items.empty()
        self.group_lives.empty()
        # Limpiar referencias a objetos importantes
        self.player = None
        self.enemy = None
        self.scene = None
        self.sound = None
        # Detener el bucle de juego
        self.running = False
        # Limpiar eventos pendientes
        pygame.event.clear()
        self.bg = None
        self.buttons.clear()
        # Forzar al recolector de basura a limpiar
        import gc
        gc.collect()
    
       
    def run(self):    
        self.running = True
        while self.running:           
            self.clock.tick(self.FPS) # indicamos el numero de frames por segundo
            self.handle_events()
            self.update()
            self.render()

            
            
            
        
        


        