import os
import numpy as np
from doctr.models import ocr_predictor
import cv2
from datetime import datetime
import regex as re
from classification import docClassification


format = "%d/%m/%Y"
# import matplotlib.pyplot as plt
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Let's pick the desired backend
os.environ['USE_TF'] = '1'
# os.environ['USE_TORCH'] = '1'

predictor = ocr_predictor(det_arch='linknet_resnet18_rotation',
                          reco_arch='crnn_vgg16_bn', pretrained=True, assume_straight_pages=False)


datepatn = r'\d+[-/]\d+[-/]\d+'
panpatn = r'([A-Z]){5}([O0-9]){4}([A-Z]){1}'
namepatn = r'([A-Z]+)\s([A-Z]+)\s([A-Z]+)'
fnamepatn = r'([A-Z]+)\s+?'
godpatn = r'([A-Z]+)\s([A-Z]+)\s([A-Z]+)$|([A-Z]+)\s([A-Z]+)$'


def grayscale(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

# https://becominghuman.ai/how-to-automatically-deskew-straighten-a-text-image-using-opencv-a0c30aed83df


def getSkewAngle(cvImage) -> float:
    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = cvImage.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Apply dilate to merge text into meaningful lines/paragraphs.
    # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
    # But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=2)

    # Find all contours
    contours, hierarchy = cv2.findContours(
        dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    for c in contours:
        rect = cv2.boundingRect(c)
        x, y, w, h = rect
        cv2.rectangle(newImage, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Find largest contour and surround in min area box
    largestContour = contours[0]
    # print(len(contours))
    minAreaRect = cv2.minAreaRect(largestContour)
    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    if angle < -45:
        angle = 90 + angle
    if angle != 90:
        angle = 90 - angle
    return -1.0 * angle


def rotate_image_stack(mat, angle):
    """
    Rotates an image (angle in degrees) and expands image to avoid cropping
    """

    height, width = mat.shape[:2]  # image shape has 3 dimensions
    # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape
    image_center = (width/2, height/2)

    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)

    # rotation calculates the cos and sin, taking absolutes of those.
    abs_cos = abs(rotation_mat[0, 0])
    abs_sin = abs(rotation_mat[0, 1])

    # find the new width and height bounds
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    # subtract old image center (bringing image back to origo) and adding the new image center coordinates
    rotation_mat[0, 2] += bound_w/2 - image_center[0]
    rotation_mat[1, 2] += bound_h/2 - image_center[1]

    # rotate image with the new bounds and translated rotation matrix
    rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))
    return rotated_mat

# Deskew image


def deskew(cvImage):
    angle = getSkewAngle(cvImage)
    print("\nAngle: ", angle, "\n")
    height, width = cvImage.shape[:2]
    # print("angle: ",angle)
    if (angle != -90 or (angle == -90 and height > width)):
        rotated_image = rotate_image_stack(cvImage,  angle)
    else:
        rotated_image = cvImage
    return rotated_image


def isDate(date):
    res = True
    try:
        res = bool(datetime.strptime(date, format))
    except ValueError:
        res = False
    return res

# Reference : pan-aadhar-ocr library


def find_adhar_number(ocr_text):
    """Function to find adhar number inside the image

    Args:
    ocr_text (list): text from the ocr

    Returns:
    str: 12 digit aadhaar number
    """
    adhar_number_patn = '[0-9]{4}\s[0-9]{4}\s[0-9]{4}'
    match = re.search(adhar_number_patn, ocr_text)
    if match:
        return match.group()


def find_name(ocr_text):
    """Function to find adhar name inside the image

    Args:
    ocr_text (list): text from the ocr

    Returns:
    str: name on the aadhar card
    """
    adhar_name_patn = r'[A-Z][a-z]+\s[A-Z][a-z]+(\s[A-Z][a-z]+)?'
    match = re.search(adhar_name_patn, ocr_text)
    if match:
        return (match.group()).rstrip()


def find_dob(ocr_text):
    """Function to find date of birth inside the image

    Args:
    ocr_text (list): text from the ocr

    Returns:
    str: Date of birth
    """
    dob_patn = '\d+[-/]\d+[-/]\d+'
    yob_patn = '[0-9]{4}'
    DateOfBirth = ''
    try:
        if 'Year of Birth' in ocr_text:
            match = re.search(yob_patn, ocr_text)
            DateOfBirth = match.group()
        else:
            match = re.search(dob_patn, ocr_text)
            DateOfBirth = match.group()
    except:
        DateOfBirth = 'Nan'
    return DateOfBirth


