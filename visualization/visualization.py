import os, sys
import numpy as np
import cv2

class Visualization:
    """A class for visualizing something"""

    @staticmethod
    def draw_img(img_url):
        from file_op import FileOp
        img = FileOp.read_img_file(img_url)
        cv2.imshow('image',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def draw_landmarks_on_img(img_url):
        from dir_processing import DirProcessing
        landmarks_url = DirProcessing.generate_landmarks_url_from_img_url(img_url)

        from file_op import FileOp
        img = FileOp.read_img_file(img_url)
        landmarks = FileOp.read_landmarks_file(landmarks_url)

        for i in xrange(0, landmarks.shape[0]):   # for every point
            loc = landmarks[i, :]
            x = int(round(loc[0]))
            y = int(round(loc[1]))
            cv2.circle(img, (x, y), 3, 255)

        cv2.imshow('image',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def draw_landmarks_on_sequence(img_urls):
        from dir_processing import DirProcessing
        landmarks_urls = []
        for i in xrange(0, len(img_urls)):
            img_url = img_urls[i]
            landmarks_url = DirProcessing.generate_landmarks_url_from_img_url(img_url)
            landmarks_urls.append(landmarks_url)

        from file_op import FileOp
        for i in xrange(0, len(img_urls)):
            img_url = img_urls[i]
            landmarks_url = landmarks_urls[i]
            img = FileOp.read_img_file(img_url)
            landmarks = FileOp.read_landmarks_file(landmarks_url)

            for i in xrange(0, landmarks.shape[0]):   # for every point
                loc = landmarks[i, :]
                x = int(round(loc[0]))
                y = int(round(loc[1]))
                cv2.circle(img, (x, y), 1, 255)
            
            print img_url
            cv2.imshow('image' + str(i), img)
            cv2.waitKey(0)
        
        cv2.destroyAllWindows()
                                                                                        

    @staticmethod
    def test():
        lib_path = os.path.abspath('../utilization/')
        sys.path.append(lib_path)

        from dir_processing import DirProcessing

        img_urls = DirProcessing.get_all_img_urls_from_sequence('79','2')
        print img_urls
        Visualization.draw_landmarks_on_sequence(img_urls)
#        img_url = DirProcessing.generate_img_url('10','2','1')
#        Visualization.draw_landmarks_on_img(img_url)

####################################3
    
if __name__ == '__main__':
    Visualization.test()

        
