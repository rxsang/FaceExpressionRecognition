from __future__ import with_statement
import ConfigParser

config = ConfigParser.ConfigParser()
with open('../config/config.ini','rw') as cfgfile:
    config.readfp(cfgfile)
dataset_root = config.get('directory','dataset_root')
label_folder = config.get('directory','label_folder')
landmark_folder = config.get('directory','landmark_folder')

import os
print os.listdir(dataset_root)
