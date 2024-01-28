import tkinter as tk
from player import Player
from plan import Plan
from obstacle import Obstacle
from related_function import *
import os, random

class Game:
    def __init__(self, root, base_layer, game_speed):
        self.root = root
        self.ROOT_WIDTH = get_resolution()[0]
        self.ROOT_HEIGHT = get_resolution()[1]
        self.GAME_BASE_LAYER = base_layer
        self.GAME_SPEED = game_speed

        self.score = 0
        self.score_speed = 0
        self.game_tick = 0
        self.tick_image = 1
        self.speed_threshold = 1000
        self.secret_code_str = ''

        self.obstacles_list = []
    
    def game_start(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        global player, obstacles_list, game, in_front_setting_list, behind_setting_list, score_speed
        game = tk.Canvas(self.root, width=self.ROOT_WIDTH, height=self.ROOT_HEIGHT, bg='lightblue')
        game.focus_set()

        player = Player(self.GAME_BASE_LAYER, self.GAME_SPEED, self.score_speed)

        in_front_setting_list = [Plan(name='dirt', folder='dirt', distance_min=0, distance_max=0, y=self.GAME_BASE_LAYER, element_width=50, element_height=50, speed=self.speed(5), ROOT_WIDTH=self.ROOT_WIDTH, canvas=game),
                                Plan(name='ground', folder='ground', distance_min=0, distance_max=0, y=self.GAME_BASE_LAYER+50, element_width=50, element_height=50, speed=self.speed(5), ROOT_WIDTH=self.ROOT_WIDTH, canvas=game),
                                Plan(name='grass', folder='grass', distance_min=50, distance_max=100, y=self.GAME_BASE_LAYER-30, element_width=30, element_height=30, speed=self.speed(5), ROOT_WIDTH=self.ROOT_WIDTH, canvas=game)
                                ]

        behind_setting_list = [Plan(name='clouds', folder='clouds', distance_min=200, distance_max=400, y=self.GAME_BASE_LAYER-470, element_width=80, element_height=80, speed=self.speed(1.2), ROOT_WIDTH=self.ROOT_WIDTH, canvas=game),
                            Plan(name='clouds', folder='clouds', distance_min=100, distance_max=300, y=self.GAME_BASE_LAYER-500, element_width=90, element_height=90, speed=self.speed(1), ROOT_WIDTH=self.ROOT_WIDTH, canvas=game),
                            Plan(name='trees', folder='trees', distance_min=0, distance_max=100, y=self.GAME_BASE_LAYER-200, element_width=200, element_height=200, speed=self.speed(3), ROOT_WIDTH=self.ROOT_WIDTH, canvas=game),
                            Plan(name='trees', folder='trees', distance_min=0, distance_max=100, y=self.GAME_BASE_LAYER-250, element_width=250, element_height=250, speed=self.speed(4), ROOT_WIDTH=self.ROOT_WIDTH, canvas=game),
                            Plan(name='trees', folder='trees', distance_min=50, distance_max=100, y=self.GAME_BASE_LAYER-250, element_width=250, element_height=250, speed=self.speed(4), ROOT_WIDTH=self.ROOT_WIDTH, canvas=game),
                            Plan(name='trees', folder='trees', distance_min=0, distance_max=100, y=self.GAME_BASE_LAYER-300, element_width=300, element_height=300, speed=self.speed(4.5), ROOT_WIDTH=self.ROOT_WIDTH, canvas=game)
                            ]

        self.root.bind('<Key>', self.on_key)
        self.update_game()

        game.pack()

    def update_tick_image(self):
        self.game_tick += 1
        if self.game_tick >= 50:
            self.game_tick = 0
            if self.tick_image == 1:
                self.tick_image = 2
            else:
                self.tick_image = 1

    def update_game(self):
        global score_label, entities

        self.score_speed = self.score//self.speed_threshold
        player.dead(self.obstacles_list)
        if player.alive:
            self.score += 1

            #player update
            player.update(tick_image=self.tick_image)

            self.obstacles_list = self.create_obstacles(distance_min=70*self.speed(5), max=5, spawn_rate=1, root_width=self.ROOT_WIDTH, game_base_layer=self.GAME_BASE_LAYER)
            for i, obstacle in enumerate(self.obstacles_list):
                if obstacle.despawnable():
                    self.obstacles_list.pop(i)
                else:
                    obstacle.update(self.speed(5))

            #game clear  
            game.delete('all')

            #Tout les décors derrière
            for setting in behind_setting_list:
                setting.update()

            #afficher le joueur
            game.create_image(player.x, player.y, anchor=tk.SW, image=player.skin)

            #afficher les obstacle
            for obstacle in self.obstacles_list:
                game.create_image(obstacle.x, obstacle.y, anchor=tk.SW, image=obstacle.image)

            #afficher le score
            game.create_text(10, 10, text=f"High score: {read_highscore()}", anchor=tk.NW, fill='gray', font=("Helvetica", 20), tags="score_text")
            game.create_text(10, 40, text=f"Score: {self.score}", anchor=tk.NW, fill='gray', font=("Helvetica", 20), tags="score_text")
            
            #compter les entitées à afficher
            entities = {}
            entities['obstacles'] = len(self.obstacles_list)
            for setting in in_front_setting_list + behind_setting_list:
                setting.count_entities(entities_list=entities)
            game.create_text(10, 70, text=f"{entities}", anchor=tk.NW, fill='gray', font=("Helvetica", 20), tags="score_text")
            entities = {}

            #Tout les décors devant
            for setting in in_front_setting_list:
                setting.update()

            self.update_tick_image()
            game.after(10, self.update_game)
        
        else:
            game.pack_forget()
            death_frame = tk.Frame(self.root)  # Créez un Frame pour les boutons
            death_frame.pack(side='top', expand=1)
            death_label = tk.Label(death_frame, text='You died', font=("Helvetica", 36))
            death_label.pack()
            score_label = tk.Label(death_frame, text=f"You're score : {self.score}", font=("Helvetica", 20))
            score_label.pack()
            if read_highscore() < self.score:
                write_highscore(self.score)
            self.root.update()
            self.score = 0
            self.score_speed = 0
            player.alive = True
            self.obstacles_list = []
            self.appear_menu()

    def speed(self, n):
        return n*self.GAME_SPEED+self.score_speed

    def create_obstacles(self, distance_min, max, spawn_rate, root_width, game_base_layer):
        cactus_image_list = []
        for file_path in os.listdir('Slime-Adventure/images/cactus/cactus'):
            if os.path.isfile(os.path.join('Slime-Adventure/images/cactus/cactus', file_path)):
                cactus_image_list.append(file_path)

        if not self.obstacles_list:
            self.obstacles_list.append(Obstacle(x=root_width, y=game_base_layer, width=70, height=90, image=random.choice(cactus_image_list), ROOT_WIDTH=root_width, GAME_BASE_LAYER=game_base_layer))
        elif self.obstacles_list[-1].x <= distance_min and random.randint(0, spawn_rate) == 0:
            for i in range(random.randint(1, max)):
                new_cactus = Obstacle(x=root_width + i*random.randint(distance_min, distance_min+100), y=game_base_layer, width=70, height=90, image=random.choice(cactus_image_list), ROOT_WIDTH=root_width, GAME_BASE_LAYER=game_base_layer)
                self.obstacles_list.append(new_cactus)
        return self.obstacles_list

    def on_key(self, event):
        global secret_code
        if event.keysym == 'space' and player.surface:
            player.dead(self.obstacles_list)
            player.jump()
        
        elif event.keysym == 'Escape':
            quit()
        
        elif event.keysym == 'g':
            print('g')
        
        else:
            secret_code = ''

    def appear_menu(self):
        menu_frame = tk.Frame(self.root)  # Créez un Frame pour les boutons
        menu_frame.pack(side='top', expand=1)  # Placez le Frame au centre verticalement

        play_b = tk.Button(menu_frame, text='Play', command=self.game_start)
        credit_b = tk.Button(menu_frame, text='Credit')
        settings_b = tk.Button(menu_frame, text='Settings')
        high_score_label = tk.Label(menu_frame, text=f"High  score : {read_highscore()}", font=("Helvetica", 20))

        # Centrez horizontalement les boutons dans le Frame
        high_score_label.pack(side='top', anchor='center')
        play_b.pack(side='top', anchor='center')
        credit_b.pack(side='top', anchor='center')
        settings_b.pack(side='top', anchor='center')

