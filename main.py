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

PASTA_IMAGENS = "./imagens_iniciais"
PASTA_RESULTADOS = "./resultados"

# Função que limpa o terminal
def limpar_terminal():
    os.system("cls" if os.name == "nt" else "clear")

# Função que encerra execução do programa ao usuário selecionar tecla 'e'
def encerrar():
    keyboard.wait("e")

    print("Sistema encerrado.")
    sys.stdout.flush()
    os._exit(0)

# Função que inicia thread executada paralelamente ao sistema, aguardando a seleção da tecla 'e'
def iniciar_thread():
    print("Sistema iniciado\nPressione 'E' para encerrar.")
    threading.Thread(target=encerrar, daemon=True).start()

# Função que gerencia o processamento de imagens
def processar_arquivo(arquivo, caminho_imagem):
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

        plano_de_estudos = dados.get(
            "plano_estudos"
        )

        categoria = categoria.strip()

        # Criação/Seleção de pastas
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

        pasta_plano_de_estudos = os.path.join(
            pasta_categoria,
            "planos_de_estudos"
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

        os.makedirs(
            pasta_plano_de_estudos,
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

        plano_de_estudos_destino = os.path.join(
            pasta_plano_de_estudos,
            nome_base + ".txt"
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

        print(
            f"Plano de estudos: {plano_de_estudos_destino[2:]}"
        )

        os.remove(imagem_processada)

        for _ in range(50):
            time.sleep(0.1)

    except Exception as erro:
        print(f"Erro: {erro}")


# Função que inicia o processamento de todas as imagens do diretório
def iniciar_processamento_geral():
    iniciar_thread()

    for arquivo in os.listdir(PASTA_IMAGENS):
        caminho_imagem = os.path.join(
            PASTA_IMAGENS,
            arquivo
        )

        if not os.path.isfile(caminho_imagem):
            continue

        print(f"\nProcessando: {arquivo}")
        processar_arquivo(arquivo, caminho_imagem)

    print("\nProcessamento finalizado")

# Função que inicia o processamento de uma imagem específica do diretório
def iniciar_processamento_unico(nome_arquivo):
    iniciar_thread()

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
    processar_arquivo(nome_arquivo, caminho_imagem)

    print("\nProcessamento finalizado")

# Função que inicia o menu inicial do sistema
def menu_inicial():
    while True:
        print("\n===SPRINT 2 - Sistema de melhoria, identificação e organização de fotos===")
        print(f"| 1 - Iniciar processamento geral da pasta {PASTA_IMAGENS[2:]}")
        print("| 2 - Iniciar processamento de imagem específica")
        print("| 3 - Sair\n")

        opcao = input()

        if not opcao.isnumeric():
            print("Opção inválida. Tente novamente.")
            limpar_terminal()
            continue

        match int(opcao):
            case 1:
                limpar_terminal()
                iniciar_processamento_geral()
                limpar_terminal()
                continue
            case 2:
                print(f"Digite o nome do arquivo da imagem no formato 'nome_arquivo.extensao' (a imagem deve estar na pasta {PASTA_IMAGENS[2:]}):")
                nome_arquivo = str(input())
                limpar_terminal()
                iniciar_processamento_unico(nome_arquivo)
                limpar_terminal()
                continue
            case 3:
                limpar_terminal()
                print("Sistema encerrado.")
                sys.stdout.flush()
                os._exit(0)
            case _:
                print("Opção inválida. Tente novamente.")
                limpar_terminal()
                continue

menu_inicial()