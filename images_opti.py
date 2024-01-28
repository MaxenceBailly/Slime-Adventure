from PIL import *
import os

def img_dir(element):
    elements = os.listdir(f'Slime-Adventure/images/settings/{element}')
    return elements

def check_opti():
    pass

def new_img(img_lst):
    pass

print(img_dir('dirt'))
