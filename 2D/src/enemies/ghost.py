'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''
import pygame, random,   utils.globals as globals, utils.auxiliar as auxiliar

from classes.enemy import Enemy

vec = pygame.math.Vector2 #2 for two dimensional

class Ghost(Enemy):
    
    def __init__(self, x, y):
        self.spritesheet = pygame.image.load(auxiliar.get_path(f"{ globals.config.get_artpath()}/ghost/sprite_sheet.png"))
        super().__init__(x,y, (self.spritesheet.get_width() / 5), self.spritesheet.get_height(), False )
        
        self.vel = vec(globals.config.get_player_Acc()*2 , 0)  # Velocidad inicial para moverse hacia la derecha
        self.speed = globals.config.get_player_Acc() 
        self.frames = {
            "idle": [(0, 0)],
            "walk": [(i * self.width, 0) for i in range(2)],
            "death": [((self.width * 2) + (i * self.width), 0) for i in range(3)]
        }

    #region move
    def move(self):
        """
        Gestiona el movimiento del fantasma.

        Determina la dirección horizontal basándose en la posición del objetivo y se mueve en horizontal,
        también añade movimiento vertical aleatorio y actualiza la posición del rectángulo.

        :return: None
        """
        self.set_objective()
        distance_x = self.objective[0] - self.rect.x
        if distance_x < 0:
            self.direction = -1
        else:
            self.direction = 1
            
        if abs(distance_x) < self.screen_width/3 or abs(distance_x) >  self.screen_width/32:
            self.vel.x = self.direction * self.speed
        
        # añadir movimiento de subida y bajada
        random_y_adjustment = random.randint(-2, 2)
        self.vel.y =  random_y_adjustment * self.speed
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        
        self.update_rect()
    #endregion