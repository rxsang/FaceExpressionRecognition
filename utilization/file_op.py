import numpy as np
import cv2

class FileOp:
    
    @staticmethod
    def read_img_file(img_url):
        img = cv2.imread(img_url, 0)    # Gray image
        return img

    @staticmethod
    def read_landmarks_file(landmarks_url):
        landmarks = np.loadtxt(landmarks_url)
        return landmarks

    @staticmethod
    def read_landmarks_sequence(landmarks_urls):
        """ get all landmarks from a sequence of landmarks urls """
        
        landmarks_sequence = []
        for i in xrange(0, len(landmarks_urls)):
            landmarks_url = landmarks_urls[i]
            landmarks = FileOp.read_landmarks_file(landmarks_url)
            landmarks_sequence.append(landmarks)

        return landmarks_sequence

    @staticmethod
    def test():
        import os, sys
        lib_path = os.path.abspath('../utilization/')
        sys.path.append(lib_path)
        from dir_processing import DirProcessing
        landmarks_url = DirProcessing.generate_landmarks_url('147','2','1')
        landmarks = FileOp.read_landmarks_file(landmarks_url)
        print landmarks[1,:]

##########################################3

if __name__ == '__main__':
    FileOp.test()
