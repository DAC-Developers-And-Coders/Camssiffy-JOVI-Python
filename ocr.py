import pytesseract
import cv2

# caminho do tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extrair_texto(img):
    # 🔥 configuração importante
    config = '--oem 3 --psm 6'

    texto = pytesseract.image_to_string(img, lang='por', config=config)

    return texto