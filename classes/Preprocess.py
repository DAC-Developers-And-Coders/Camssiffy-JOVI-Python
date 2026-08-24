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
    def iniciar_processamento_unico(self, nome_arquivo, pasta_imagens, tag_selecionada=None, tag_manager=None):
        print("Sistema iniciado\nUse CTRL+C para interromper\n")

        caminho_imagem = os.path.join(
            pasta_imagens,
            nome_arquivo
        )

        if not os.path.isfile(caminho_imagem):
            print("Arquivo Não Encontrado")
            for _ in range(20):
                time.sleep(0.1)
            return

        print(f"\nProcessando: {nome_arquivo}")
        self.processar_arquivo(nome_arquivo, caminho_imagem, tag_selecionada, tag_manager)

        print("\nProcessamento finalizado")

    # Função que inicia o processamento de todas as imagens do diretório
    def iniciar_processamento_geral(self, pasta_imagens, tag_selecionada=None, tag_manager=None):
        print("Sistema iniciado\nUse CTRL+C para encerrar\n")

        for arquivo in os.listdir(pasta_imagens):
            caminho_imagem = os.path.join(
                pasta_imagens,
                arquivo
            )

            if not os.path.isfile(caminho_imagem):
                continue

            print(f"\nProcessando: {arquivo}")
            self.processar_arquivo(arquivo, caminho_imagem, tag_selecionada, tag_manager)

        print("\nProcessamento finalizado")

    # Função que gerencia o processamento de imagens
    def processar_arquivo(self, arquivo, caminho_imagem, tag_selecionada, tag_manager=None):
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

            tags = dados.get(
                "tags"
            )

            categoria = categoria.strip()

            if categoria == "Estudo" and tag_selecionada is None:
                tag_selecionada = self.escolha_tag(tags)

            # Criação/Seleção de pastas
            name = tag_selecionada if tag_selecionada is not None else categoria

            pasta_categoria = os.path.join(
                self.PASTA_RESULTADOS,
                name
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
                    name.lower()
                    + "_"
                    + timestamp
            )

            extensao = str(os.path.splitext(
                arquivo
            )[1])

            # Caminhos finais
            imagem_original_destino = None

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

            destino = plano_de_estudos_destino
            if destino is not None:
                with open(
                        destino,
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

            #Salva imagem original, se não for de estudos
            if categoria != "Estudo":
                pasta_originais = os.path.join(
                    pasta_categoria,
                    "originais"
                )

                os.makedirs(
                    pasta_originais,
                    exist_ok=True
                )

                imagem_original_destino = os.path.join(
                    pasta_originais,
                    nome_base + extensao
                )

                shutil.copy2(
                    caminho_imagem,
                    imagem_original_destino
                )

            print(f"\nCategoria: {categoria}")
            if tag_selecionada : print(f"Tag: {tag_selecionada}")
            if imagem_original_destino : print(f"Original: {imagem_original_destino[2:]}")
            print(f"Melhorada: {imagem_melhorada_destino[2:]}")
            print(f"JSON: {json_destino[2:]}")

            if plano_de_estudos_destino is not None:
                print(f"Plano de estudos: {plano_de_estudos_destino[2:]}")

            os.remove(imagem_processada)

            if tag_manager and tag_selecionada:
                tag_manager.adicionar_tag(tag_selecionada)

                if tag_manager.ultima_tag != tag_selecionada:
                    tag_manager.ultima_tag = tag_selecionada

                tag_manager.salvar_tags()

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

    @staticmethod
    def escolha_tag(tags):
        print("\nEscolha uma tag para salvar a imagem (Digite o número de 1 a 4):")

        if tags is not None:
            for i in range(len(tags)):
                print(f"[{i + 1}] {tags[i]}")

        print("\nCaso deseje inserir uma tag manualmente, digite '0'.")

        while True:
            try:
                escolha = int(input())

                if tags is not None and 1 <= escolha <= len(tags):
                    tag_selecionada = tags[escolha - 1]
                    break
                elif escolha == 0:
                    tag_selecionada = input("\nDigite a tag desejada: ")

                    print(f"\nTag escolhida: {tag_selecionada}\nSalvamento concluído.")
                    break

                print("\nOpção inválida. Tente novamente:")
            except ValueError:
                print("\nOpção inválida. Tente novamente:")

        return tag_selecionada