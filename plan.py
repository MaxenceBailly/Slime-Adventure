import os, random
from PIL import Image, ImageTk
from plan_element import PlanElement

class Plan:
    def __init__(self, name, folder, distance_min, distance_max, y, element_width, element_height, speed, ROOT_WIDTH, canvas):
        self.canvas = canvas
        self.ROOT_WIDTH = ROOT_WIDTH
        self.name = name
        self.folder = f'Slime-Adventure/images/settings/{folder}'
        self.y = y
        self.distance_min = distance_min
        self.distance_max = distance_max
        self.element_width = element_width
        self.element_height = element_height
        self.speed = speed
        self.image_element_list = []
        self.element_list = []
        self.get_elements()
        self.create_elements()
        self.update()
    
    def count_entities(self, entities_list):
        if self.name in entities_list.keys():
            entities_list[self.name] += len(self.element_list)
        else:
            entities_list[self.name] = len(self.element_list)
    
    def get_elements(self):
        dir_path = f'Slime-Adventure/images/settings/{self.name}'
        for file_path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, file_path)):
                self.image_element_list.append(ImageTk.PhotoImage(Image.open(f"Slime-Adventure/images/settings/{self.name}/{file_path}").resize((self.element_width, self.element_height), Image.LANCZOS)))

    def update(self):
        for i, element in enumerate(self.element_list):
            if element.despawnable():
                poped_elements = self.element_list.pop(i)
                self.element_list.append(PlanElement(x=self.element_list[-1].x+self.element_list[-1].width+random.randint(self.distance_min, self.distance_max), y=self.y, width=self.element_width, height=self.element_height, image=random.choice(self.image_element_list), speed=self.speed, canvas=self.canvas))
            element.update(self.speed)
    
    def create_elements(self):
        for i in range(self.ROOT_WIDTH//(self.element_width+self.distance_max)+4):
            if i == 0:
                self.element_list.append(PlanElement(x=self.element_width+random.randint(self.distance_min, self.distance_max), y=self.y, width=self.element_width, height=self.element_height, image=random.choice(self.image_element_list), speed=self.speed, canvas=self.canvas))
            else:
                self.element_list.append(PlanElement(x=self.element_list[-1].x+self.element_list[-1].width+random.randint(self.distance_min, self.distance_max), y=self.y, width=self.element_width, height=self.element_height, image=random.choice(self.image_element_list), speed=self.speed, canvas=self.canvas))

    def check_lag(self):
        if self.distance_min == 0:
            pass
