#--------------------------------------------------------------------------------------
# Optical character recognition algorithm
#
# Author: T. Cunha 
#
# Introsys S.A.
#
#----------------------------------------------------------------------------------------
#Control variables
min_thresh = 180
max_thresh = 255


#Modules
import cv2
import time
import numpy as np
import imutils
import pytesseract
import os

#----------------------------------------------------------------------------------------
#Functions
#----------------------------------------------------------------------------------------

#it outputs the contour with the largest area
def check_maxContour (contours):
	rect_index = 0
	max_area = 0
	for index in range(len(contours)):
		area = cv2.contourArea(contours[index])
		if area > max_area:
			max_area = area
			rect_index = index
	return contours[rect_index]

#Creates a black and White image in 8uCi format through binarization method
def create_BW_image (image, min_thresh, max_thresh):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	return cv2.threshold(gray,min_thresh,max_thresh,cv2.THRESH_BINARY)

# fits a rectangle and oputputs diamsions 
def fit_rectangle (contour):
	rect = cv2.minAreaRect(contour)
	box = cv2.cv.BoxPoints(rect)
	return np.int0(box)

#outputs the rectangle angle orientation
def determine_angle (contour):
	rect = cv2.minAreaRect(contour)
	width = rect[1][0]
	height = rect[1][1]

	angle = rect[2]

	if width < height:
		angle = angle - 90 
	return angle

#outputs the top-left corner of the rectangle 
def rect_point (contour):
	rect = cv2.minAreaRect(contour)
	#print(rect)
	return rect[0][0],rect[0][1]

#Checks if the image is inverted 
def is_inverted (image):
	ret, thresh = create_BW_image (image, min_thresh, max_thresh)
	contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	cnt=check_maxContour (contours)
	rect = cv2.minAreaRect(cnt)
	xi,yi = rect_point(cnt)
	box = fit_rectangle (cnt)
	cv2.drawContours(image,[box],0,(0,255,0),2)
	#cv2.imshow("rotated", image)
	#cv2.waitKey(0)

	inverted = imutils.rotate_bound(image,180)

	ret, thresh = create_BW_image (inverted, min_thresh, max_thresh)
	contours1, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	cnt1=check_maxContour (contours1)
	xf,yf = rect_point(cnt1)
	box = fit_rectangle (cnt1)
	cv2.drawContours(inverted,[box],0,(0,0,255),2)
	#cv2.imshow("inv", inverted)
	#cv2.waitKey(0)

	if yf>yi:
		return True
	else:
		return False

#Connects to camera via USB
def connect_to_camera ():
	return cv2.VideoCapture(0)

#Grab image: acquires ten images e returns only the last one.
def catch_frame (camera):
	for i in range(10):
		ret, frame = camera.read()
		#cv2.imshow("frame",frame)
		#cv2.waitKey(0)
	return  frame

#OCR
def image_to_string(image):
	return pytesseract.image_to_string(image, config = '-psm 10 -c tessedit_char_whitelist=0123456789')

#crop the number region 
def number_extraction (image):
	ret, thresh1 = create_BW_image (image, min_thresh, max_thresh)
	contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	cnt=check_maxContour (contours)
	box = fit_rectangle (cnt)
	cv2.drawContours(image,[box],0,(255,0,0),2)
	#cv2.imshow("Final", image)
	#cv2.waitKey(0)
	
	#Box points
	point0 = box[0]
	point1 = box[1]
	point2 = box[2]
	point3 = box[3]

	return image[50:point1[1],point1[0]:point2[0]]

#Close windows
def exit():
	cv2.waitKey(1)
	cv2.destroyAllWindows()
	cv2.waitKey(1)

#------------------------------------------------------------------------------------------
# Main Function
#------------------------------------------------------------------------------------------

#image analysis to number recognition as output
def read_number (camera):
	
	#grab image
	frame = catch_frame(camera)
	
	#cv2.imshow("imagem",frame)
	#cv2.waitKey(0)

	#setting up
	crop = frame[40:250,230:450]
	#cv2.imshow("crop",crop)
	#cv2.waitKey(0)
	ret, thresh = create_BW_image (crop, min_thresh, max_thresh)
	#cv2.imshow("bin",thresh)
	#cv2.waitKey(0)

	try:
		contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		
		#Looking for the ref rectangle
		cnt = check_maxContour (contours)
		box = fit_rectangle (cnt)

		#Determine angle orientation
		angle = determine_angle (cnt)

		#Align number with horizontal axis
		rotated = imutils.rotate(crop,angle)

		#Check if image is inverted and if so, rotate by 180 deg
		if is_inverted (rotated) == True:
		#if True:
			final = imutils.rotate(crop,angle+180)
		else:
			final = imutils.rotate(crop, angle)

		#Number selection region
		num_selec = number_extraction (final)
		#cv2.imshow("number", num_selec)
		#cv2.waitKey(0)
	
		#Number recognition
		ret, thresh2 = create_BW_image (num_selec, min_thresh, max_thresh)

		return image_to_string(thresh2)
	except:
		print("<<< No digit detected")
		return -1

#-------------------------------------------------------------------------------------------
#Test Unit
#-------------------------------------------------------------------------------------------
if __name__ == "__main__":
	
	
	#Connect camera 
	cam = connect_to_camera()
	
	#Check if is opened
	if not cam.isOpened():
		print("<<< Error Message: Camera not OK. Trying to open...")
		try:
			cam.open()
			print("Camera opened")
		except:
			print("<<< Error connecting")
	
	try:	
	#Reading number
		number = read_number(cam)
	#Outputs number
		if number != '':
			print("number:" + number)
		else:
			print("<<< No number recognized in picture")
	except:
		print("<<< Error Message: Reading number failure")
		print("")#new line

	exit()

