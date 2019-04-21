from PIL import Image
import numpy as np
import glob,os,sys
import cv2
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--real_image_path", required=True, help="path where are the images.")
parser.add_argument("-p", "--predict_image_path", required=True, help="path where are the images.")
parser.add_argument("-o", "--tab_detect_image_path", help="path where do you want to save detected tables images.")
parser.add_argument("-c", "--grayColor", default="RGB", help="define whether ground truth is gray or multi color labels.")
args = parser.parse_args()

#real_path = "../Final_dataset/split_1024x1024_11415/B/test"
# predict_path ="model_10274_1024px_pix2pix_AtoB/model_10274_1024px_pix2pix_AtoB/test_latest/images"

real_path = "/home/ranjith/Desktop/gtdb master/augmented_image_0-outputs"
predict_path = "/home/ranjith/Desktop/gtdb master/augmented_image_0-targets"
current_time = datetime.now().strftime("%Y-%m-%d-%H-%M")
#print args.image_path
if predict_path.endswith('/'):
	pathX = r'%s' %(predict_path[:-1])
else:
	pathX = r'%s' %(predict_path)
log_path = os.path.dirname(pathX)

log_filename = "accuracyṭ_log_"+ current_time +".txt"

#print ("Ground truth is : ", args.grayColor)?

def write_log(contents):
	with open(os.path.join(log_path, log_filename), "a") as fp:
		fp.writelines(contents + '\n')

def calc_accuracy(r_boxes, p_boxes, height, width):
	# for box in r_boxes:
	# 	for y in range(box[1],box[3]+1):
	# 		for i in range((y-1)*width+x1,(y-1)*width+x2+1):

	r_index = [i for x1,y1,x2,y2 in r_boxes for y in range(y1,y2+1)	for i in range((y-1)*width+x1,(y-1)*width+x2+1)]
	p_index = [i for x1,y1,x2,y2 in p_boxes for y in range(y1,y2+1)	for i in range((y-1)*width+x1,(y-1)*width+x2+1)]
	#print ii[0],ii[-1],len(ii)
	
	common_index = set(r_index) & set(p_index)
	print "r_index, p_index, common_index : ", len(r_index),len(p_index), len(common_index)	
	accuracy = round(float(2*len(common_index)) / float(len(r_index) + len(p_index)),5) if len(r_index)>0 or len(p_index)>0 else 1.0
	avg_accuracy.append(accuracy)
	print "accuracy : ", accuracy
	write_log("accuracy : %s" % accuracy)

def table_detect_gray(file, border_color):
	#img = Image.open(file).convert("RGB")
	img = cv2.imread(file)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(gray,127,255,0)
	_, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	height, width = gray.shape

	rects = [cv2.boundingRect(cnt) for cnt in contours]
	rects = sorted(rects,key=lambda  x:(x[2]*x[3]),reverse=True)
	rects = rects[1:len(rects)]

	x_all=[]
	found=""
	imgArea = height*width
	#mask = np.ones(img.shape[:2], dtype="uint8") * 255
	for rect in rects:
		(x,y,w,h)=rect
		if (int(imgArea*0.95) > (w*h) > int(imgArea*0.01)):
			if len(x_all)>0:
				for i in x_all:
					if (i[0]<x<i[2] and i[1]<y<i[3]):
						found=""
						break
					else:
						found="add"
			else:
				found="add"

			if found=="add":
				found=""
				cv2.rectangle(img, (x,y), (x+w,y+h), border_color, 3)
				x_all.append([x,y,x+w,y+h])				
				#print("x_all", x_all)
	
	#cv2.imwrite(os.path.join(folder + "/groundTruth", imgName.split('.')[0] + page+ '.png'), mask)
	#cv2.imwrite(os.path.join("test4", os.path.basename(file)), img)
	return x_all, height, width

