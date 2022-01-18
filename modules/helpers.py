import cv2
import imutils
import numpy as np


#it outputs the contour with the largest area
def check_maxContour (contours):
    return max(contours, key=cv2.contourArea)


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
	return rect[0][0],rect[0][1]


#Checks if the image is inverted 
def is_inverted (image):
    #Control variables
    min_thresh = 80
    max_thresh = 255
    ret, thresh = create_BW_image (image, min_thresh, max_thresh)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnt=check_maxContour (contours)
    rect = cv2.minAreaRect(cnt)
    xi,yi = rect_point(cnt)
    box = fit_rectangle (cnt)
    cv2.drawContours(image,[box],0,(0,255,0),2)
    
    inverted = imutils.rotate_bound(image,180)
    
    ret, thresh = create_BW_image (inverted, min_thresh, max_thresh)
    contours1, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnt1=check_maxContour (contours1)
    xf,yf = rect_point(cnt1)
    box = fit_rectangle (cnt1)
    cv2.drawContours(inverted,[box],0,(0,0,255),2)
    if yf>yi:
        return True
    else:
        return False


#crop the number region 
def number_extraction (image):
    min_thresh = 80
    max_thresh = 255
    ret, thresh1 = create_BW_image (image, min_thresh, max_thresh)
    contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnt=check_maxContour (contours)
    box = fit_rectangle (cnt)
    cv2.drawContours(image,[box],0,(255,0,0),2)
    #Box points
    point0 = box[0]
    point1 = box[1]
    point2 = box[2]
    point3 = box[3]
    return image[:point1[1],point1[0]:point2[0]]


class Camera():
    def __init__(self, channel=3):
        self.cam = cv2.VideoCapture(channel)
    
    def catch_frame(self):
        for i in range(10):
            _, frame = self.cam.read()
        return  frame
    
    def is_connected(self):
        return self.cam.isOpened()


# TEST UNIT
if __name__ == "__main__":
    cam=Camera()
    
    
