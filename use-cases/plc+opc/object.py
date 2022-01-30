import numpy as np 
import cv2


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

#if __name__ == '__main__':

