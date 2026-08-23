import os
import sys

from classes.Preprocess import Preprocess

class MenuManager:
    PASTA_IMAGENS = "./imagens_iniciais"

    menu_string = ("\n===CAMSSIFY & JOVI - Sistema de melhoria, identificação e organização de fotos==="
                   "\n| DEFAULT TAG: \n|"
                   "\n| [1] - Tutorial inicial de uso"
                   "\n| [2] - Selecionar modo de salvamento"
                   "\n| [3] - Utilizar última tag"
                   "\n| [4] - Criar nova tag"
                   "\n| [5] - Selecionar DEFAULT TAG para múltiplas fotos"
                   f"\n| [6] - Iniciar processamento geral da pasta {PASTA_IMAGENS[2:]}"
                   "\n| [7] - Iniciar processamento de imagem específica"
                   "\n| [8] - Sair\n")
    preprocess = None

    @staticmethod
    def limpar_terminal():
        os.system("cls" if os.name == "nt" else "clear")

    def __init__(self):
        self.limpar_terminal()

        self.preprocess = Preprocess()
        self.iniciar_menu_inicial()

    def iniciar_menu_inicial(self):
        #Checa se o sistema foi encerrado pelo comando CTRL+C
        try:
            self.menu_inicial()
        except KeyboardInterrupt:
            print("\nSistema encerrado.")
            os._exit(0)

    def menu_inicial(self):
        while True:
            print(self.menu_string)

            opcao = input()

            if not opcao.isnumeric():
                print("Opção inválida. Tente novamente.")
                self.limpar_terminal()
                continue

            match int(opcao):
                case 6:
                    self.limpar_terminal()
                    self.gerenciar_processamento("", False)
                    self.limpar_terminal()
                    continue
                case 7:
                    print(
                        f"Digite o nome do arquivo da imagem no formato 'nome_arquivo.extensao' (a imagem deve estar na pasta {self.PASTA_IMAGENS[2:]}):")
                    nome_arquivo = str(input())
                    self.limpar_terminal()

                    self.gerenciar_processamento(nome_arquivo)
                    self.limpar_terminal()
                    continue
                case 8:
                    self.limpar_terminal()
                    print("Sistema encerrado.")
                    sys.stdout.flush()
                    os._exit(0)
                case _:
                    print("Opção inválida. Tente novamente.")
                    self.limpar_terminal()
                    continue

    def gerenciar_processamento(self, nome_arquivo, unico=True):
        try:
            if unico:
                self.preprocess.iniciar_processamento_unico(nome_arquivo, self.PASTA_IMAGENS)
                self.limpar_terminal()
            else:
                self.preprocess.iniciar_processamento_geral(self.PASTA_IMAGENS)
        except KeyboardInterrupt:
            print("\nProcessamento interrompido.")