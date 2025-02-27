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
from game.objects.spikes import Spikes
from objects.lifes import Lives
from ui.button import Button
from ui.pausa import Pausa
from game.camera import Camera
vec = pygame.math.Vector2  


class Level1():

    def __init__(self, scene = None, sound = None):      
       #cuando se trate del nivel en lugar de una escena se pasara la lista de escenas que debera gestionar los cambios de momento tiene una 
       self.scene = scene
       self.bg = pygame.image.load(f"../Art/{ConfigManager().get_instance().get_artpath()}/background/{self.scene.background}")
       self.sound = sound
       self.running = False
       self.sprites = pygame.sprite.Group()
       self.floor = pygame.sprite.Group()
       self.stones = pygame.sprite.Group()
       self.group_lives = pygame.sprite.Group()
       self.world_width = 5120   # O la dimensión que abarque todo el escenario
       self.world_height = 2160  # O la altura máxima del escenario
       self.camera = Camera(self.world_width, self.world_height,
                            ConfigManager().get_instance().get_width(),
                            ConfigManager().get_instance().get_height())

       #generamos suelo (funcion que debera ser modificada cuando se tengan los niveles)
       self.generate_floor()
       
       self.buttons = {
            "pause": Button(pos=(ConfigManager().get_instance().get_width() - 100, ConfigManager().get_instance().get_height() / 8), 
                text_input=ConfigManager().get_instance().get_text_button(key ="PAUSE")),

            "quit": Button(pos=(ConfigManager().get_instance().get_width()/ 16, ConfigManager().get_instance().get_height() / 8), 
                text_input=ConfigManager().get_instance().get_text_button(key ="QUIT")),

        }
       #empieza la musica del nivel
       pygame.mixer.music.stop() #paramos la anterior
       pygame.mixer.music.load(self.sound)
       pygame.mixer.music.play(-1) #indicamos loop infinito

       self.sprites.add(GameManager().get_instance().player)
       self.sprites.add(GameManager().get_instance().enemy)
        
    #funcion de generación de suelo
    def generate_floor(self):
        """
        Genera plataformas de suelo (rojo) y de pinchos (verde)
        a partir de las coordenadas que has proporcionado.
        """

        # ----------------------------
        # BLOQUES ROJOS (SUELO)
        # Formato: (x, y, width, height)
        # ----------------------------
        platforms_floor_rects = [
            (0,    507,  745, 175),   # Bloque 1
            (1041, 507,  484, 175),   # Bloque 3
            (1655, 507,  423, 175),   # Bloque 5
            (2206, 507,  599, 175),   # Bloque 6
            (2806,   0,  123, 1522),  # Bloque 7
            (1844, 1228, 961, 192),   # Bloque 8
            (546,  1228, 1040, 192),  # Bloque 10
            (0,    1918, 808, 240),   # Bloque 11
            (1437, 1918, 448, 240),   # Bloque 13
            (2516, 1815, 984, 343),   # Bloque 15
            (3501, 507,  1618, 1651), # Bloque 16
            (3300, 1300, 200, 50),    # Bloque 17
            (2930, 800,  200, 50),    # Bloque 18
            (0,    0,    20,  2158),  # Bloque 19
            (5100, 0,    19,  2158)   # Bloque 20
        ]

        # ----------------------------
        # BLOQUES VERDES (PINCHOS)
        # ----------------------------
        platforms_spikes_rects = [
            (746,  607, 294, 75),   # Bloque 2
            (1526, 607, 128, 75),   # Bloque 4
            (1587, 1328, 256, 92),  # Bloque 9
            (809,  2018, 627, 140),  # Bloque 12
            (1886, 2018, 629, 140)   # Bloque 14
        ]

        # ----------------------------
        # CREACIÓN DE BLOQUES DE SUELO (invisibles)
        # ----------------------------
        for (x, y, w, h) in platforms_floor_rects:
            platform = Platforms(x, y, w, h, self.scene.pt_skin)
            self.floor.add(platform)
            self.sprites.add(platform)

        # ----------------------------
        # CREACIÓN DE BLOQUES DE PINCHOS (visibles)
        # ----------------------------
        for (x, y, w, h) in platforms_spikes_rects:
            spike = Spikes(x, y, w, h, self.scene.pt_skin)
            self.floor.add(spike)
            self.sprites.add(spike)
    
    def run(self):
        
        self.running = True
        screen = GameManager().get_instance().screen
 
        while self.running:
            
            GameManager().get_instance().clock.tick(ConfigManager().get_instance().get_fps()) # indicamos el numero de frames por segundo

            if GameManager().get_instance().player.get_lives() == 0:
                GameManager().get_instance().end_game()

            # Se manejan los eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.buttons["pause"].checkForInput(pygame.mouse.get_pos()):
                        #todo menu pausa 
                        Pausa(GameManager().get_instance().screen)
                    if self.buttons["quit"].checkForInput(pygame.mouse.get_pos()):
                        self.running = False    

                
            
            GameManager().get_instance().player.update(self.floor) #actualiza al player
            self.stones = GameManager().get_instance().player.group  #añade piedras al grupo de piedras para su visualizacion
            GameManager().get_instance().enemy.move() #actualiza al enemigo
            
            # Actualizamos la cámara usando el jugador como target
            self.camera.update(GameManager().get_instance().player)

            # Dibujado: el fondo y cada objeto se dibujan desplazados
            screen.blit(self.bg, (-self.camera.offset.x, -self.camera.offset.y))
            
            for btn in self.buttons.values(): #carga botones
                btn.update(GameManager().get_instance().screen)
            
            for i in range(GameManager().get_instance().player.get_lives()): 
                self.group_lives.add(Lives(path= "../Art/big/avatar/live.png", x = 400 + (i * 30), y = 50))#todo make dinamic

            self.group_lives.update(GameManager().get_instance().screen)
            
            for platform in self.floor: #carga plataformas
                platform.update(GameManager().get_instance().screen)
            
            for stn in self.stones: #carga piedrass
                stn.update(GameManager().get_instance().screen, self.sprites)
            
            screen.blit(GameManager().get_instance().player.surf, self.camera.apply(GameManager().get_instance().player.rect))
            screen.blit(GameManager().get_instance().enemy.surf, self.camera.apply(GameManager().get_instance().enemy.rect))
            
            # Otros elementos (vidas, etc.)
            self.group_lives.update(screen)
            
            #Muestra por pantalla
            pygame.display.flip()
        
        #maneja la salida y cierre para que todos los bucles finalicen correctamente
        GameManager().get_instance().running = False


        