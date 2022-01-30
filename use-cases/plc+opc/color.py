from __future__ import print_function
import numpy as np 
import cv2
from object import check_maxContour 

#List of colors
colors = ['yellow','green','blue','purple']
min_hsv_color =[22,45,100,150]
max_hsv_color =[49,91,140,180]

#color tolerances in HSV color space
'''
orange 0-22
yellow 22-38
green 38-75
blue 75-130
violet 130-160
red 160-179
'''

def clean(image):
        open_kernel = np.ones((10,10),np.uint8)
        close_kernel = np.ones((3,3), np.uint8)
        image = cv2.morphologyEx(image, cv2.MORPH_OPEN, open_kernel)
        image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, close_kernel)
        return image

#return a color in string format
def set_color (col):
        for i in range(len(colors)):
                if col == colors[i]:
                        
                        return (min_hsv_color[i],max_hsv_color[i])

#return a boolean if color exists or not
def find_part(col,image):
        hsv_img= cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        #print("seting color")
        min_col,max_col = set_color(col)
       # print(min_col)
        #print(max_col)
        color_mask = cv2.inRange(hsv_img,np.array([min_col,50,120]),np.array([max_col,255,255]))
        color_mask = clean(color_mask)
        contours, _ = cv2.findContours(color_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        if len(contours)>0:
                obj = check_maxContour(contours)
                rect = cv2.minAreaRect(obj)
                box = cv2.cv.BoxPoints(rect)
                box = np.int0(box)
                #print(box)
                area=cv2.contourArea(obj)
                if area > 5000 and area < 11000:
                        #print("here")
                        return True
                else:
                        return False
        else:
                return False
        
def determine(image):
        for color in colors:
                print(color)
                status = find_part(color,image)
                print(status)
                if status == True:
                        return color
        return "None"

def wtf():
        return True

#Test unit
if __name__ == '__main__':
        col1,col2 = set_color('blue')
        print(col1)
        print(col2)
        
