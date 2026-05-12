import os
import json
import time

from preprocess import preprocessar_imagem
from ocr import analisar_imagem

PASTA_IMAGENS = "imagens_teste"
PASTA_RESULTADOS = "resultados"

print("Sistema iniciado")

for arquivo in os.listdir(PASTA_IMAGENS):

    caminho_imagem = os.path.join(
        PASTA_IMAGENS,
        arquivo
    )

    if not os.path.isfile(caminho_imagem):
        continue

    print(f"\nProcessando: {arquivo}")

    try:

        imagem_processada = preprocessar_imagem(
            caminho_imagem
        )

        dados = analisar_imagem(
            imagem_processada
        )

        nome_json = os.path.splitext(
            arquivo
        )[0] + ".json"

        caminho_json = os.path.join(
            PASTA_RESULTADOS,
            nome_json
        )

        with open(
            caminho_json,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                dados,
                f,
                ensure_ascii=False,
                indent=4
            )

        print("Resultado salvo")

        time.sleep(8)

    except Exception as erro:

        print(f"Erro: {erro}")