from PIL import Image
import pytesseract
import cv2
import numpy as np

def is_pgcr(image):
    height, width, channels = image.shape
    banner_height = int((80/480)*height)
    #crop image only to area that would have Post Game Carnage Report Banner
    modified_image = image[0:banner_height, 0:width] #for 640x480 image, fixed values are image[0:80, 0:640]
    modified_image = cv2.resize(modified_image, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    #convert to grayscale for better OCR results
    modified_image = cv2.cvtColor(modified_image, cv2.COLOR_BGR2GRAY)

    #run OCR on cropped grayscale modified_image
    text = pytesseract.image_to_string(modified_image)
    return ("POSTGAME CARNAGE REPORT" in text), text

def get_scores(image, logger):
    height, width, channels = image.shape
    banner_height = int((80/480)*height)-5
    #crop image only to area that would have Post Game Carnage Report Banner
    modified_image = image[banner_height:, 0:width] #for 640x480 image, fixed values are image[0:80, 0:640]
    modified_image = cv2.resize(modified_image, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    #convert to grayscale for better OCR results
    modified_image = cv2.cvtColor(modified_image, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1, 1), np.uint8)
#    modified_image = cv2.dilate(modified_image, kernel, iterations=1)
#    modified_image = cv2.erode(modified_image, kernel, iterations=1)
    # Apply blur to smooth out the edges
#    modified_image = cv2.GaussianBlur(modified_image, (5, 5), 0)
    #modified_image = cv2.threshold(modified_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cv2.imwrite("scores.png", modified_image)
    #run OCR on cropped grayscale modified_image
    text = pytesseract.image_to_string(modified_image, config="-c tessedit_char_whitelist=0123456789RedBlue")
    logger.debug("get_scores text: {}".format(text))
    lines = text.split('\n')[0:3]
    red_score = -1
    blue_score = -1
    logger.debug("get_scores lines: {}".format(text))
    for line in lines:
        if "Red" in line:
            things = line.split(' ')
            red_score = int(things[-1])
        if "Blue" in line:
            things = line.split(' ')
            blue_score = int(things[-1])
    return red_score, blue_score
