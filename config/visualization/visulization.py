from PIL import Image
from __future__ import with_statement
import ConfigParser

config = ConfigParser.ConfigParser()
with open('../config/config.ini','r') as cfgfile:
    config.readfp(cfgfile)
    dataset_root = config.get('directory','dataset_root')
    label_folder = config.get('directory','label_folder')
    landmark_folder = config.get('directory','landmark_folder')

class Visualization:
    """A class for visualizing something"""
    def __init__(self, person_id, perform_id, img_id):
        self.img_loc = img_loc
        self.perform = perform_id
        self.img_id = img_id

    def generate_img_loc(self)
        

    def draw_image(self):
        self.img = Image.open(self.img_loc)
        self.img.show()

    def draw_landmarks_on_image(self):
        self.draw_image()

    def get_landmarks_loc(self)
        
