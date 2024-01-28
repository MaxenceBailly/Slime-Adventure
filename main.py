from tkinter import *
from PIL import Image, ImageTk
import yaml, os, ctypes, random
from play_sound import play_sound
from player import Player
from plan import Plan
from obstacle import Obstacle

def get_resolution():
    usr32 = ctypes.windll.user32
    return (usr32.GetSystemMetrics(0), usr32.GetSystemMetrics(1))

ROOT_WIDTH = get_resolution()[0]
ROOT_HEIGHT = get_resolution()[1]
GAME_BASE_LAYER = ROOT_HEIGHT-100
GAME_SPEED = 2

score = 0
score_speed = 0
game_tick = 0
tick_image = 1
speed_threshold = 1000
secret_code_str = ''

def speed(n):
 return n*GAME_SPEED+score_speed

def read_highscore():
    try:
        with open('Slime Adventure/highscore.yml', 'r') as fichier:
            highscore = yaml.safe_load(fichier)
            return highscore
    except FileNotFoundError:
        return 0

def write_highscore(new_highscore):
    with open('Slime Adventure/highscore.yml', 'w') as fichier:
        yaml.dump(new_highscore, fichier)

# Player binding
def on_key(event):
    global fullscreen, secret_code
    if event.keysym == 'space' and player.surface:
        player.dead(obstacles_list)
        player.jump()
    
    elif event.keysym == 'Escape':
        quit()
    
    elif event.keysym == 'F11':
        if fullscreen:
            fullscreen = False
        else:
            fullscreen = True
        root.attributes('-fullscreen', fullscreen)
    
    elif event.keysym == 'g':
        print('g')
    
    else:
        secret_code = ''

def update_tick_image():
    global game_tick, tick_image
    game_tick += 1
    if game_tick >= 50:
        game_tick = 0
        if tick_image == 1:
            tick_image = 2
        else:
            tick_image = 1

def update_game():
    global score, score_label, score_speed, speed_threshold, entities

    score_speed = score//speed_threshold
    player.dead(obstacles_list)
    if player.alive:
        score += 1

        #player update
        player.update(tick_image=tick_image)

        create_obstacles(obstacles_list=obstacles_list, distance_min=70*speed(5), max=5, spawn_rate=1)
        for i, obstacle in enumerate(obstacles_list):
            if obstacle.despawnable():
                obstacles_list.pop(i)
            else:
                obstacle.update(speed(5))

        #game clear  
        game.delete('all')

        #Tout les décors derrière
        for setting in behind_setting_list:
            setting.update()

        #afficher le joueur
        game.create_image(player.x, player.y, anchor=SW, image=player.skin)

        #afficher les obstacle
        for obstacle in obstacles_list:
            game.create_image(obstacle.x, obstacle.y, anchor=SW, image=obstacle.image)

        #afficher le score
        game.create_text(10, 10, text=f"High score: {read_highscore()}", anchor=NW, fill='gray', font=("Helvetica", 20), tags="score_text")
        game.create_text(10, 40, text=f"Score: {score}", anchor=NW, fill='gray', font=("Helvetica", 20), tags="score_text")
        
        #compter les entitées à afficher
        entities = {}
        entities['obstacles'] = len(obstacles_list)
        for setting in in_front_setting_list + behind_setting_list:
            setting.count_entities(entities_list=entities)
        game.create_text(10, 70, text=f"{entities}", anchor=NW, fill='gray', font=("Helvetica", 20), tags="score_text")
        entities = {}

        #Tout les décors devant
        for setting in in_front_setting_list:
            setting.update()

        update_tick_image()
        #update encore (recurrence)
        game.after(10, update_game)
    
    else:
        game.pack_forget()
        death_frame = Frame(root)  # Créez un Frame pour les boutons
        death_frame.pack(side='top', expand=1)
        death_label = Label(death_frame, text='You died', font=("Helvetica", 36))
        death_label.pack()
        score_label = Label(death_frame, text=f"You're score : {score}", font=("Helvetica", 20))
        score_label.pack()
        if read_highscore() < score:
            write_highscore(score)
        root.update()
        score = 0
        score_speed = 0

