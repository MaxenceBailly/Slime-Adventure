import ctypes, yaml
def get_resolution():
    usr32 = ctypes.windll.user32
    return (usr32.GetSystemMetrics(0), usr32.GetSystemMetrics(1))

def read_highscore():
    try:
        with open('Slime-Adventure/highscore.yml', 'r') as fichier:
            highscore = yaml.safe_load(fichier)
            return highscore
    except FileNotFoundError:
        return 0

def write_highscore(new_highscore):
    with open('Slime-Adventure/highscore.yml', 'w') as fichier:
        yaml.dump(new_highscore, fichier)

def clear_root(root):
    for widget in root.winfo_children():
        widget.destroy()
