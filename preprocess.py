import cv2

def preprocessar(img_path):
    img = cv2.imread(img_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BRG2GRAY)

    blur = cv2.GaussianBlur(gray, (5,5), 0)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    contrast = clahe.apply(blur)

    return contrast