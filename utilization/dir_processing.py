from __future__ import with_statement
import ConfigParser
import os
import re

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
    def get_id_from_url(url):
        name = os.path.basename(url)
        person_id = name[1:4]
        perform_id = name[5:8]
        index_id = name[9:17]

        return person_id, perform_id, index_id
   
    @staticmethod
    def get_id_from_img_url(img_url):
        return DirProcessing.get_id_from_url(img_url)

    @staticmethod
    def get_id_from_landmarks_url(landmarks_url):
        return DirProcessing.get_id_from_url(landmarks_url)

    @staticmethod
    def get_id_from_label_url(label_url):
        return DirProcessing.get_id_from_url(label_url)
    
    @staticmethod
    def generate_label_url_from_img_url(img_url):
        person_id, perform_id, index_id = DirProcessing.get_id_from_img_url(img_url)
        label_url = DirProcessing.generate_label_url(person_id, perform_id, index_id)

        return label_url

    @staticmethod
    def generate_landmarks_url_from_img_url(img_url):
        person_id, perform_id, index_id = DirProcessing.get_id_from_img_url(img_url)
        landmarks_url = DirProcessing.generate_landmarks_url(person_id, perform_id, index_id)

        return landmarks_url

    @staticmethod
    def generate_img_url_from_landmarks_url(landmarks_url):
        person_id, perform_id, index_id = DirProcessing.get_id_from_landmarks_url(landmarks_url)
        img_url = DirProcessing.generate_img_url(person_id, perform_id, index_id)

        return img_url

    @staticmethod
    def get_label_url_from_landmarks_url(landmarks_url):
        person_id, perform_id, index_id = DirProcessing.get_id_from_landmarks_url(landmarks_url)
        label_url = DirProcessing.get_label_url_from_sequence(person_id, perform_id)

        return label_url

    @staticmethod
    def generate_img_urls_from_landmarks_urls(landmarks_urls):
        img_urls = []
        for landmarks_url in landmarks_urls:
            img_url = DirProcessing.generate_img_url_from_landmarks_url(landmarks_url)
            img_urls.append(img_url)

        return img_urls


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

    @staticmethod
    def get_all_landmarks_urls_from_sequence(person_id, perform_id):
        person_sid = 'S' + person_id.zfill(3)
        perform_sid = perform_id.zfill(3)
        
        url_list = []
        index_id = 1
        while True:
            index_sid = str(index_id).zfill(8)
            landmarks_folder = "{}/{}/{}/{}".format(DirProcessing.dataset_root, DirProcessing.landmarks_folder, person_sid, perform_sid)
            landmarks_name = "{}_{}_{}_landmarks.txt".format(person_sid, perform_sid, index_sid)
            landmarks_url = landmarks_folder + '/' + landmarks_name
            if not os.path.isfile(landmarks_url): 
                break
            url_list.append(landmarks_url)
            index_id = index_id + 1
        return url_list

    @staticmethod
    def get_label_url_from_sequence(person_id, perform_id):
        person_sid = 'S' + person_id.zfill(3)
        perform_sid = perform_id.zfill(3)

        root_sequence_folder = os.path.join(DirProcessing.dataset_root, DirProcessing.label_folder, person_sid, perform_sid)

        if not os.path.exists(root_sequence_folder):
            return None

        f = os.listdir(root_sequence_folder)

        if not f:
            return None
        else:
            return os.path.join(root_sequence_folder, f[0])

    @staticmethod
    def get_location_from_sequence(landmarks_url, sel_num):
        """ get the location of the landmarks url in the sequence, the fisrt url is taken
        as the neural expression, return "START". The middle urls are discarded, return "MIDDLE". 
        The last sel_num urls are taken as the expression for the sequence, return "LAST". """

        person_id, perform_id, index_id = DirProcessing.get_id_from_landmarks_url(landmarks_url)

        person_sid = 'S' + person_id.zfill(3)
        perform_sid = perform_id.zfill(3)

        root_sequence_folder = os.path.join(DirProcessing.dataset_root, DirProcessing.landmarks_folder, person_sid, perform_sid)
        f = os.listdir(root_sequence_folder)

        total_num = len(f)

        if int(index_id) <= 1:
            return "START"
        elif int(index_id) > total_num - sel_num:
            return "LAST"
        else:
            return "MIDDLE"
        
        
    @staticmethod
    def get_all_person_ids():
        root_img_folder = "{}/{}".format(DirProcessing.dataset_root, DirProcessing.image_folder)
        files = os.listdir(root_img_folder)
        person_ids = []

        for f in files:
            if re.match("S\d{3}", f):
                person_ids.append(f[1:])

        return person_ids

    @staticmethod
    def get_all_perform_ids_from_person_id(person_id):
        person_sid = 'S' + person_id.zfill(3)
        root_person_folder = "{}/{}/{}".format(DirProcessing.dataset_root, DirProcessing.image_folder, person_sid)
        files = os.listdir(root_person_folder)
        perform_ids = []

        for f in files:
            if re.match("\d{3}", f):
                perform_ids.append(f)

        return perform_ids
