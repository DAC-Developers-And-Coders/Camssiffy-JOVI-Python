import cv2
import os

def preprocessar(path, salvar=True):
    img = cv2.imread(path)

    if img is None:
        raise ValueError("Erro ao carregar imagem")
       
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (3,3), 0)

    contrast = cv2.convertScaleAbs(blur, alpha=1.3, beta=10)
    
    final = cv2.cvtColor(contrast, cv2.COLOR_GRAY2BGR)

    if salvar:
        os.makedirs('resultados', exist_ok=True)
        cv2.imwrite('resultados/debug.jpg', final)

    return final