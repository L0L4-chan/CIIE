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
from game.camera import Camera
from game.objects.lifes import Lifes
from game.base import Base
from classes.enemy import Enemy
from enemies.devil import Devil

from ui.button import Button
vec = pygame.math.Vector2  


class Game(Base):

    def __init__(self, scene = None, sound = None):
        super().__init__()   
        #cuando se trate del nivel en lugar de una escena se pasara la lista de escenas que debera gestionar los cambios de momento tiene una 
        self.scene = scene
        self.bg = pygame.image.load(f"../Art/{ConfigManager().get_instance().get_artpath()}/background/{self.scene.background}")
        self.sound = sound
        self.path = ConfigManager().get_instance().get_artpath()
        self.sprites = pygame.sprite.Group()
        self.floor = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.group_lives = pygame.sprite.Group()
        self.clock =  GameManager().get_instance().clock
        self.FPS = ConfigManager().get_instance().get_fps()
        self.world_width = self.bg.get_width()   # O la dimensión que abarque todo el escenario
        self.world_height = self.bg.get_height()   # O la altura máxima del escenario
        self.camera = Camera(self.world_width, self.world_height,self.screen_width, self.screen_height)
        path_button = f"../Art/{ConfigManager().get_instance().get_artpath()}/avatar/pause_button.png"
        path_hover = f"../Art/{ConfigManager().get_instance().get_artpath()}/avatar/pause_button_hover.png"

        pauseb = Button(pos=(self.screen_width - 100, self.screen_height / 8), 
                text_input=ConfigManager().get_instance().get_text_button(key ="PAUSE"),
                image_path = path_button,
                hover_image_path=path_hover
                )
        self.buttons = {
            "pause": pauseb
        } 
        self.player = GameManager().get_instance().player
        self.enemies=[]
        for sprite in self.scene.sprites:
            if isinstance(sprite, Enemy):
                self.enemies.append(sprite)
                self.scene.sprites.remove(sprite)

        #empieza la musica del nivel
        #pygame.mixer.music.stop() #paramos la anterior
        #pygame.mixer.music.load(self.sound)
        #pygame.mixer.music.play(-1) #indicamos loop infinito   
        self.sprites.add(self.player)

        self.floor = self.scene.sprites
        self.sprites.add(self.floor)

    
    #game loop se modificara si es necesario cuando se tengan los niveles
    def handle_events(self):
        if self.player.get_lifes() == 0:
            self.running = False
            GameManager().get_instance().end_game()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttons["pause"].checkForInput(pygame.mouse.get_pos()):
                    GameManager().get_instance().load_pause()
    
    def update(self):       
        #Capa jugador se actualiza
        self.player.update(self.floor) #actualiza al player
        self.items = self.player.group  #añade piedras al grupo de piedras para su visualizacion
        self.items.update(self.sprites)
        for enemy in self.enemies:
            enemy.update()

        self.floor.update()
        # Capa informacion se actualiza
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons.values(): #carga botones
            btn.changeColor(mouse_pos)
        self.group_lives.empty()  # Limpia las vidas actuales antes de agregar las nuevas
        for i in range(self.player.get_lifes()): 
            self.group_lives.add(Lifes( x = 50 + (i * 30), y = 50))#todo make dinamic
        self.camera.update(self.player)
        self.camera.check_elements_on_screen(self.floor)
                
    def render(self):
        # Dibujado: el fondo y cada objeto se dibujan desplazados
        self.screen.blit(self.bg, (-self.camera.offset.x, -self.camera.offset.y))
        #capa escenario se actualiza
        for platform in self.floor: #carga plataformas
            if platform.on_screen:
                platform.draw(self.screen, self.camera.apply(platform.rect).topleft)        
        self.screen.blit(self.player.surf, self.camera.apply(self.player.rect).topleft)
        
        for enemy in self.enemies:
            #if enemy.on_screen:
            self.screen.blit(enemy.surf, self.camera.apply(enemy.rect).topleft)
        
        for item in self.items:
            item.draw(screen = self.screen, position = self.camera.apply(item.rect).topleft)           
        
        for item in self.group_lives:
            item.draw(self.screen)
        
        for btn in self.buttons.values(): #carga botones
            btn.render(self.screen)
        
        #Muestra por pantalla
        pygame.display.flip()
    
    def cleanup(self):
        # Detener el bucle de juego
        self.running = False
        # Limpiar eventos pendientes
        pygame.event.clear()
        # Detener la música
        #pygame.mixer.music.stop()
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

            
            
            
        
        


        