import cv2
import os
import numpy as np

PASTA_TEMP = "temp"

os.makedirs(
    PASTA_TEMP,
    exist_ok=True
)

# Função que melhora qualidade de imagens
def preprocessar_imagem(caminho):

    imagem = cv2.imread(caminho)

    # Aumenta resolução
    imagem = cv2.resize(
        imagem,
        None,
        fx=1.5,
        fy=1.5,
        interpolation=cv2.INTER_CUBIC
    )

    # Redução leve de ruído
    imagem = cv2.fastNlMeansDenoisingColored(
        imagem,
        None,
        5,
        5,
        7,
        21
    )

    # Brilho e contraste
    alpha = 1.15
    beta = 8

    imagem = cv2.convertScaleAbs(
        imagem,
        alpha=alpha,
        beta=beta
    )

    # Nitidez
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])

    imagem = cv2.filter2D(
        imagem,
        -1,
        kernel
    )

    nome = os.path.basename(caminho)

    saida = os.path.join(
        PASTA_TEMP,
        f"prep_{nome}"
    )

    cv2.imwrite(
        saida,
        imagem
    )

    return saida