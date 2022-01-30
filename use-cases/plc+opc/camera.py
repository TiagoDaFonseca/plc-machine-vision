import numpy as np 
import cv2
import time

def connect( channel):
        return cv2.VideoCapture(channel)

def capture_image (device,exposition):
        cam= connect(device)
        for i in range(exposition):
                ret, bgr_img = cam.read()
        cam.release()        
        return bgr_img 

#Test unit
if __name__ == '__main__':
        while True:
                img = capture_image(0,10)
                print(img)
                time.sleep(2)
                
        cv2.imshow("c",img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
