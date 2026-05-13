import os
import sys
import time
import json
import shutil
import keyboard
import threading

from datetime import datetime

from preprocess import preprocessar_imagem
from ocr import analisar_imagem

PASTA_IMAGENS = "imagens_teste"
PASTA_RESULTADOS = "resultados"

def encerrar():
    keyboard.wait("e")

    print("Sistema encerrado.")
    sys.stdout.flush()
    os._exit(0)

print("Sistema iniciado\nPressione 'E' para encerrar.")

threading.Thread(target=encerrar, daemon=True).start()

for arquivo in os.listdir(PASTA_IMAGENS):
    caminho_imagem = os.path.join(
        PASTA_IMAGENS,
        arquivo
    )

    if not os.path.isfile(caminho_imagem):
        continue

    print(f"\nProcessando: {arquivo}")

    try:
        # Preprocessa imagem
        imagem_processada = preprocessar_imagem(
            caminho_imagem
        )

        # Analisa imagem
        dados = analisar_imagem(
            imagem_processada
        )

        categoria = dados.get(
            "categoria",
            "Outros"
        )

        categoria = categoria.strip()

        # Pastas
        pasta_categoria = os.path.join(
            PASTA_RESULTADOS,
            categoria
        )

        pasta_originais = os.path.join(
            pasta_categoria,
            "originais"
        )

        pasta_melhoradas = os.path.join(
            pasta_categoria,
            "melhoradas"
        )

        pasta_json = os.path.join(
            pasta_categoria,
            "json"
        )

        os.makedirs(
            pasta_originais,
            exist_ok=True
        )

        os.makedirs(
            pasta_melhoradas,
            exist_ok=True
        )

        os.makedirs(
            pasta_json,
            exist_ok=True
        )

        # Timestamp
        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        nome_base = (
            os.path.splitext(arquivo)[0]
            + "_"
            + timestamp
        )

        extensao = os.path.splitext(
            arquivo
        )[1]

        # Caminhos finais
        imagem_original_destino = os.path.join(
            pasta_originais,
            nome_base + extensao
        )

        imagem_melhorada_destino = os.path.join(
            pasta_melhoradas,
            nome_base + extensao
        )

        json_destino = os.path.join(
            pasta_json,
            nome_base + ".json"
        )

        # Copia imagem original
        shutil.copy2(
            caminho_imagem,
            imagem_original_destino
        )

        # Copia imagem preprocessada
        shutil.copy2(
            imagem_processada,
            imagem_melhorada_destino
        )

        # Salva JSON
        with open(
            json_destino,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                dados,
                f,
                ensure_ascii=False,
                indent=4
            )

        print(
            f"Categoria: {categoria}"
        )

        print(
            f"Original: {imagem_original_destino}"
        )

        print(
            f"Melhorada: {imagem_melhorada_destino}"
        )

        print(
            f"JSON: {json_destino}"
        )

        os.remove(imagem_processada)

        for _ in range(100):
            time.sleep(0.1)

    except Exception as erro:

        print(f"Erro: {erro}")

print("Processamento finalizado")