import cv2
import os

srcPath = "/home/adeykin/projects/parking/115000004/901000011"
dstPath = "/home/adeykin/projects/parking/115000004/901000011_crop"

for filename in os.listdir(srcPath):
    #print filename
    img = cv2.imread(srcPath + '/' + filename);
    crop = img[150:,:]
    cv2.imwrite(dstPath + '/' + filename, crop)