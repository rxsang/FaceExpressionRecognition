from __future__ import with_statement
import ConfigParser
import numpy as np
import math

class LSF:
    """A class to compute LSF features"""


    config = ConfigParser.ConfigParser()
    with open('../config/config.ini','rw') as cfgfile:
        config.readfp(cfgfile)
        keypoint_num = config.get('feature','keypoint_num')
        direction_num = config.get('feature','direction_num')
        radius_num = config.get('feature','radius_num')

    id2word = {}
    word2id = {}
    LSF.build_dictionary()

    @staticmehod
    def build_dictionary():
        count = 0
        for i in xrange(0, keypoint_num):
            for j in xrange(0, direction_num):
                for k in xrange(2, (radius_num + 1) * 2, 2):
                    word = LSF.generate_format_word(i, j, k)
                    LSF.word2id[word] = count
                    LSF.id2word[count] = word
                    count = count + 1

    @staticmethod
    def generate_format_word(keypoint_index, direction_index, radius_index):
        keypoint_sindex = str(keypoint_index).zfill(3)
        direction_sindex = str(direction_index).zfill(2)
        radius_sindex = str(radius_index)

        word_name = "P{}D{}R{}".format(keypoint_sindex, direction_sindex, radius_sindex)

        return word_name
        
    @staticmethod
    def lsf(landmarks, landmarks_neural):
    """ computer the lsf feature from one image """

        lsf_dict = {}
        for i in xrange(0, landmarks.shape[0]): # for every landmark
            landmark = landmarks[i, :]
            landmark_neural = landmarks_neural[i, :]
            word = LSF.compute_word(i, landmark, landmark_neural)
            lsf_dict[word] = 1  # as every word can only occur once.
           
        return lsf_dict # return lsf feature is a dict

    @staticmethod
    def lsf_from_sequence(landmarks_urls):
    """ computer the lsf feature from a expression sequence """

        from file_op import Fileop
        lsf_sequence = [] 
        for i in xrange(0, len(landmarks_urls)):
            landmarks_url = landmarks_urls[i]
            landmarks_neural_url = landmarks_urls[0]    # the first image is the neural expression
            landmarks = FileOp.read_landmarks_file(landmarks_url)
            landmarks_neural = FileOp.read_landmarks_file(landmarks_neral_url)
            lsf_document = LSF.lsf(landmarks, landmarks_neural) #get the lsf word feature from one image (document) 
        lsf_sequence.append(lsf_document)

        return lsf_sequence

    @staticmehtod
    def compute_word(landmark_index, landmark, landmark_neural):
    """ computer the lsf feature for one landmark """

        delta_landmark = landmark - landmark_neural
        
        radius = np.linalg.norm(delta_landmark)
        y_axis = np.asarray([0, 1])

        cos_value = np.dot(delta_landmark, y_axis)
        angle = math.degrees(math.acos(cos_value))
        delta_landmark[1] < 0 and angle = 360 - angle

        radius_index = (int(radius) / 2 + 1) * 2
        radius_index > 6 and radius_index = 6

        direction_index = int((angle + 22.5) / 45)
        direction_index < 8 and direction_index = 0

        word = LSF.generate_format_word(landmark_index, direction_index, radius_index)

        return word 




        

