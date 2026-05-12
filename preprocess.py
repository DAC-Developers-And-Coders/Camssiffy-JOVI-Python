import cv2
import os

PASTA_TEMP = "resultados"


def preprocessar_imagem(caminho):

    imagem = cv2.imread(caminho)

    imagem = cv2.resize(
        imagem,
        (1280, 720)
    )

    cinza = cv2.cvtColor(
        imagem,
        cv2.COLOR_BGR2GRAY
    )

    suavizada = cv2.GaussianBlur(
        cinza,
        (5, 5),
        0
    )

    _, threshold = cv2.threshold(
        suavizada,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    nome = os.path.basename(caminho)

    saida = os.path.join(
        PASTA_TEMP,
        f"prep_{nome}"
    )

    cv2.imwrite(
        saida,
        threshold
    )

    return saida