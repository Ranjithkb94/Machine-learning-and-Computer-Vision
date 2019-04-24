import cv2
import numpy as np
from PIL import Image
import glob 
import os
import sys 

def get_original_image_name("//give folderlocation //"):
    try:
        os.chdir(folderLocation)
        listOfFile = glob.glob(sys.argv[1])
        return listOfFile
    except OSError as o:
        print("OSError: {0}".format(o))
        return []
    except:
        print("got error")
        return []

def get_gt_image_name(folderLocation=os.getcwd()+ r"\input files\\"  ):
    try:
        os.chdir(folderLocation)
        listOfFile = glob.glob(sys.argv[2])
        return listOfFile
    except OSError as o:
        print("OSError: {0}".format(o))
        return []
    except:
        print("got error")
        return []

original_img_name_list = get_original_image_name()
gt_img_name_list =  get_gt_image_name()
folderLocation=os.getcwd()
folder=os.getcwd()
save_location_1 = folderLocation+ '\Vessels'
save_location_2 = folderLocation+'\Symbols'
save_location_3 = folderLocation+'\Tabels'
if not os.path.exists(save_location_1): 
   os.makedirs(save_location_1)
if not os.path.exists(save_location_2):    
   os.makedirs(save_location_2)
if not os.path.exists(save_location_3):    
   os.makedirs(save_location_3)
counters = 0 
from scipy import misc as msc
for img_name in original_img_name_list:
	full_orig_image_path = os.path.join(folder, img_name)
	orig_image = cv2.imread(full_orig_image_path,1)
	
	full_path_gt_image = os.path.join(folder, gt_img_name_list[counters])
	print(full_path_gt_image)
	gt_image = cv2.imread(full_path_gt_image,1)
	counters += 1
	gray = cv2.cvtColor(orig_image,cv2.COLOR_BGR2GRAY)
	_, contours, heirarchy = cv2.findContours(gray, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	rects = [cv2.boundingRect(cnt) for cnt in contours]
	
	folderNameOfImages = "gtdb\\Files\\*raw.png"
	crop_counter = 0 
	for rect in rects:
		orig_crop_img = orig_image[rect[1] : rect[1] + rect[3], rect[0] : rect[0] + rect[2], :]
		if(orig_crop_img[0][0][1] == 255):
			img = gt_image[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2], :]
			save_img_name = os.path.join(save_location_1, str(crop_counter) + '_'+img_name)
			msc.imsave(save_img_name, img)
		if(orig_crop_img[0][0][1] == 100):
			img = gt_image[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2], :]
			save_img_name = os.path.join(save_location_2, str(crop_counter) + '_'+img_name)
			msc.imsave(save_img_name, img)
		if(orig_crop_img[0][0][2] == 255):
			img = gt_image[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2], :]
			save_img_name = os.path.join(save_location_3, str(crop_counter) + '_'+img_name)
			msc.imsave(save_img_name, img)
		crop_counter += 1

