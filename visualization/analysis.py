import numpy as np
import cPickle
import cv2

class Analysis:
    """ A class for analysing the result of ctm """


    @staticmethod
    def get_topic_proportions_for_every_image():
        
        landmarks_urls_list = []

        person_ids = DirProcessing.get_all_person_ids()
        for person_id in person_ids:
            perform_ids = DirProcessing.get_all_perform_ids_from_person_id(person_id)
            for perform_id in perform_ids:
                landmarks_urls = DirProcessing.get_all_landmarks_urls_from_sequence(person_id, perform_id)
                landmarks_urls_list.extend(landmarks_urls)
       
        doc_num = len(landmarks_urls_list)

        dt_file = '../ctm-dist/CTM46/final-lambda.dat'
        dt_vector = np.loadtxt(dt_file)
        topic_num = dt_vector.size / doc_num
        print dt_vector.size, doc_num, topic_num
        dt_matrix = np.reshape(dt_vector, (doc_num, topic_num)) 
        np.set_printoptions(suppress=True)

        final_theta = np.exp(dt_matrix)
        final_theta = final_theta / np.sum(final_theta, axis=1)[:, np.newaxis]

        return landmarks_urls_list, final_theta

    @staticmethod
    def cluster_topic_propotions(final_theta):

        import scipy.cluster
        centroid, label = scipy.cluster.vq.kmeans2(final_theta, 6, 100, minit='points')

        return centroid, label

    @staticmethod
    def random_show_cluster(landmarks_urls_list, label, cluster_index):
        
        from dir_processing import DirProcessing
        from file_op import FileOp
        from visualization import Visualization

        sample_list = np.where(label == cluster_index)[0]
        sample_list = np.random.permutation(sample_list)
       
        landmarks_urls_sublist = []
        for i in sample_list:
            landmarks_urls_sublist.append(landmarks_urls_list[i])

        img_urls_sublist = DirProcessing.generate_img_urls_from_landmarks_urls(landmarks_urls_sublist)

        Visualization.draw_landmarks_on_sequence(img_urls_sublist)
    
    @staticmethod
    def main():
        import os
        import sys
        lib_path = os.path.abspath('../utilization/')
        sys.path.append(lib_path)

        clustered = True

        if not clustered:
            landmarks_urls_list, final_theta = Analysis.get_topic_proportions_for_every_image()
            centroid, label = Analysis.cluster_topic_propotions(final_theta)

            print centroid

            with open('../model/kmeans_results.pk', 'wb') as f:
                cPickle.dump([landmarks_urls_list, centroid, label], f)

            
        if clustered:
            with open('../model/kmeans_results.pk', 'rb') as f:
                landmarks_urls_list, centroid, label = cPickle.load(f)

            Analysis.random_show_cluster(landmarks_urls_list, label, 4)

##############################################################

if __name__ == '__main__':
    Analysis.main()




        




