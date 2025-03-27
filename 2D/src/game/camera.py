'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame

class Camera:
    #region __init__
    def __init__(self, world_width, world_height, screen_width, screen_height):
        """
        Inicializa la clase Camera.

        Establece las dimensiones del mundo, la pantalla y calcula los márgenes de la cámara.

        :param world_width: Ancho del mundo.
        :param world_height: Alto del mundo.
        :param screen_width: Ancho de la pantalla.
        :param screen_height: Alto de la pantalla.
        """
        self.world_width = world_width
        self.world_height = world_height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = pygame.math.Vector2(0, 0)
        # Margenes en píxeles según los porcentajes:
        self.left_margin = screen_width * 0.35
        self.right_margin = screen_width * 0.35
        self.top_margin = screen_height * 0.35
        self.bottom_margin = screen_height * 0.15
    #endregion

    #region update
    def update(self, target):
        """
        Actualiza la posición de la cámara, siguiendo al objetivo.

        Calcula el desplazamiento necesario para centrar al objetivo, ajusta el offset de la cámara y asegura que no se salga de los límites del mundo.

        :param target: El objeto (usualmente el jugador) al que la cámara debe seguir.
        """
        # Posición del target en pantalla (en coordenadas del mundo menos el offset)
        player_screen_x = target.rect.centerx - self.offset.x
        player_screen_y = target.rect.centery - self.offset.y

        dx = 0
        dy = 0

        # Verificar si el jugador se acerca a la izquierda o derecha
        if player_screen_x < self.left_margin:
            dx = player_screen_x - self.left_margin
        elif player_screen_x > self.screen_width - self.right_margin:
            dx = player_screen_x - (self.screen_width - self.right_margin)

        # Verificar si el jugador se acerca a la parte superior o inferior
        if player_screen_y < self.top_margin:
            dy = player_screen_y - self.top_margin
        elif player_screen_y > self.screen_height - self.bottom_margin:
            dy = player_screen_y - (self.screen_height - self.bottom_margin)

        # Actualizar el offset de la cámara
        self.offset.x += dx
        self.offset.y += dy

        # Limitar el offset para que la cámara no muestre áreas fuera del mundo
        self.offset.x = max(0, min(self.offset.x, self.world_width - self.screen_width))
        self.offset.y = max(0, min(self.offset.y, self.world_height - self.screen_height))
    #endregion

    #region apply
    def apply(self, rect):
        """
        Aplica el offset de la cámara a un rectángulo.

        Mueve el rectángulo restando el offset de la cámara.

        :param rect: El rectángulo a mover.
        :return: El rectángulo movido.
        :rtype: pygame.Rect
        """
        return rect.move(-self.offset.x, -self.offset.y)
    #endregion

    #region check_elements_on_screen
    # Verificar si el rect del elemento está dentro de la vista de la cámara
    def check_elements_on_screen(self, elements):
        """
        Verifica si los elementos están dentro de la vista de la cámara.

        Itera sobre una lista de elementos, aplica el offset de la cámara a sus rectángulos y verifica si colisionan con la pantalla..
        Establece el atributo `on_screen` de cada elemento y retorna un grupo de sprites con los elementos visibles..

        :param elements: Lista de elementos (sprites) a verificar.
        :return: Un grupo de sprites que están en la pantalla.
        :rtype: pygame.sprite.Group
        """
        in_scene = pygame.sprite.Group()
        for element in elements:
            aux = self.apply(element.rect)
            if aux.colliderect(pygame.Rect(0,0, self.screen_width, self.screen_height)):
                element.on_screen = True
                in_scene.add(element)
            else:
                element.on_screen = False
        return in_scene
    #endregion