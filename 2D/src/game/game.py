'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame,  utils.globals as globals, utils.auxiliar as auxiliar
from game.camera import Camera
from game.objects.lifes import Lifes
from game.base import Base


from ui.button import Button
vec = pygame.math.Vector2  

#Clase que define el juego en sí, con la escena, los sprites, la cámara, los botones y el jugador.
#Se encarga de gestionar los eventos, las colisiones y el renderizado de los elementos llamando a las funciones correspondientes
# de cada elemento.
class Game(Base):
    #region __init__
    def __init__(self, scene, sound ):
        """
        Inicializa la clase Game.

        Configura el entorno del juego, incluyendo la escena, el fondo, los grupos de sprites, la cámara, los botones, y el jugador.

        :param scene: La escena del juego (contiene plataformas, enemigos, etc.).
        :param sound: La música del juego.
        """
        super().__init__()   
        #cuando se trate del nivel en lugar de una escena se pasara la lista de escenas que debera gestionar los cambios de momento tiene una 
        self.scene = scene
        self.bg = pygame.image.load(auxiliar.get_path(f"{ globals.config.get_artpath()}/background/{self.scene.background}"))
        self.path = auxiliar.get_path( globals.config.get_artpath())
        self.sprites = pygame.sprite.Group()
        self.group_lifes = pygame.sprite.Group()
        self.in_scene = pygame.sprite.Group()
        self.in_scene_now = pygame.sprite.Group() #elemetos en escena ahora
        self.clock =  globals.game.get_clock()# utiliza el relog del config
        self.FPS =  globals.config.get_fps()
        self.world_width = self.bg.get_width()   # O la dimensión que abarque todo el escenario
        self.world_height = self.bg.get_height()   # O la altura máxima del escenario
        self.camera = Camera(self.world_width, self.world_height,self.screen_width, self.screen_height)
        self.sound = sound
        path_button =auxiliar.get_path( f"{ globals.config.get_artpath()}/avatar/pause_button.png")
        path_hover = auxiliar.get_path(f"{ globals.config.get_artpath()}/avatar/pause_button_hover.png")

        pauseb = Button(pos=(self.screen_width - 100, self.screen_height / 8), 
                text_input= globals.config.get_text_button(key ="PAUSE"),
                image_path = path_button,
                hover_image_path=path_hover
                )
        self.buttons = {
            "pause": pauseb
        } 
        self.player = globals.game.get_player()
        #grupo para jugador y enemigos
        self.sprites.add(self.player)
        self.sprites.add(self.scene.enemies)
        #grupo para elementos en escena para collisiones
        self.in_scene.add(self.scene.enemies)
        self.scene.it.add(self.player.get_group())
        self.in_scene.add(self.scene.it)
        self.in_scene.add(self.scene.platform)
        
        self.player.set_platform(self.scene.platform)
    #endregion
       
    
    #region handle_events
    #game loop se modificara si es necesario cuando se tengan los niveles
    def handle_events(self):
        """
        Maneja los eventos del juego.

        Procesa eventos de teclado y ratón, como salir del juego o activar la pausa.

        """
        if self.player.get_lifes() == 0:
            self.running = False
            globals.game.end_game()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttons["pause"].checkForInput(pygame.mouse.get_pos()):
                    self.buttons["pause"].make_sound()
                    globals.game.load_pause()
    #endregion
    
    #region update
    def update(self):    
        """
        Actualiza el estado del juego en cada ciclo.

        Llama a los métodos update de los objetos del juego, actualiza las vidas del jugador, actualiza la cámara y verifica los elementos en la pantalla.
        """    
            
        self.player.update()
        self.in_scene.update()
        # Capa informacion se actualiza
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons.values(): #carga botones
            btn.update(mouse_pos)
        self.group_lifes.empty()  # Limpia las vidas actuales antes de agregar las nuevas
        for i in range(self.player.get_lifes()): 
            self.group_lifes.add(Lifes( x = 50 + (i * 40), y = 50))#todo make dinamic
        self.camera.update(self.player)
        self.in_scene_now.empty()
        self.in_scene_now.add(self.camera.check_elements_on_screen(self.in_scene))
    #endregion
        
    #region collision
    def collision(self):
        """
        Gestiona las colisiones entre los objetos del juego.

        Llama al método collision_managment para sprites, para gestionar las colisiones.
        """
        for item in self.sprites:
            item.collision_managment(self.in_scene_now)
        self.in_scene_now.add(self.player) 
    #endregion
                
    #region render
    def render(self):
        """
        Dibuja todos los elementos en la pantalla.

        Dibuja el fondo, los elementos en la escena, las vidas y los botones.
        """
        # Dibujado: el fondo y cada objeto se dibujan desplazados
        self.screen.blit(self.bg, (-self.camera.offset.x, -self.camera.offset.y))
        #capa escenario se actualiza
        for item in self.in_scene_now: #carga plataformas
                item.draw(self.screen, self.camera.apply(item.rect).topleft)                
        for item in self.group_lifes:
            item.draw(self.screen) 
        for btn in self.buttons.values(): #carga botones
            btn.render(self.screen)
        
        #Muestra por pantalla
        pygame.display.flip()
    #endregion
    
    #region cleanup
    def cleanup(self):
        """
        Limpia los recursos del juego.

        Detiene el bucle del juego, libera la memoria de los objetos, para la recolección de basura
        """
        # Detener el bucle de juego
        self.running = False
        # Limpiar eventos pendientes
        pygame.event.clear()
        # Detener la música
        pygame.mixer.music.stop()
        pygame.mixer.stop()
        # Vaciar grupos de sprites
        self.sprites.empty()
        self.group_lifes.empty()
        self.in_scene.empty()
        self.in_scene_now.empty()
        # Limpiar referencias a objetos importantes
        self.player = None
        self.scene = None
        self.sound = None
        
        self.bg = None
        self.buttons.clear()
        # Forzar al recolector de basura a limpiar
        import gc
        gc.collect()
    #endregion
       
    #region run
    def run(self):
        """
        Ejecuta el bucle principal del juego.

        Inicia la música, establece la variable running a True y ejecuta el bucle principal del juego,
        llamando a los métodos handle_events, update, collision y render en cada ciclo.
        """
        globals.game.changeMusic(self.sound)    
        self.running = True
        while self.running:           
            self.clock.tick(self.FPS)  # indicamos el numero de frames por segundo
            self.handle_events()
            self.update()
            self.collision()
            self.render()
    #endregion