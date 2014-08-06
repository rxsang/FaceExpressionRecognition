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
    def read_label_file(label_url):
        label = np.loadtxt(label_url)
        return int(label)

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
        label_url = DirProcessing.generate_label_url('34','3','27')
        label = FileOp.read_label_file(label_url)
        print label

##########################################3

if __name__ == '__main__':
    FileOp.test()
