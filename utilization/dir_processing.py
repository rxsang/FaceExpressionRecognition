from __future__ import with_statement
import ConfigParser
import os

class DirProcessing:
    config = ConfigParser.ConfigParser()
    with open('../config/config.ini','rw') as cfgfile:
        config.readfp(cfgfile)
        dataset_root = config.get('directory','dataset_root')
        image_folder = config.get('directory','image_folder')
        label_folder = config.get('directory','label_folder')
        landmarks_folder = config.get('directory','landmarks_folder')

    @staticmethod
    def generate_img_url(person_id, perform_id, index_id):
        person_sid = 'S' + person_id.zfill(3)
        perform_sid = perform_id.zfill(3)
        index_sid = index_id.zfill(8)
        
        img_name = "{}_{}_{}.png".format(person_sid, perform_sid, index_sid)
        img_url = "{}/{}/{}/{}/{}".format(DirProcessing.dataset_root, DirProcessing.image_folder, person_sid, perform_sid, img_name)

        return img_url
       
    @staticmethod
    def generate_label_url(person_id, perform_id, index_id):
        person_sid = 'S' + person_id.zfill(3)
        perform_sid = perform_id.zfill(3)
        index_sid = index_id.zfill(8)

        label_name = "{}_{}_{}_emotion.txt".format(person_sid, perform_sid, index_sid)
        label_url = "{}/{}/{}/{}/{}".format(DirProcessing.dataset_root, DirProcessing.label_folder, person_sid, perform_sid, label_name)

        return label_url

    @staticmethod
    def generate_landmarks_url(person_id, perform_id, index_id):
        person_sid = 'S' + person_id.zfill(3)
        perform_sid = perform_id.zfill(3)
        index_sid = index_id.zfill(8)
        
        landmarks_name = "{}_{}_{}_landmarks.txt".format(person_sid, perform_sid, index_sid)
        landmarks_url = "{}/{}/{}/{}/{}".format(DirProcessing.dataset_root, DirProcessing.landmarks_folder, person_sid, perform_sid, landmarks_name)

        return landmarks_url

    @staticmethod
    def get_id_from_img_url(img_url):
        img_name = os.path.basename(img_url)
        person_id = img_name[1:4]
        perform_id = img_name[5:8]
        index_id = img_name[9:17]

        return person_id, perform_id, index_id
        
    @staticmethod
    def generate_labels_url_from_img_url(img_url):
        person_id, perform_id, index_id = DirProcessing.get_id_from_img_url(img_url)
        label_url = DirProcessing.generate_label_url(person_id, perform_id, index_id)

        return label_url

    @staticmethod
    def generate_landmarks_url_from_img_url(img_url):
        person_id, perform_id, index_id = DirProcessing.get_id_from_img_url(img_url)
        landmarks_url = DirProcessing.generate_landmarks_url(person_id, perform_id, index_id)

        return landmarks_url

    @staticmethod
    def get_all_img_urls_from_sequence(person_id, perform_id):
        person_sid = 'S' + person_id.zfill(3)
        perform_sid = perform_id.zfill(3)
        
        url_list = []
        index_id = 1
        while True:
            index_sid = str(index_id).zfill(8)
            img_folder = "{}/{}/{}/{}".format(DirProcessing.dataset_root, DirProcessing.image_folder, person_sid, perform_sid)
            img_name = "{}_{}_{}.png".format(person_sid, perform_sid, index_sid)
            img_url = img_folder + '/' + img_name
            print img_url
            if not os.path.isfile(img_url): 
                break
            url_list.append(img_url)
            index_id = index_id + 1
        return url_list