def find_gender(ocr_text):
    """Function to find Gender inside the image

    Args:
    ocr_text (list): text from the ocr

    Returns:
    str: Gender
    """
    if 'Female' in ocr_text or 'FEMALE' in ocr_text:
        GENDER = 'Female'
    elif 'Male' in ocr_text or 'MALE' in ocr_text:
        GENDER = 'Male'
    elif 'Transgender' in ocr_text or 'TRANSGENDER' in ocr_text:
        GENDER = 'Transgender'
    else:
        GENDER = 'NAN'
    return GENDER


def postProcess(json_result):
    textExtracted = ""
    for count, block in enumerate(json_result["pages"][0]["blocks"]):
        for lineCount, line in enumerate(block["lines"]):
            for wordCount, word in enumerate(line["words"]):
                # if (word["confidence"] > 0.3):
                # if (word["confidence"] > 0.5 and word["value"].isalnum() == True):
                textExtracted += (word["value"] + " ")
            textExtracted = textExtracted.rstrip()
            textExtracted += '\n'
    return textExtracted


def ocr_image(img, flag=0):
    data = {}
    rotFlag = 1

    rotated_img = deskew(img)
    result = predictor([rotated_img])
    json_result = result.export()
    textExtracted = postProcess(json_result)
    print(textExtracted)
    docType = docClassification(textExtracted)
    print("Doc Type ", docType, "\n\n")
    if docType <= 1:
        # rotated_img = rotate_image_stack(rotated_img, 180)
        # result = predictor([rotated_img])
        # json_result = result.export()
        # textExtracted = postProcess(json_result)
        data = aadhar_extract(textExtracted)
    else:
        # if docType == 3:
        #     rotated_img = rotate_image_stack(rotated_img, 180)
        #     result = predictor([rotated_img])
        #     json_result = result.export()
        #     textExtracted = postProcess(json_result)
        data = pan_extract(textExtracted)
    return [data, rotated_img]


def aadhar_extract(textExtracted, flag=0):
    # if (flag == 0):
    #     words = textExtracted.split(" ")
    #     for word in words:
    #         if (word.isdigit() == True and len(word) == 4):
    #             # Check if the image is 180 degrees rotated
    #             if (words.index(word) <= len(words)/2 and rotFlag):
    #                 rotFlag = 0
    #                 correctImg = rotate_image_stack(rotated_img, 180)
    #                 print("Rotating")
    #                 return ocr_image(correctImg, 1)
    data = {}
    data['docType'] = 'Aadhar'
    data['dob'] = find_dob(textExtracted)
    data['name'] = find_name(textExtracted)
    data['gender'] = find_gender(textExtracted)
    data['aadharNumber'] = find_adhar_number(textExtracted)
    return data


def pan_extract(textExtracted, flag=0):
    PAN = 'NAN'
    Name = 'NAN'
    FatherName = 'NAN'
    DOB = 'NAN'
    # print(OCR_text)
    textExtracted = textExtracted.split('\n')
    gov = [i for i, txt in enumerate(textExtracted) if 'GOVT' in txt][0]
    OCR_text = textExtracted[gov + 1:]
    temp = []
    for text in OCR_text:
        name = re.search(godpatn, text)
        # print(name.group())
        if name:
            temp.append(name.group())

    # # Handle 'O's in Digits
    # temp = ''
    # for i, char in enumerate(PAN):
    #     if i > 4 and i < 9:
    #         if char == 'O':
    #             char = '0'
    #     temp = temp+char
    # PAN = temp
    # # print(PAN)
    if len(temp) >= 1:
        Name = temp[0]
    if (len(temp) > 1):
        FatherName = temp[1]

    for text in OCR_text:
        if re.search(panpatn, text):
            PAN = re.search(panpatn, text).group()
            break

    for text in OCR_text:
        if re.search(datepatn, text):
            DOB = re.search(datepatn, text).group()
            break

    data = {
        'docType': 'PAN',
        'Pan_number': PAN,
        'Name': Name,
        'Father_Name': FatherName,
        'DOB': DOB
    }
    return data


def ocr_ner(img):
    # rotated_img = deskew(img)
    rotated_img = img
    result = predictor([rotated_img])
    json_result = result.export()
    textExtracted = postProcess(json_result)
    file = open("extractedOCR.txt", "w")
    a = file.write(textExtracted)
    file.close()
    return textExtracted


if __name__ == "__main__":
    img = cv2.imread("./test_imgs/pan_6.png")
    img = grayscale(img)
    print(ocr_ner(img))
