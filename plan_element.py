import tkinter as tk

class PlanElement:
    def __init__(self, x, y, width, height, image, speed, canvas):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self._speed = speed

    def despawnable(self):
        if self.x+self.width < -100:
            return True

    def update(self, speed):
        self._speed = speed
        self.x -= self._speed
        self.canvas.create_image(self.x, self.y, anchor=tk.NW, image=self.image)
