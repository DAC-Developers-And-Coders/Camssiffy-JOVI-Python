import numpy as np
import os, cv2, time

from classes.OCR import OCR
from classes.Armazenamento.ArmazenamentoBase import ArmazenamentoBase

class Preprocess:
    PASTA_TEMP = "temp"

    def __init__(self, armazenamento: ArmazenamentoBase):
        os.makedirs(
            self.PASTA_TEMP,
            exist_ok=True
        )

        self.armazenamentos = []
        self.erros = []

        self.ocr = OCR()
        self.armazenamentos.append(armazenamento)

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

        if self.erros:
            print("\n========== ERROS ==========")

            for erro in self.erros:
                print(f"\nArquivo: {erro['arquivo']}")
                print(f"Erro: {erro['erro']}")

            print("\n============================")

        str_print = "Pressione ENTER para finalizar."
        input(str_print)

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

    def processar_arquivo(self, arquivo, caminho_imagem, tag_selecionada, tag_manager=None):
        try:
            imagem_processada = self.preprocessar_imagem(caminho_imagem)

            dados = self.ocr.analisar_imagem(imagem_processada)

            categoria = dados.get(
                "categoria",
                "Outros"
            )

            plano_de_estudos = dados.get("plano_estudos")

            tags = dados.get("tags")

            categoria = categoria.strip()

            if categoria == "Estudo" and tag_selecionada is None:
                tag_selecionada = self.escolha_tag(tags)

            print("\nArmazenamento iniciado.\n")

            if len(self.armazenamentos) > 1:
                self.armazenamentos[0].salvar(categoria, tag_selecionada, arquivo, imagem_processada, caminho_imagem, dados, plano_de_estudos)

                print("\nArmazenando no Google Drive...")
                self.armazenamentos[1].salvar(categoria, tag_selecionada, arquivo, imagem_processada, caminho_imagem, dados, plano_de_estudos)
            else:
                self.armazenamentos[0].salvar(categoria, tag_selecionada, arquivo, imagem_processada, caminho_imagem, dados, plano_de_estudos)

            os.remove(imagem_processada)

            if tag_manager and tag_selecionada:
                tag_manager.adicionar_tag(tag_selecionada)

                if tag_manager.ultima_tag != tag_selecionada:
                    tag_manager.ultima_tag = tag_selecionada

                tag_manager.salvar_tags()

            for _ in range(50):
                time.sleep(0.1)

        except KeyboardInterrupt:
            raise
        except Exception as erro:
            self.erros.append({
                "arquivo": arquivo,
                "erro": str(erro)
            })

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

    def selecionar_armazenamento(self, armazenamentos):
        self.armazenamentos = armazenamentos
