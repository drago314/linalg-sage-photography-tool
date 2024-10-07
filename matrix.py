from PIL import Image
import pytesseract
import glob
import os.path
import cv2
import pyperclip as pc

options = "--psm 6"

# find most recently edited file on the desktop
folder_path = r"/Users/avrickaltmann/Documents/Screenshots/"
file_type = r"*png"
files = glob.glob(folder_path + file_type)
filename = max(files, key=os.path.getctime)

img = cv2.imread(filename)
threshold = 50
_, img_binarized = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
pil_img = Image.fromarray(img_binarized)
#pil_img.show()
text = pytesseract.image_to_string(pil_img, config=options)

print(text)
matrix = []
line = []
number = ""
negative = False
for char in text:
    # me doing stupid debugging
    if char == "l":
        char = '1'

    # actual logic
    if char == "\n":
        if number != "":
            result = int(number)
            number = ""
            if negative:
                result *= -1
                negative = False
            line.append(result)
        matrix.append(line.copy())
        line = []
    elif char.isdigit():
        number += char
    elif char == " " and number != "":
        result = int(number)
        number = ""
        if negative:
            result *= -1
            negative = False
        line.append(result)
    elif char == "-" or char == "—":
        negative = True

result = "A = matrix([("
for row in matrix:
    for num in row:
        result += str(num)
        result += ", "
    result = result[:-2]
    result += "), ("
result = result[:-3]
result += "])"

pc.copy(result)