from PIL import ImageTk, Image
import os, random

class Obstacle:
    def __init__(self, x, y, width, height, image, ROOT_WIDTH, GAME_BASE_LAYER):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = 'green'
        self.image = ImageTk.PhotoImage(Image.open(f"Slime Adventure/images/cactus/noobs/{image}").resize((self.width, self.height), Image.LANCZOS))
        self.ROOT_WIDTH = ROOT_WIDTH
        self.GAME_BASE_LAYER = GAME_BASE_LAYER
        self.type = ''

    def get_all_skins(self):
        pass

    def update(self, speed):
        self.x -= speed

    def despawnable(self):
        if self.x <= -100:
            return True
        else:
            return False
