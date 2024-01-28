from PIL import Image

# Sélectionner l'image d'entrée
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(title="Sélectionnez une image", filetypes=[("Images", "*.png")])
if not file_path:
    exit()

img = Image.open(file_path)

# Obtenir la taille de l'image d'origine
width, height = img.size

# Créer une nouvelle image avec une taille multipliée par 2
new_width = width * 2
new_height = height * 2
new_img = Image.new("RGBA", size=(new_width, new_height), color=(0, 0, 0, 0))

# Copier les pixels de l'image d'origine dans les carrés de 2x2 de la nouvelle image
for x in range(width):
    for y in range(height):
        pixel = img.getpixel((x, y))
        for i in range(2):
            for j in range(2):
                new_x = x * 2 + i
                new_y = y * 2 + j
                new_img.putpixel((new_x, new_y), pixel)

# Enregistrer ou afficher la nouvelle image
root = tk.Tk()
root.withdraw()
folder_path = filedialog.askdirectory(title="Sélectionnez un dossier pour enregistrer la nouvelle image")
if folder_path:
    save_path = f'{folder_path}/new.png'
    new_img.save(save_path)
    print(f"Image enregistrée sous : {save_path}")
else:
    new_img.show()

root.destroy()
