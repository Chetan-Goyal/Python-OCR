import cv2
import numpy as np
import pytesseract
from pytesseract import Output


# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

#template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED) 


# * FOR IMPROVING IMAGE
def img_enhancement():
    gray = get_grayscale(img)
    thresh = thresholding(gray)
    opening = opening(gray)
    canny = canny(gray)

# * TESTING CUSTUM CONFIGS
def special_printing_image():
    cv2.imshow('canny', canny)
    cv2.waitKey()
    custom_config = r'--oem 3 --psm 6'
    print(pytesseract.image_to_string(canny, config=custom_config))


# * FOR BOXES AROUND THE TEXT
def boxes_characters():
    h, w, c = img.shape
    boxes = pytesseract.image_to_boxes(img) 
    for b in boxes.splitlines():
        b = b.split(' ')
        img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

    cv2.imshow('img', img)
    cv2.waitKey()


# * FOR BOXES AROUND WORDS
def boxes_words(img_copy):
    d = pytesseract.image_to_data(img_copy, lang='eng', output_type=Output.DICT) 
    n_boxes = len(d['text'])
    for i in range(n_boxes):
        if int(d['conf'][i]) > 60:
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            img_copy = cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)

    print(' '.join(d['text']))

    cv2.imshow('img', img_copy)
    cv2.waitKey()


# * Image Orientation
def img_oriented(image):
    import re
    osd = pytesseract.image_to_osd(image)
    angle = osd.splitlines()[2].split()[1]
    script = osd.splitlines()[4].split()[1]

    print("angle: ", angle)
    print("script: ", script)

    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
 
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -int(angle), 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
 
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
 
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
 
    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))
    
if __name__ == "__main__":
    img = cv2.imread('Sample_Images/rotated.png')
    img_copy = img_oriented(img)
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
    boxes_words(img_copy)