import tkinter as tk
from PIL import Image, ImageTk

class GUI(tk.Canvas):
    def __init__(self, root, width, height):
        super().__init__(root, width=width, height=height)
        self.images = []

    def add_image(self, x, y, image):
        image_id = self.create_image(x, y, image=image, anchor=tk.NW)
        self.images.append(image_id)
        return image_id

    def remove_image(self, image_id):
        self.delete(image_id)
        if image_id in self.images:
            self.images.remove(image_id)

    def clear_canvas(self):
        for image_id in self.images:
            self.delete(image_id)
        self.images = []

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("GUI Example")

    image1 = Image.open("Slime Adventure/images/gui/title.png")
    width, height = image1.size

    gui = GUI(root, width, height)
    gui.pack()

    photo_image1 = ImageTk.PhotoImage(image1)

    image_id1 = gui.add_image(0, 0, photo_image1)

    root.mainloop()
