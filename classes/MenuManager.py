import os
import sys

from classes.Preprocess import Preprocess

class MenuManager:
    PASTA_IMAGENS = "./imagens_iniciais"

    preprocess = None

    @staticmethod
    def limpar_terminal():
        os.system("cls" if os.name == "nt" else "clear")

    def __init__(self):
        self.preprocess = Preprocess()
        self.iniciar_menu_inicial()

    def iniciar_menu_inicial(self):
        try:
            self.menu_inicial()
        except KeyboardInterrupt:
            print("\nSistema encerrado.")
            os._exit(0)

    def menu_inicial(self):
        while True:
            print("\n===SPRINT 2 - Sistema de melhoria, identificação e organização de fotos===")
            print(f"| 1 - Iniciar processamento geral da pasta {self.PASTA_IMAGENS[2:]}")
            print("| 2 - Iniciar processamento de imagem específica")
            print("| 3 - Sair\n")

            opcao = input()

            if not opcao.isnumeric():
                print("Opção inválida. Tente novamente.")
                self.limpar_terminal()
                continue

            match int(opcao):
                case 1:
                    self.limpar_terminal()
                    self.preprocess.iniciar_processamento_geral(self.PASTA_IMAGENS)
                    self.limpar_terminal()
                    continue
                case 2:
                    print(
                        f"Digite o nome do arquivo da imagem no formato 'nome_arquivo.extensao' (a imagem deve estar na pasta {self.PASTA_IMAGENS[2:]}):")
                    nome_arquivo = str(input())
                    self.limpar_terminal()
                    self.preprocess.iniciar_processamento_unico(nome_arquivo, self.PASTA_IMAGENS)
                    self.limpar_terminal()
                    continue
                case 3:
                    self.limpar_terminal()
                    print("Sistema encerrado.")
                    sys.stdout.flush()
                    os._exit(0)
                case _:
                    print("Opção inválida. Tente novamente.")
                    self.limpar_terminal()
                    continue