def table_detect_color(file, border_color):
	#img = Image.open(file).convert("RGB")
	img = cv2.imread(file)
	#img1 = cv2.imread(file)
	h,w,c = img.shape
	#image=[[[0 0 0] for x in range(w)] for y in range(h)]
	imgR = np.reshape(img, (h*w,3))
	# imgR[imgR<200]=0
	# imgR[imgR>=200]=255
	# imgR = np.where(imgR >=200, 255, 0)
	# print imgR.dtype
	
	imgR = np.array(np.where(imgR >=200, 255, 0), dtype=np.uint8)
	# print imgR.dtype
	imgR[np.all(imgR==[255,0,0], 1)] = [255,255,255]
	imgR[np.all(imgR==[0,0,0], 1)] = [255,255,255]
	imgR[np.all(imgR!=[0,0,255], 1)] = [255,255,255]

	imgR = np.reshape(imgR, (h,w,3))
	#a=[[[255,255,255] for x in range(width)] for y in range(height) if img[x][y] != [0,0,255] else [0,0,255]]
	#cv2.imwrite(os.path.join(real_path + '/out' , os.path.basename(file)), imgR)

	gray = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(gray,127,255,0)
	_, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	height, width = gray.shape

	rects = [cv2.boundingRect(cnt) for cnt in contours]
	rects = sorted(rects,key=lambda  x:(x[2]*x[3]),reverse=True)
	rects = rects[1:len(rects)]

	x_all=[]
	found=""
	imgArea = height*width
	#mask = np.ones(img.shape[:2], dtype="uint8") * 255
	for rect in rects:
		(x,y,w,h)=rect
		if (int(imgArea*0.95) > (w*h) > int(imgArea*0.01)):
			if len(x_all)>0:
				for i in x_all:
					if (i[0]<x<i[2] and i[1]<y<i[3]):
						found=""
						break
					else:
						found="add"
			else:
				found="add"

			if found=="add":
				found=""
				cv2.rectangle(imgR, (x,y), (x+w,y+h), border_color, 2)
				x_all.append([x,y,x+w,y+h])				
				#print("x_all", x_all)
				#print os.path.join(args.tab_detect_image_path, os.path.basename(file)+str(y+h))
				#cv2.imwrite(os.path.join(args.tab_detect_image_path, str(y+h)+os.path.basename(file)), imgR)
	if args.tab_detect_image_path:
		cv2.imwrite(os.path.join(args.tab_detect_image_path, os.path.basename(file)), imgR)
	return x_all, height, width

def table_localization_accuracy(file):
	fname = os.path.basename(file)[:-4]
	if not os.path.exists(os.path.join(real_path, fname + ".png")) or not os.path.exists(os.path.join(predict_path, fname + "_synthesized_image.jpg")):
		print "Wrong file extension"
		os.system("rm " + os.path.join(log_path, log_filename))
		sys.exit(0)

	if args.grayColor=="RGB":
		r_boxes, height, width = table_detect_color(os.path.join(real_path, fname + ".png"), border_color=(0,0,0))
		p_boxes, height, width = table_detect_color(os.path.join(predict_path, fname + "_synthesized_image.jpg"), border_color=(0,0,0))
	else:
		r_boxes, height, width = table_detect_gray(os.path.join(real_path, fname + ".png"), border_color=(0,255,0))
		p_boxes, height, width = table_detect_gray(os.path.join(predict_path, fname + "_synthesized_image.jpg"), border_color=(0,0,255))
	# if args.grayColor=="RGB":
	# 	r_boxes = table_detect_color(os.path.join(real_path, file_part[0] + "_real_image.jpg"), border_color=(0,0,0))
	# 	p_boxes = table_detect_color(os.path.join(predict_path, file_part[0] + "_synthesized_image.jpg"), border_color=(0,0,0))
	# else:
	# 	r_boxes = table_detect_gray(os.path.join(real_path, file_part[0] + "_real_image.jpg"), border_color=(0,255,0))
	# 	p_boxes = table_detect_gray(os.path.join(predict_path, file_part[0] + "_synthesized_image.jpg"), border_color=(0,0,255))
	calc_accuracy(r_boxes, p_boxes, height, width)

	#sys.exit(0)

#img_seg_eval()
avg_accuracy=[]
if args.tab_detect_image_path and not os.path.exists(args.tab_detect_image_path):
	os.system('mkdir -p '+ args.tab_detect_image_path)

for i, file in enumerate(sorted(glob.glob(os.path.join(real_path, "*.*")))):
	write_log("File : %s" % (os.path.join(real_path, os.path.basename(file))))
	print "File : ", os.path.join(real_path, os.path.basename(file)), i+1
	table_localization_accuracy(file)
## calculate how much accuracy with each table of groundTruth with predicted one.
#print "Individual images accuracy : ", exact_accuracy
print "avg accuracy : ", round(sum(avg_accuracy)/len(avg_accuracy),5)

write_log("avg accuracy : %s" % (round(sum(avg_accuracy)/len(avg_accuracy),5)))
