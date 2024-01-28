from tkinter import *
from PIL import Image, ImageTk
import yaml, os, ctypes, random
from play_sound import play_sound
from game import Game
from related_function import *

ROOT_WIDTH = get_resolution()[0]
ROOT_HEIGHT = get_resolution()[1]
GAME_BASE_LAYER = ROOT_HEIGHT-100
GAME_SPEED = 2

# Player binding
def on_key(event):
    global fullscreen
    
    if event.keysym == 'Escape':
        quit()
    
    elif event.keysym == 'F11':
        if fullscreen:
            fullscreen = False
        else:
            fullscreen = True
        root.attributes('-fullscreen', fullscreen)

# Window
root = Tk()
root.iconphoto(False, PhotoImage(file='Slime-Adventure/images/slime/green/walk/1.png'))
root.geometry(f'{ROOT_WIDTH}x{ROOT_HEIGHT}')
root.title('Slime-Adventure')
fullscreen = True
root.attributes('-fullscreen', fullscreen)
root.bind('<Key>', on_key)
print(get_resolution())

game = Game(root=root, base_layer=GAME_BASE_LAYER, game_speed=GAME_SPEED)

def appear_menu():
    menu_frame = Frame(root)  # Créez un Frame pour les boutons
    menu_frame.pack(side='top', expand=1)  # Placez le Frame au centre verticalement

    play_b = Button(menu_frame, text='Play', command=game.game_start)
    credit_b = Button(menu_frame, text='Credit')
    settings_b = Button(menu_frame, text='Settings')
    high_score_label = Label(menu_frame, text=f"High  score : {read_highscore()}", font=("Helvetica", 20))

    # Centrez horizontalement les boutons dans le Frame
    high_score_label.pack(side='top', anchor='center')
    play_b.pack(side='top', anchor='center')
    credit_b.pack(side='top', anchor='center')
    settings_b.pack(side='top', anchor='center')

appear_menu()
root.mainloop()
