from __future__ import with_statement
import ConfigParser
import numpy as np
import math

class LSFSequence:
    """A class representing LSF features for expression sequence"""
    

    def __init__(self, landmarks_urls, landmarks, lsf_sequence):
        self.landmarks_urls = landmarks_urls
        self.landmarks = landmarks
        self.lsf_sequence = lsf_sequence


class LSF:
    """A class to compute LSF features"""


    config = ConfigParser.ConfigParser()
    with open('../config/config.ini','rw') as cfgfile:
        config.readfp(cfgfile)
        keypoint_num = int(config.get('feature','keypoint_num'))
        direction_num = int(config.get('feature','direction_num'))
        radius_num = int(config.get('feature','radius_num'))
        radius_interval = int(config.get('feature','radius_interval'))

    id2word = {}
    word2id = {}

    @staticmethod
    def build_dictionary():
        count = 0
        for i in xrange(0, LSF.keypoint_num):
            
            keypoint_sindex = str(i).zfill(2)
            word = "P{}NEURAL".format(keypoint_sindex)
            LSF.word2id[word] = count
            LSF.id2word[count] = word
            count = count + 1

            for j in xrange(0, LSF.direction_num):

                direction_sindex = str(j).zfill(2)
                word = "P{}D{}R99".format(keypoint_sindex, direction_sindex)
                LSF.word2id[word] = count
                LSF.id2word[count] = word
                count = count + 1

                for k in xrange(LSF.radius_interval, (LSF.radius_num + 1) * LSF.radius_interval, LSF.radius_interval):
                    word = LSF.generate_format_word(i, j, k)
                    LSF.word2id[word] = count
                    LSF.id2word[count] = word
                    count = count + 1

    @staticmethod
    def generate_format_word(keypoint_index, direction_index, radius_index):
        keypoint_sindex = str(keypoint_index).zfill(2)
        direction_sindex = str(direction_index).zfill(2)
        radius_sindex = str(radius_index).zfill(2)

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

        from file_op import FileOp
        landmarks_sequence = FileOp.read_landmarks_sequence(landmarks_urls)

        lsf_sequence = [] 
        for i in xrange(0, len(landmarks_urls)):
            landmarks = landmarks_sequence[i] 
            landmarks_neural = landmarks_sequence[0] 
            lsf_document = LSF.lsf(landmarks, landmarks_neural) #get the lsf word feature from one image (document) 
            lsf_sequence.append(lsf_document)

        return LSFSequence(landmarks_urls, landmarks_sequence, lsf_sequence)

    @staticmethod
    def compute_word(landmark_index, landmark, landmark_neural):
        """ compute the lsf feature for one landmark """

        delta_landmark = landmark - landmark_neural
        
        radius = np.linalg.norm(delta_landmark)

        if radius < LSF.radius_interval:
            landmark_sindex = str(landmark_index).zfill(2)
            word = "P{}NEURAL".format(landmark_sindex)
            return word     # A Neural word

        y_axis = np.asarray([0, -1])

        cos_value = np.dot(delta_landmark, y_axis) / radius

        angle = math.degrees(math.acos(cos_value))
        if delta_landmark[0] < 0:
            angle = 360 - angle

        radius_index = (int(radius) / LSF.radius_interval + 1) * LSF.radius_interval
        if radius_index > LSF.radius_interval * LSF.radius_num:
            radius_index = 99

        direction_interval = 360 / LSF.direction_num
        direction_index = int((angle + direction_interval / 2) / direction_interval)
        if direction_index >= LSF.direction_num:
            direction_index = 0

        word = LSF.generate_format_word(landmark_index, direction_index, radius_index)

        return word

    @staticmethod
    def generate_corpus_and_write_to_file():
        """ generate the copus, write it to files and store the LSF corpus features """
        
        import os
        import sys
        lib_path = os.path.abspath('../utilization/')
        sys.path.append(lib_path)

        from dir_processing import DirProcessing

        LSF.build_dictionary()

        lsf_corpus = []

        person_ids = DirProcessing.get_all_person_ids()
        for person_id in person_ids:
            perform_ids = DirProcessing.get_all_perform_ids_from_person_id(person_id)
            for perform_id in perform_ids:
                landmarks_urls = DirProcessing.get_all_landmarks_urls_from_sequence(person_id, perform_id)
                expression_sequence = LSF.lsf_from_sequence(landmarks_urls)
                print 'The feature extraction of expression person S{} and perform time {} has ' \
                        'been done.'.format(person_id, perform_id)
                lsf_corpus.append(expression_sequence)

        import cPickle
        with open('../model/corpus.pk', 'wb') as f:
            cPickle.dump(lsf_corpus, f)
       
        with open('../model/corpus.txt', 'w') as f:
            for expression_sequence in lsf_corpus:
                lsf_sequence = expression_sequence.lsf_sequence
                for lsf_document in lsf_sequence:
                    f.write(str(len(lsf_document)))
                    for word, count in lsf_document.iteritems():
                        wid = LSF.word2id[word]
                        s = " %d:%d" %(wid, count)
                        f.write(s)
                    f.write("\n")
    
    @staticmethod
    def write_vocab_to_file():
        """ write the all the words to file """

        with open('../model/vocab.txt', 'w')  as f:
            for i in xrange(0, len(LSF.id2word)):
                f.write(str(LSF.id2word[i]) + "\n")
            


    
    @staticmethod
    def test():
        import os
        import sys
        lib_path = os.path.abspath('../utilization/')
        sys.path.append(lib_path)

        from dir_processing import DirProcessing
        from file_op import FileOp

        LSF.build_dictionary()
        landmarks_urls = DirProcessing.get_all_landmarks_urls_from_sequence('87','4')

        test_one_sequence = True
        if test_one_sequence:
            video = LSF.lsf_from_sequence(landmarks_urls)
            print video.landmarks_urls

        test_one_landmark = False
        if test_one_landmark:
            landmarks = FileOp.read_landmarks_file(landmarks_urls[11])
            landmarks_neural = FileOp.read_landmarks_file(landmarks_urls[0])
            lsf_document = LSF.lsf(landmarks, landmarks_neural)
            landmark = landmarks[35,:]
            landmark_neural = landmarks_neural[35, :]
            word = LSF.compute_word(35, landmark, landmark_neural)
            print landmark, landmark_neural, word


#################################################

if __name__ == '__main__':
#    LSF.generate_corpus_and_write_to_file()
#    LSF.build_dictionary()
#    LSF.write_vocab_to_file()

    import cPickle
    with open('../model/corpus.pk','rb') as f:
        lsf_corpus = cPickle.load(f)
        print 'succeed'




        

