from PIL import Image, ImageTk
from play_sound import play_sound
import time

class Player:
    def __init__(self, GAME_BASE_LAYER, GAME_SPEED, score_speed):
        self.color = 'green'
        self.GAME_BASE_LAYER = GAME_BASE_LAYER
        self.y = self.GAME_BASE_LAYER
        self.x = 200
        self.size = 50

        self.gravity = 5*GAME_SPEED+score_speed
        self.jump_height = 150
        self.jump_speed = 10*GAME_SPEED+score_speed
        self.is_jumping = False
        self.jump_count = 0
        self.jumped = False

        self.surface = False
        self.surface_sound = False
        Player.on_surface(self)
        self.is_sneaking = 0
        self.alive = True
        self.state = 'walk'
        self.skin_list = []
        self.start_time = time.time()

        self.skin = ImageTk.PhotoImage(Image.open(f"Slime Adventure/images/slime/{self.color}/walk/1.png").resize((self.size, self.size), Image.LANCZOS))
    
    def change_color(self, color):
        self.color = color
        print('changed to :', self.color)
        self.state = ''
        self.update_skins()

    def update_skins(self, tick_image):
        end_time = time.time()
        if not self.skin_list:
            self.skin_list = [ImageTk.PhotoImage(Image.open(f"Slime Adventure/images/slime/{self.color}/{self.state}/{i}.png").resize((self.size, self.size), Image.LANCZOS)) for i in range(1, 3)]
        self.skin = self.skin_list[tick_image-1]

    def dead(self, cactus_list):
        for cactus in cactus_list:
            if any(item in [i for i in range(self.x, self.x+self.size)] for item in [i for i in range(cactus.x, cactus.x+cactus.width)]) and any(item in [i for i in range(self.y, self.y+self.size)] for item in [i for i in range(cactus.y, cactus.y+cactus.height)]):
                self.alive = False

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_count = 0
            play_sound('slime_jump')
            self.jumped = True
    
    def on_surface(self):
        if self.y != self.GAME_BASE_LAYER:
            self.surface = False
        else:
            self.surface = True
            if self.surface_sound:
                self.surface = False
                self.surface_sound = False
                play_sound('slime_on_surface')

        if self.y < 0:
            self.y = 0

    def update(self, tick_image):
        self.update_state()
        self.on_surface()
        self.update_skins(tick_image)
        if self.is_jumping:
            if self.jump_count < self.jump_height:
                self.y -= self.jump_speed
                self.jump_count += self.jump_speed
            else:
                self.jump_count = 0
                self.is_jumping = False
                self.surface_sound = True
        else:
            if self.y < self.GAME_BASE_LAYER:
                self.y += self.gravity

    def update_state(self): 
        if self.is_jumping and self.state != 'jump':
            self.state = 'jump'
            self.skin_list = []

        elif self.jumped and self.y == self.GAME_BASE_LAYER and self.state != 'on_surface':
            self.start_time = time.time()
            self.state = 'on_surface'
            self.jumped = False
            self.skin_list = []
        
        else:
            if self.y == self.GAME_BASE_LAYER and time.time() - self.start_time <= 20 and self.state != 'walk':
                self.state = 'walk'
                self.skin_list = []
