import numpy as np
from sklearn import svm
from sklearn import preprocessing

class Classifier:
    """A class to classify facial images into different emotions"""
    
    @staticmethod
    def get_expression_from_label(label):
        """ get expression name from label id """

        option = {0:'NEURAL',
                        1:'ANGER',
                        2:'CONTEMPT',
                        3:'DISGUST',
                        4:'FEAR',
                        5:'HAPPY',
                        6:'SADNESS',
                        7:'SURPRISE'
        }

        return option[label]

    def __init__(self, subset_num):
        self.subset_num = subset_num
        self.features_pool = [[] for i in range(self.subset_num)]
        self.labels_pool = [[] for i in range(self.subset_num)]
        self.urls_pool = [[] for i in range(self.subset_num)]

    def cross_validation(self):

        recognition_results = [0] * self.subset_num

        for i in range(self.subset_num):
            #   Use the i_th subset for testing and the rest for training
            train_indexes = range(0, i) + range(i + 1, self.subset_num) 
            test_indexes = [i]

            self.generate_training_testing_files(train_indexes, test_indexes)

            svm_model = svm.LinearSVC(C=10)
            svm_model.fit(self.train_features, self.train_labels)
            self.predict_labels = svm_model.predict(self.test_features)
            recognition_results[i] = svm_model.score(self.test_features, self.test_labels)

            print recognition_results[i]

 #           self.demonstrate_wrong_predictions()

        print "Mean recognition rate is {}.".format(np.mean(recognition_results))

    def demonstrate_wrong_predictions(self):
        from dir_processing import DirProcessing
        from visualization import Visualization

        for i in range(len(self.predict_labels)):
            test_label = self.test_labels[i]
            predict_label = self.predict_labels[i]

            if test_label != predict_label:
                test_expression = Classifier.get_expression_from_label(test_label)
                predict_expression = Classifier.get_expression_from_label(predict_label)
                print "Wrong prediction: {}, Right prediction: {}.".format(predict_expression, test_expression)

                landmarks_url = self.test_urls[i]
                img_url = DirProcessing.generate_img_url_from_landmarks_url(landmarks_url)
                Visualization.draw_landmarks_on_img(img_url)


    def generate_training_testing_files(self, train_indexes, test_indexes):
        self.train_features = []
        self.train_labels = []
        self.train_urls = []
        self.test_features = []
        self.test_labels = []
        self.test_urls = []

        for train_index in train_indexes:
            self.train_features += self.features_pool[train_index]
            self.train_labels += self.labels_pool[train_index]
            self.train_urls += self.urls_pool[train_index]

        for test_index in test_indexes:
            self.test_features += self.features_pool[test_index]
            self.test_labels += self.labels_pool[test_index]
            self.test_urls += self.urls_pool[test_index]

        self.train_features = np.array(self.train_features)
        self.train_labels = np.array(self.train_labels)
        self.test_features = np.array(self.test_features)
        self.test_labels = np.array(self.test_labels)
        
        need_normalized = False 
        if need_normalized:
            self.train_features = preprocessing.normalize(self.train_features, norm='l2')
            self.test_features = preprocessing.normalize(self.test_features, norm='l2')
            

    def generate_features_pool(self):
        """ generate train and test files for classification """

        from analysis import Analysis
        from dir_processing import DirProcessing
        from file_op import FileOp

        landmarks_urls_list, features = Analysis.get_topic_proportions_for_every_image()

        subsets_dict = self.divide_persons_into_subsets()
        
        for i in range(0, len(landmarks_urls_list)):
            landmarks_url = landmarks_urls_list[i]
            label_url = DirProcessing.get_label_url_from_landmarks_url(landmarks_url)
            loc = DirProcessing.get_location_from_sequence(landmarks_url, 3)

            if label_url and loc != "MIDDLE":
                person_id, perform_id, index_id = DirProcessing.get_id_from_label_url(label_url)
                subset_id = subsets_dict[person_id]
                feature = features[i, :]

                if loc == "START":
                    label = 0
                else:
                    label = FileOp.read_label_file(label_url)

                self.features_pool[subset_id].append(feature)
                self.labels_pool[subset_id].append(label)
                self.urls_pool[subset_id].append(landmarks_url)

        print "Features pools have been generated. "

    def divide_persons_into_subsets(self):
        from dir_processing import DirProcessing

        person_ids = DirProcessing.get_all_person_ids()
        permute_ids = np.random.permutation(person_ids)

        total_person_num = len(person_ids)

        step_arr = np.linspace(0, total_person_num, self.subset_num + 1)
        step_arr = step_arr.astype(int)

        subsets_dict = dict.fromkeys(person_ids)

        for i in range(0, self.subset_num):
            for j in range(step_arr[i], step_arr[i + 1]):
                subsets_dict[permute_ids[j]] = i

        return subsets_dict

    def main(self):
        import os
        import sys
        lib_path1 = os.path.abspath('../utilization/')
        lib_path2 = os.path.abspath('../visualization/')
        sys.path.append(lib_path1)
        sys.path.append(lib_path2)

        self.generate_features_pool()
        self.cross_validation()

###########################################################

if __name__ == '__main__':
    c = Classifier(8)
    c.main()


