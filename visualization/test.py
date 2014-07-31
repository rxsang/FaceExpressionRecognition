import cv2

import os,sys
lib_path = os.path.abspath('../utilization/')
sys.path.append(lib_path)

from file_op import FileOp

img = FileOp.read_img_file('/Users/sangruoxin/Documents/research/dataset/CK+/cohn-kanade-images/S022/001/S022_001_00000007.png')
cv2.imshow('img',img)
cv2.waitKey(0)
img = FileOp.read_img_file('/Users/sangruoxin/Documents/research/dataset/CK+/cohn-kanade-images/S022/001/S022_001_00000001.png')
cv2.imshow('img',img)
cv2.waitKey(0)
img = FileOp.read_img_file('/Users/sangruoxin/Documents/research/dataset/CK+/cohn-kanade-images/S022/001/S022_001_00000004.png')
cv2.imshow('img',img)
cv2.waitKey(0)

cv2.destroyAllWindows()
