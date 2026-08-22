import numpy as np
from datetime import datetime
import os, cv2, time, json, shutil

from classes.OCR import OCR

class Preprocess:
    PASTA_TEMP = "temp"
    PASTA_RESULTADOS = "./resultados"

    ocr = None

    def __init__(self):
        os.makedirs(
            self.PASTA_TEMP,
            exist_ok=True
        )

        self.ocr = OCR()

    # Função que inicia o processamento de uma imagem específica do diretório
    def iniciar_processamento_unico(self, nome_arquivo, PASTA_IMAGENS):
        print("Sistema iniciado\nUse CTRL+C para encerrar\n")

        caminho_imagem = os.path.join(
            PASTA_IMAGENS,
            nome_arquivo
        )

        if not os.path.isfile(caminho_imagem):
            print("Arquivo Não Encontrado")
            for _ in range(30):
                time.sleep(0.1)
            return

        print(f"\nProcessando: {nome_arquivo}")
        self.processar_arquivo(nome_arquivo, caminho_imagem)

        print("\nProcessamento finalizado")

    # Função que inicia o processamento de todas as imagens do diretório
    def iniciar_processamento_geral(self, PASTA_IMAGENS):
        print("Sistema iniciado\nUse CTRL+C para encerrar\n")

        for arquivo in os.listdir(PASTA_IMAGENS):
            caminho_imagem = os.path.join(
                PASTA_IMAGENS,
                arquivo
            )

            if not os.path.isfile(caminho_imagem):
                continue

            print(f"\nProcessando: {arquivo}")
            self.processar_arquivo(arquivo, caminho_imagem)

        print("\nProcessamento finalizado")

    # Função que gerencia o processamento de imagens
    def processar_arquivo(self, arquivo, caminho_imagem):
        try:
            # Preprocessa imagem
            imagem_processada = self.preprocessar_imagem(
                caminho_imagem
            )

            # Analisa imagem
            dados = self.ocr.analisar_imagem(
                imagem_processada
            )

            categoria = dados.get(
                "categoria",
                "Outros"
            )

            plano_de_estudos = dados.get(
                "plano_estudos"
            )

            categoria = categoria.strip()

            # Criação/Seleção de pastas
            pasta_categoria = os.path.join(
                self.PASTA_RESULTADOS,
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

            if plano_de_estudos is not None:
                pasta_plano_de_estudos = os.path.join(
                    pasta_categoria,
                    "planos_de_estudos"
                )

                os.makedirs(
                    pasta_plano_de_estudos,
                    exist_ok=True
                )
            else:
                pasta_plano_de_estudos = None

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
                    categoria.lower()
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

            if pasta_plano_de_estudos is not None:
                plano_de_estudos_destino = os.path.join(
                    pasta_plano_de_estudos,
                    nome_base + ".txt"
                )
            else:
                plano_de_estudos_destino = None

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

            if plano_de_estudos_destino is not None:
                with open(
                        plano_de_estudos_destino,
                        "w",
                        encoding="utf-8"
                ) as f:
                    f.write(
                        json.dumps(
                            plano_de_estudos,
                            ensure_ascii=False,
                            indent=4
                        )
                    )

            print(
                f"Categoria: {categoria}"
            )

            print(
                f"Original: {imagem_original_destino[2:]}"
            )

            print(
                f"Melhorada: {imagem_melhorada_destino[2:]}"
            )

            print(
                f"JSON: {json_destino[2:]}"
            )

            if plano_de_estudos_destino is not None:
                print(
                    f"Plano de estudos: {plano_de_estudos_destino[2:]}"
                )

            os.remove(imagem_processada)

            for _ in range(50):
                time.sleep(0.1)
        # Envia a interrupção pelo CTRL + C
        except KeyboardInterrupt:
            raise
        except Exception as erro:
            print(f"Erro: {erro}")

    def preprocessar_imagem(self, caminho):
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
            self.PASTA_TEMP,
            f"prep_{nome}"
        )

        cv2.imwrite(
            saida,
            imagem
        )

        return saida