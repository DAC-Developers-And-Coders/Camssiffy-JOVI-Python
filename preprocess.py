import cv2
import os

def preprocessar(path, salvar=True):
    img = cv2.imread(path)

    if img is None:
        raise ValueError("Erro ao carregar imagem")
    
    # 🔥 escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 50, 150)

    # 🔥 leve suavização (mantém detalhes)
    blur = cv2.GaussianBlur(gray, (3,3), 0)

    # 🔥 leve aumento de contraste (SEM exagero)
    contrast = cv2.convertScaleAbs(blur, alpha=1.3, beta=10)

    # 🔥 voltar pra 3 canais
    final = cv2.cvtColor(contrast, cv2.COLOR_GRAY2BGR)

    if salvar:
        os.makedirs('resultados', exist_ok=True)
        cv2.imwrite('resultados/debug.jpg', final)

    return final