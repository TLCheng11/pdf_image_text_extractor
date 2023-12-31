import numpy as np
import cv2

def decode_img(image_file):
    # Read the image as bytes
    image_bytes = image_file.read()
    # Convert the image bytes to a numpy array
    image_np = np.frombuffer(image_bytes, np.uint8)
    # Decode the image using OpenCV
    img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    
    return img

def getSkewAngle(cvImage) -> float:
    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = cvImage.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Apply dilate to merge text into meaningful lines/paragraphs.
    # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
    # But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=2)

    # Find all contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)
    for c in contours:
        rect = cv2.boundingRect(c)
        x,y,w,h = rect
        cv2.rectangle(newImage,(x,y),(x+w,y+h),(0,255,0),2)

    # Find largest contour and surround in min area box
    largestContour = contours[0]
    # print (len(contours))
    minAreaRect = cv2.minAreaRect(largestContour)
    # cv2.imwrite("temp/boxes.jpg", newImage)
    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    if angle < -45:
        angle = 90 + angle
    return -1.0 * angle

# Rotate the image around its center
def rotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage

def numpify_image(source_image):
    return np.array(source_image)

# Deskew image
def deskew(cvImage, turn_90=False):
    angle = getSkewAngle(cvImage)
    if turn_90:
        return rotateImage(cvImage, -1.0 * angle - 90)
    else:
        return rotateImage(cvImage, -1.0 * angle)

# to adjust brightness and contrast
def adj_contrast(cvImage, contrast, brightness):
    adjusted_image = cv2.convertScaleAbs(cvImage, alpha=contrast, beta=brightness)
    return adjusted_image

# to make font bolder
def thick_font(cvImage, size=1):
    image = cv2.bitwise_not(cvImage)
    kernel = np.ones((size,size), np.int8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return image

# to make image black & white
def black_and_white(cvImage, darkness=200):
    # Convert the image to grayscale for better text enhancement
    gray = cv2.cvtColor(cvImage, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding to enhance the text
    _, thresholded = cv2.threshold(gray, darkness, 255, cv2.THRESH_BINARY)

    return thresholded