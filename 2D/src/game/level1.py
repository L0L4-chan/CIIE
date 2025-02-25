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
from ui.button import Button
from ui.pausa import Pausa

class Game():

    def __init__(self, scene=None, sound=None):
        # configuración de pantalla, textos, reloj y resolución
        self.gameManager = GameManager.get_instance()
        self.config = ConfigManager().get_instance()

        # lista de escenas que deberá gestionar los cambios, de momento tiene una
        self.scene = scene
        self.bg = pygame.image.load(f"../Art/{self.config.get_artpath()}/background/{self.scene.background}")
        self.sound = sound
        self.running = False

        # Carga de grupos para plataformas, sprites, elementos...
        self.sprites = pygame.sprite.Group()
        self.floor = pygame.sprite.Group()
        self.stones = pygame.sprite.Group()

        # Nueva variable para controlar el desplazamiento de la cámara
        self.camera_x = 0

        # Se generan las plataformas
        self.generate_floor()

        self.buttons = {
            "pause": Button(pos=(self.config.get_width() - 100, self.config.get_height() / 8),
                            text_input=self.config.get_text_button(key="PAUSE")),

            "quit": Button(pos=(self.config.get_width() / 16, self.config.get_height() / 8),
                           text_input=self.config.get_text_button(key="QUIT")),
        }

        # Empieza la música del nivel
        pygame.mixer.music.stop()  # Paramos la anterior
        pygame.mixer.music.load(self.sound)
        pygame.mixer.music.play(-1)  # Loop infinito

        self.sprites.add(self.gameManager.player)
        self.sprites.add(self.gameManager.enemy)

    def generate_floor(self):
        platform_width = 80
        platform_height = 18
        platform_width_wall = 30
        platform_height_wall = 200
        floor_y = self.config.get_height() - 50  # nivel base del suelo
        start_x = 0  # posición inicial en X

        # ---------------------------------------------------------
        # Segmento 1: Muro inicial (bloquea la salida por la izquierda)
        wall_x = start_x
        for i in range(10):  # Muro de 10 bloques de altura
            platform = Platforms(wall_x, floor_y - (i * platform_height_wall),
                                platform_width_wall, int(platform_height_wall * 1.2),
                                self.scene.pt_skin)
            platform.original_x = platform.rect.x
            # Ajustar la hitbox para colisión
            platform.rect = pygame.Rect(platform.rect.x, platform.rect.y, platform_width_wall, platform_height)
            self.floor.add(platform)
            self.sprites.add(platform)

        # ---------------------------------------------------------
        # Segmento 2: 12 plataformas de suelo (camino horizontal)
        for i in range(12):
            platform = Platforms(start_x + (i * platform_width), floor_y,
                                platform_width, platform_height, self.scene.pt_skin)
            platform.original_x = platform.rect.x
            self.floor.add(platform)
            self.sprites.add(platform)

        # Hueco de 2 plataformas
        start_x += (12 + 2) * platform_width

        # ---------------------------------------------------------
        # Segmento 3: 8 plataformas de suelo tras el hueco
        for i in range(8):
            platform = Platforms(start_x + (i * platform_width), floor_y,
                                platform_width, platform_height, self.scene.pt_skin)
            platform.original_x = platform.rect.x
            self.floor.add(platform)
            self.sprites.add(platform)

        # ---------------------------------------------------------
        # Segmento 4: Escalera de 5 peldaños con fondo de muro
        start_x += 8 * platform_width
        for i in range(5):
            # Peldaño
            step_y = floor_y - ((i + 1) * platform_height * 3)
            platform = Platforms(start_x + (i * platform_width), step_y,
                                platform_width * (5 - i) * 1.02, platform_height, self.scene.pt_skin)
            platform.original_x = platform.rect.x
            self.floor.add(platform)
            self.sprites.add(platform)
            # Fondo: 2 bloques de muro debajo del peldaño
            for j in range(2):
                wall_y = step_y + ((j + 1) * platform_height)
                wall_block = Platforms(start_x + (i * platform_width), wall_y,
                                    platform_width * (5 - i) * 1.02, platform_height, self.scene.pt_skin)
                wall_block.original_x = wall_block.rect.x
                self.floor.add(wall_block)
                self.sprites.add(wall_block)

        # ---------------------------------------------------------
        # Segmento 5: Muro final de la sección de escaleras
        wall_x = start_x + (5 * platform_width)
        for i in range(16):
            platform = Platforms(wall_x, floor_y - (i * platform_height),
                                platform_width_wall, platform_height, self.scene.pt_skin)
            platform.original_x = platform.rect.x
            self.floor.add(platform)
            self.sprites.add(platform)

        # ---------------------------------------------------------
        # Segmento 6: 25 plataformas en línea recta
        start_x += 5 * platform_width
        for i in range(25):
            platform = Platforms(start_x + (i * platform_width), floor_y,
                                platform_width, platform_height, self.scene.pt_skin)
            platform.original_x = platform.rect.x
            self.floor.add(platform)
            self.sprites.add(platform)

        # Hueco de 2 plataformas
        start_x += (25 + 2) * platform_width

        # ---------------------------------------------------------
        # Segmento 7: 6 plataformas tras el hueco (antes del último hueco)
        for i in range(6):
            platform = Platforms(start_x + (i * platform_width), floor_y,
                                platform_width, platform_height, self.scene.pt_skin)
            platform.original_x = platform.rect.x
            self.floor.add(platform)
            self.sprites.add(platform)

        # ---------------------------------------------------------
        # Ahora, en lugar del "hueco de 6 plataformas" original, modificamos la sección:
        # Segmento X: Caída vertical de 8 bloques de muro
        for i in range(8):
            drop_block = Platforms(start_x, floor_y + (i * platform_height_wall),
                                platform_width_wall, platform_height_wall, self.scene.pt_skin)
            drop_block.original_x = drop_block.rect.x
            self.floor.add(drop_block)
            self.sprites.add(drop_block)
        new_floor_y = floor_y + 8 * platform_height_wall

        # Segmento Y: Línea de 15 plataformas de suelo (avance hacia la izquierda)
        for i in range(15):
            platform = Platforms(start_x - (i * platform_width), new_floor_y,
                                platform_width, platform_height, self.scene.pt_skin)
            platform.original_x = platform.rect.x
            self.floor.add(platform)
            self.sprites.add(platform)
        # Actualizamos start_x al extremo izquierdo de esta línea:
        start_x = start_x - (15 - 1) * platform_width

        # Segmento Z: Hueco de 4 plataformas con "fondo"
        # Generamos un hueco, colocando dos bloques de muro en cada borde del hueco.
        gap_start_x = start_x  # lado derecho del hueco
        # Muro derecho del hueco
        for i in range(2):
            wall_block = Platforms(gap_start_x, new_floor_y - (i * platform_height_wall),
                                platform_width_wall, platform_height_wall, self.scene.pt_skin)
            wall_block.original_x = wall_block.rect.x
            self.floor.add(wall_block)
            self.sprites.add(wall_block)
        # Saltamos 4 plataformas de ancho para el hueco
        gap_end_x = gap_start_x - (4 * platform_width)
        # Muro izquierdo del hueco
        for i in range(2):
            wall_block = Platforms(gap_end_x, new_floor_y - (i * platform_height_wall),
                                platform_width_wall, platform_height_wall, self.scene.pt_skin)
            wall_block.original_x = wall_block.rect.x
            self.floor.add(wall_block)
            self.sprites.add(wall_block)

        # Segmento W: 5 plataformas más de suelo tras el hueco
        for i in range(5):
            platform = Platforms(gap_end_x - (i * platform_width), new_floor_y,
                                platform_width, platform_height, self.scene.pt_skin)
            platform.original_x = platform.rect.x
            self.floor.add(platform)
            self.sprites.add(platform)
        # Actualizamos start_x al extremo izquierdo de esta nueva sección:
        start_x = gap_end_x - (5 - 1) * platform_width

        # ---------------------------------------------------------
        # Segmento V: Habitación grande con techo alto
        # Definimos el techo a una altura considerable por encima del suelo actual
        room_ceiling_y = new_floor_y - (8 * platform_height)
        for i in range(12):
            platform = Platforms(start_x - (i * platform_width), room_ceiling_y,
                                platform_width, platform_height, self.scene.pt_skin)
            platform.original_x = platform.rect.x
            self.floor.add(platform)
            self.sprites.add(platform)

        # ---------------------------------------------------------
        # Segmento U: Bajar el techo y crear un camino de 6 plataformas
        room_floor_y = room_ceiling_y + platform_height_wall
        for i in range(6):
            platform = Platforms(start_x - (12 * platform_width) - (i * platform_width), room_floor_y,
                                platform_width, platform_height, self.scene.pt_skin)
            platform.original_x = platform.rect.x
            self.floor.add(platform)
            self.sprites.add(platform)

        # ---------------------------------------------------------
        # Segmento T: Otra caída vertical, de 6 bloques de muro (como la anterior)
        drop2_x = start_x - (12 * platform_width) - (6 * platform_width)
        for i in range(6):
            drop_block = Platforms(drop2_x, room_floor_y + (i * platform_height_wall),
                                platform_width_wall, platform_height_wall, self.scene.pt_skin)
            drop_block.original_x = drop_block.rect.x
            self.floor.add(drop_block)
            self.sprites.add(drop_block)
        new_floor_y2 = room_floor_y + 6 * platform_height_wall

        # ---------------------------------------------------------
        # Segmento S: Generar plataformas hacia la derecha hasta alcanzar el muro
        # (usamos un objetivo arbitrario basado en la primera caída)
        final_wall_x = drop2_x + (10 * platform_width)
        current_x = drop2_x
        while current_x < final_wall_x:
            platform = Platforms(current_x, new_floor_y2,
                                platform_width, platform_height, self.scene.pt_skin)
            platform.original_x = platform.rect.x
            self.floor.add(platform)
            self.sprites.add(platform)
            current_x += platform_width

        # ---------------------------------------------------------
        # Segmento R: Ascenso con plataformas para subir a lo alto del muro
        ascend_start_x = final_wall_x
        ascend_start_y = new_floor_y2
        for i in range(4):
            platform = Platforms(ascend_start_x + (i * platform_width),
                                ascend_start_y - (i * platform_height * 2),
                                platform_width, platform_height, self.scene.pt_skin)
            platform.original_x = platform.rect.x
            self.floor.add(platform)
            self.sprites.add(platform)

        # Colocar al jugador en la primera plataforma (como referencia inicial)
        first_platform = list(self.floor)[6]
        self.gameManager.player.rect.x = first_platform.rect.x
        self.gameManager.player.rect.y = first_platform.rect.y - self.gameManager.player.rect.height

    def run(self):
        self.running = True

        while self.running:
            self.gameManager.clock.tick(self.config.get_fps())

            # Manejo de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.buttons["pause"].checkForInput(pygame.mouse.get_pos()):
                        Pausa(self.gameManager.screen)
                    if self.buttons["quit"].checkForInput(pygame.mouse.get_pos()):
                        self.running = False

            # 📌 ACTUALIZAR LA POSICIÓN DE LA CÁMARA BASADO EN EL JUGADOR
            player_x = self.gameManager.player.rect.centerx
            screen_center = self.config.get_width() // 2

            if player_x > screen_center:
                self.camera_x += min((player_x - screen_center) * 0.05, 5)  # Limitar el desplazamiento

            # Dibujar el fondo de forma estática
            self.gameManager.screen.blit(self.bg, (0, 0))

            # Dibujar botones
            for btn in self.buttons.values():
                btn.render(self.gameManager.screen)

            # Dibujar plataformas
            for platform in self.floor:
                platform.rect.x = platform.original_x - self.camera_x
                platform.update(self.gameManager.screen)

            # Dibujar jugador
            self.gameManager.player.update(self.floor, self.gameManager.screen)
            self.gameManager.screen.blit(self.gameManager.player.surf, (
                self.gameManager.player.rect.x - self.camera_x, self.gameManager.player.rect.y))

            pygame.display.flip()

        self.gameManager.running = False

    def Camera():
        def __init__(self, game, width, height):
            self.game = game
            self.width = width
            self. height = height
            self.camera = pg.Rect(0, 0, width, height)

        def update (self, target):
            x = int(self.game.width/2) - target.rect.centerx
