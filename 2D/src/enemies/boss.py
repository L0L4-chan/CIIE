import pygame,  random
from classes.enemy import Enemy
from game.configManager import ConfigManager
from game.gameManager import GameManager
from game.objects.stone import Stone
from game.objects.fireball import Fireball
vec = pygame.math.Vector2 #2 for two dimensional



class Boss(Enemy):
    def __init__(self, x, y):
        self.spritesheet = pygame.image.load(f"../Art/{ConfigManager().get_instance().get_artpath()}/boss/sprite_sheet.png")
        super().__init__(x, y, (self.spritesheet.get_width() / 11), self.spritesheet.get_height(), False)
        self.pos = vec(x, y)
        self.vel = vec(0, 0)  # Velocidad inicial para moverse hacia la derecha
        self.speed = 0.5   
        self.special_timer = 300
        self.attack = 3600
        self.frame_rate = 16
        self.frames = {
            "idle": [(self.width*4, 0)],
            "walk": [(i * self.width, 0) for i in range(2)],
            "melee":  [((self.width * 2 )+(i * self.width), 0) for i in range(2)],
            "magic": [((self.width * 5 )+(i * self.width), 0) for i in range(4)],
            "death": [((self.width * 9 )+(i * self.width), 0) for i in range(2)]
        }
        self.sound = pygame.mixer.Sound("../Sound/FX/win.wav")
        self.lifes = 3
        for i in range(5):
            self.group.add(Fireball())

    def move(self):
        self.set_objective(GameManager.get_instance().player.rect.bottomleft)
        distance_x = self.objective[0] - self.rect.x
        if distance_x < 0:
            self.direction = -1
        else:
            self.direction = 1
        # Si el jefe está en estado especial, no se mueve hasta que pase el tiempo
        if  self.current_action == "magic":
            self.special_timer -= 1
            if self.special_timer <= 0:
                self.current_action = "walk" 
            if self.special_timer % 6 ==0:
                self.magic_attack() 
             
        elif abs(distance_x) < 400 and self.lifes < 15 and self.attack <= 0:
            self.current_action = "magic"
            self.magic_attack()
            self.special_timer = 300
        else:
            self.vel.x = self.speed * self.direction
            self.pos.x += self.vel.x
            self.update_rect()
            if abs(distance_x) < 100:
                self.current_action = "melee"
            else:
                self.current_action = "walk"    
                
    def render(self):
        action_frames = self.frames[self.current_action]
        if self.index > len(action_frames)-1:
            self.index = 0
        frame = action_frames[self.index]
        sprite_image = self.spritesheet.subsurface(pygame.Rect(frame[0], frame[1], self.width, self.height))
        if self.direction < 0:
            sprite_image = pygame.transform.flip(sprite_image, True, False)
        self.surf = sprite_image
        self.animation_timer = 0  
        self.index += 1
                
    def magic_attack(self):
        for item in self.group:
            if not item.get_inUse():
                random_x = random.randint(self.rect.x - 500, self.rect.x + 500)
                item.active(random_x, self.height*3, 1)
                break
            
    def update(self):
        self.attack -= 1
        self.animation_timer += 1
        self.move()
 
    def draw(self, screen= None, position = None):
        if self.animation_timer > self.frame_rate:
            self.render()
        screen.blit(self.surf,position)    
        
    def die(self):
        if not self.hit:
            self.hit = True
            self.wounded()
                                       
    def wounded(self):
        self.lifes -= 1
        print(self.lifes)
        if self.lifes<= 0:
            self.sound.play()
            GameManager().get_instance().scene.running= False
            GameManager().get_instance().load_start("st5.json")
        else:
            #self.rect.move(0,30)
            self.hit = False