def create_obstacles(obstacles_list, distance_min, max, spawn_rate):
    cactus_image_list = []
    for file_path in os.listdir('Slime Adventure/images/cactus/cactus'):
        if os.path.isfile(os.path.join('Slime Adventure/images/cactus/cactus', file_path)):
            cactus_image_list.append(file_path)

    if not obstacles_list:
        obstacles_list.append(Obstacle(x=ROOT_WIDTH, y=GAME_BASE_LAYER, width=70, height=90, image=random.choice(cactus_image_list), ROOT_WIDTH=ROOT_WIDTH, GAME_BASE_LAYER=GAME_BASE_LAYER))
    elif obstacles_list[-1].x <= distance_min and random.randint(0, spawn_rate) == 0:
        for i in range(random.randint(1, max)):
            new_cactus = Obstacle(x=ROOT_WIDTH + i*random.randint(distance_min, distance_min+100), y=GAME_BASE_LAYER, width=70, height=90, image=random.choice(cactus_image_list), ROOT_WIDTH=ROOT_WIDTH, GAME_BASE_LAYER=GAME_BASE_LAYER)
            obstacles_list.append(new_cactus)
    return obstacles_list

# Window
root = Tk()
root.iconphoto(False, PhotoImage(file='Slime Adventure/images/slime/green/walk/1.png'))
root.geometry(f'{ROOT_WIDTH}x{ROOT_HEIGHT}')
root.title('Slime Adventure')
fullscreen = True
root.attributes('-fullscreen', fullscreen)
root.bind('<Key>', on_key)

print(get_resolution())

def appear_menu():
    menu_frame = Frame(root)  # Créez un Frame pour les boutons
    menu_frame.pack(side='top', expand=1)  # Placez le Frame au centre verticalement

    play_b = Button(menu_frame, text='Play', command=game_start)
    credit_b = Button(menu_frame, text='Credit')
    settings_b = Button(menu_frame, text='Settings')
    high_score_label = Label(menu_frame, text=f"High  score : {read_highscore()}", font=("Helvetica", 20))

    # Centrez horizontalement les boutons dans le Frame
    high_score_label.pack(side='top', anchor='center')
    play_b.pack(side='top', anchor='center')
    credit_b.pack(side='top', anchor='center')
    settings_b.pack(side='top', anchor='center')

def game_start():
    for widget in root.winfo_children():
        widget.destroy()

    global player, obstacles_list, game, in_front_setting_list, behind_setting_list, score_speed
    game = Canvas(root, width=ROOT_WIDTH, height=ROOT_HEIGHT, bg='lightblue')
    game.focus_set()

    player = Player(GAME_BASE_LAYER, GAME_SPEED, score_speed)

    in_front_setting_list = [Plan(name='dirt', folder='dirt', distance_min=0, distance_max=0, y=GAME_BASE_LAYER, element_width=50, element_height=50, speed=speed(5), ROOT_WIDTH=ROOT_WIDTH, canvas=game),
                             Plan(name='ground', folder='ground', distance_min=0, distance_max=0, y=GAME_BASE_LAYER+50, element_width=50, element_height=50, speed=speed(5), ROOT_WIDTH=ROOT_WIDTH, canvas=game),
                             Plan(name='grass', folder='grass', distance_min=50, distance_max=100, y=GAME_BASE_LAYER-30, element_width=30, element_height=30, speed=speed(5), ROOT_WIDTH=ROOT_WIDTH, canvas=game)
                            ]

    behind_setting_list = [Plan(name='clouds', folder='clouds', distance_min=200, distance_max=400, y=GAME_BASE_LAYER-470, element_width=80, element_height=80, speed=speed(1.2), ROOT_WIDTH=ROOT_WIDTH, canvas=game),
                           Plan(name='clouds', folder='clouds', distance_min=100, distance_max=300, y=GAME_BASE_LAYER-500, element_width=90, element_height=90, speed=speed(1), ROOT_WIDTH=ROOT_WIDTH, canvas=game),
                           Plan(name='trees', folder='trees', distance_min=0, distance_max=100, y=GAME_BASE_LAYER-200, element_width=200, element_height=200, speed=speed(3), ROOT_WIDTH=ROOT_WIDTH, canvas=game),
                           Plan(name='trees', folder='trees', distance_min=0, distance_max=100, y=GAME_BASE_LAYER-250, element_width=250, element_height=250, speed=speed(4), ROOT_WIDTH=ROOT_WIDTH, canvas=game),
                           Plan(name='trees', folder='trees', distance_min=50, distance_max=100, y=GAME_BASE_LAYER-250, element_width=250, element_height=250, speed=speed(4), ROOT_WIDTH=ROOT_WIDTH, canvas=game),
                           Plan(name='trees', folder='trees', distance_min=0, distance_max=100, y=GAME_BASE_LAYER-300, element_width=300, element_height=300, speed=speed(4.5), ROOT_WIDTH=ROOT_WIDTH, canvas=game)
                          ]

    obstacles_list = []

    score_label = Label(root, text=f"You're score : {score}", font=("Helvetica", 20))

    update_game()

    game.pack()

    appear_menu()

appear_menu()
root.mainloop()
