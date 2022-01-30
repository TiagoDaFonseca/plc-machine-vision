from __future__ import print_function
import numpy as np
import cv2

#it outputs the contour with the largest area
def check_maxContour (contours):
	if len(contours) == 0:
		return -1
	else:
		rect_index = 0
		max_area = 0
		for index in range(len(contours)):
			area = cv2.contourArea(contours[index])
			if area > max_area:
				max_area = area
				rect_index = index
		return contours[rect_index]


cam = cv2.VideoCapture(0)
for i in range(10):

	ret, bgr_img = cam.read()

cv2.imshow("cam",bgr_img)
cv2.waitKey(0)
hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)
#print(bgr_img.shape)
#color tolerances in HSV color space
'''
orange 0-22
yellow 22-38
green 38-75
blue 75-130
violet 130-160
red 160-179
'''

#Detecting blue
color_mask = cv2.inRange(hsv_img,np.array([0,0,0]), np.array([35,255,255]))

#detecting green
#color_mask = cv2.inRange(hsv_img, np.array([45,100,200]),np.array([75,255,255]))

#detecting orange
#color_mask = cv2.inRange(hsv_img, np.array([0,10,10]), np.array([22,255,255]))

open_kernel = np.ones((10,10),np.uint8)
close_kernel = np.ones((3,3), np.uint8)
color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_OPEN, open_kernel)
color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_CLOSE, close_kernel)

#print(color_mask.shape)

#plotting
#cv2.imshow("mask",color_mask)


#convergence of the results
result = cv2.bitwise_and(bgr_img,bgr_img,mask=color_mask)
contours, hierarchy = cv2.findContours(color_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#print(len(contours))

#Looking for the ref rectangle
if len(contours)>0: 
	obj = check_maxContour (contours)
	rect = cv2.minAreaRect(obj)
	box = cv2.cv.cv.BoxPoints(rect)
	box = np.int0(box)
	print(box)
	area = cv2.contourArea(obj)
	#print(area)
#IS there a blue object present?
	if area > 95 and area < 105000:
		print(True)
		print (area)
		print("A peca azul esta presente")
	else:
		print(False)
		print("Peca errada")
	cv2.drawContours(result,[box],0,(255,0,0),3)

else:
	print(False)
	print("A peca azul nao esta no tabuleiro")

cv2.imshow("blue",result)
cv2.waitKey(0)
cv2.imwrite('peca.png',bgr_img)

