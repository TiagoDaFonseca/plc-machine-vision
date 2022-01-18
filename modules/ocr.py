import pytesseract
from modules.helpers import *
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(name="OCR")


#OCR
def image_to_string(image):
    return pytesseract.image_to_string(image, config = '-psm 10 -c tessedit_char_whitelist=0123456789')


class Inspection():
    def __init__(self):
        pass
    
    def read_number(self):
        #grab image
        cam = Camera()
        frame = cam.catch_frame()
        
        #setting up
        crop = frame[300:,:250]
        _, thresh = create_BW_image (crop, 80, 255)
        
        try:
            contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            #Looking for the ref rectangle
            cnt = check_maxContour (contours)
            box = fit_rectangle (cnt)
		    #Determine angle orientation
            angle = determine_angle (cnt)
            #Align number with horizontal axis 
            rotated = imutils.rotate(crop,angle)
            # Check if image is inverted and if so, rotate by 180 deg
            if is_inverted (rotated) == True:
                final = imutils.rotate(crop,angle+180)
            else:
                final = imutils.rotate(crop, angle)

		    #Number selection region
            num_selec = number_extraction(final)
		    #Number recognition
            _, thresh2 = create_BW_image(num_selec, 80, 255)
            return image_to_string(thresh2)
        except:
            print("<<< No digit detected")
            return -1

