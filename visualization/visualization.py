import os, sys
import numpy as np
import cv2

class Visualization:
    """A class for visualizing something"""
    
    @staticmethod
    def draw_img(img_url):
        img = cv2.imread(img_url, 0)
        cv2.imshow('image',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def draw_landmarks_on_img():
        draw_img()

    @staticmethod
    def test():
        lib_path = os.path.abspath('../utilization/')
        sys.path.append(lib_path)
        from dir_processing import DirProcessing
        img_url = DirProcessing.generate_img_url('10','2','1')
        print img_url
        Visualization.draw_img(img_url)

####################################3
    
if __name__== '__main__':
    Visualization.test()

        
