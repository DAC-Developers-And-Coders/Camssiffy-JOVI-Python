import os, json, shutil
from datetime import datetime

from classes.Armazenamento.ArmazenamentoBase import ArmazenamentoBase

class ArmazenamentoLocal(ArmazenamentoBase):
    PASTA_RESULTADOS = "./resultados"

    def salvar(self, categoria, tag_selecionada, arquivo, imagem_processada, caminho_imagem, dados, plano_de_estudos):
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

        # Salva imagem original, se não for de estudos
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
        if tag_selecionada: print(f"Tag: {tag_selecionada}")
        if imagem_original_destino: print(f"Original: {imagem_original_destino[2:]}")
        print(f"Melhorada: {imagem_melhorada_destino[2:]}")
        print(f"JSON: {json_destino[2:]}")

        if plano_de_estudos_destino is not None:
            print(f"Plano de estudos: {plano_de_estudos_destino[2:]}")