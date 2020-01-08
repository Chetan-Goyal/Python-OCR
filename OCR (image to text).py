'''
Prerequistics      : tesseract software (freeware)
Required Libraries : Image , pytesseract
Motive             : To make a simple ocr program(image to text) in python with help of pytesseract
varible used       : file_path -> location of the image (source to read text)
'''

from PIL import Image
# importing Image module for opening image file

import pytesseract
# importing pytesseract module for calling of image_to_string function

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
# If getting errors, add the above command with path of the tesseract executable here.(It would be quite similar to above path)

file_path = 'Sample_Images/test.png'
# location of the sample image

text = pytesseract.image_to_string(Image.open(file_path))
# calling image_to_string function of pytesseract module to extract the text

print(text)
# displaying the extracted text