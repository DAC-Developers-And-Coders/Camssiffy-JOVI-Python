import os, sys, time

from classes.Preprocess import Preprocess
from classes.TagManager import TagManager
from classes.Autenticacao.GoogleAuth import GoogleAuth
from classes.Armazenamento.ArmazenamentoLocal import ArmazenamentoLocal
from classes.Armazenamento.ArmazenamentoDrive import ArmazenamentoDrive

class MenuManager:
    PASTA_IMAGENS = "./imagens_iniciais"

    @staticmethod
    def limpar_terminal():
        os.system("cls" if os.name == "nt" else "clear")

    def __init__(self):
        self.limpar_terminal()

        self.menu_string = ""
        self.default_tag = ""

        self.preprocess = Preprocess(ArmazenamentoLocal())
        self.tag_manager = TagManager()
        self.iniciar_menu_inicial()

    def atualiza_menu_string(self):
        self.menu_string = ("\n=== CAMSSIFY & JOVI - Sistema de melhoria, identificação e organização de fotos ==="
                       f"\n| TAG ATIVA: {self.default_tag}\n|"
                       "\n| [1] - Tutorial inicial de uso"
                       "\n| [2] - Selecionar modo de armazenamento"
                       "\n| [3] - Utilizar última tag"
                       "\n| [4] - Criar nova tag"
                       "\n| [5] - Deletar uma tag"
                       "\n| [6] - Selecionar TAG ATIVA para múltiplas fotos"
                       f"\n| [7] - Iniciar processamento geral da pasta {self.PASTA_IMAGENS[2:]}"
                       "\n| [8] - Iniciar processamento de imagem específica"
                       "\n| [9] - Sair\n")

    def iniciar_tutorial(self):
        self.limpar_terminal()
        print("================ TUTORIAL ================"
              "\n| [1] - Tutorial inicial de uso - - - > PERMITE INICIAR O TUTORIAL"
              "\n| [2] - Selecionar modo de armazenamento - - - > PERMITE SELECIONAR ENTRE SALVAR NA NUVEM, LOCALMENTE OU EM AMBOS"
              "\n| [3] - Utilizar última tag - - - > PERMITE SELECIONAR ÚLTIMA TAG UTILIZADA COMO TAG ATIVA"
              "\n| [4] - Criar nova tag - - - > PERMITE CRIAR UMA NOVA TAG"
              "\n| [5] - Deletar uma tag - - - > PERMITE DELETAR UMA TAG CRIADA ANTERIORMENTE"
              "\n| [6] - Selecionar TAG ATIVA para múltiplas fotos - - - > PERMITE SELECIONAR UMA TAG COMO ATIVA"
              f"\n| [7] - Iniciar processamento geral da pasta {self.PASTA_IMAGENS[2:]} - - -> PERMITE INICIAR O PROCESSAMENTO DE TODAS AS IMAGENS DA PASTA"
              "\n| [8] - Iniciar processamento de imagem específica - - - > PERMITE INICIAR O PROCESSAMENTO DE UMA IMAGEM ESPECÍFICA"
              "\n| [9] - Sair - - - > PERMITE SAIR DO SISTEMA\n")

        self.proximo_passo()

        print("=============== TUTORIAL ================\n"
              "===[2] - Selecionar modo de salvamento===\n")

        print("=============== MÉTODOS DE ARMAZENAMENTO ==============\n"
              "| [1] - Salvar localmente (pasta 'resultados') - - - > OPÇÃO DE SALVAR FOTOS E PLANOS DE ESTUDOS LOCALMENTE\n"
              "| [2] - Salvar na nuvem (Google Drive) - - - > OPÇÃO DE SALVAR FOTOS E PLANOS DE ESTUDOS NO GOOGLE DRIVE\n"
              "| [3] - Salvar em ambos (pasta 'resultados' e Google Drive) - - - > OPÇÃO DE SALVAR LOCALMENTE E NO GOOGLE DRIVE\n"
              "== Digite qualquer coisa para voltar ao menu inicial ==\n"
              "\nDigite o número da opção desejada: 3 - - - > Digite aqui o número da opção de armazenamento desejada.\n"
              "Métodos de armazenamento definidos: LOCAL e NUVEM\n")

        self.proximo_passo()

        print("=============== TUTORIAL ================\n"
              "========[3] - Utilizar última tag========\n"
              "|- - - > O sistema escolhe a última tag utilizada como tag ativa.\n")

        self.proximo_passo()

        print("=============== TUTORIAL ================\n"
              "==========[4] - Criar nova tag===========\n"
              "\nDigite o nome da nova tag: EXEMPLO - - - > Você deve inserir sua tag desejada aqui"
              "\nSe realmente deseja criar a tag EXEMPLO, digite 's': s - - - > Você deve digitar 's' para salvar sua tag, ou outra coisa caso deseje cancelar\n")

        self.proximo_passo()

        print("=============== TUTORIAL ================\n"
              "==========[5] - Deletar uma tag==========\n"
              "\n=== TAGS CRIADAS ==="
              "\n[1] EXEMPLO - - - > Lista de tags criadas anteriormente.\n"
              "\nEscolha a tag que deseja deletar, pelo número: - - - > Aqui, você deve digitar o número da tag que deseja excluir.\n"
              "\nTag EXEMPLO deletada com sucesso.\n")

        self.proximo_passo()

        print("===================== TUTORIAL ======================\n"
              "===[6] - Selecionar TAG ATIVA para múltiplas fotos===\n"
              "\nSelecione a tag que deseja ativar:"
              "\n[0] - REMOVER TAG ATIVA - - - > Caso deseje remover a tag ativa."
              "\n[1] - EXEMPLO - - - > Lista de tags criadas anteriormente."
              "\n1 - - - > Você deve inserir o número da tag desejada aqui.\n"
              "\nTag EXEMPLO selecionada com sucesso.\n")

        self.proximo_passo()

        print("============================ TUTORIAL ===========================\n"
              f"===[7] - Iniciar processamento geral da pasta {self.PASTA_IMAGENS[2:]}===\n"
              "===================== SELEÇÃO DE TAG GERADA =====================\n"
              "\nSistema iniciado\nUse CTRL+C para encerrar\n"
              "\nProcessando: nome_arquivo.extensao\n"
              "\nEscolha uma tag para salvar a imagem (Digite o número de 1 a 4):"
              "\n[1] - EXEMPLO_IA - - - > Lista de tags geradas pela IA."
              "\nCaso deseje inserir uma tag manualmente, digite '0'."
              "\n1 - - - > Você deve inserir o número da tag desejada aqui."
              "\nTag escolhida: EXEMPLO_IA\nSalvamento concluído.\n")

        self.proximo_passo()

        print("============================ TUTORIAL ===========================\n"
              f"===[7] - Iniciar processamento geral da pasta {self.PASTA_IMAGENS[2:]}===\n"
              "===================== SELEÇÃO DE TAG MANUAL =====================\n"
              "\nEscolha uma tag para salvar a imagem (Digite o número de 1 a 4):"
              "\n[1] - EXEMPLO_IA - - - > Lista de tags geradas pela IA."
              "\nCaso deseje inserir uma tag manualmente, digite '0'."
              "\n0 - - - > Você deve inserir o número da tag desejada aqui."
              "\nDigite a tag desejada: MINHA_TAG - - - > Você deve inserir a tag manualmente aqui."
              "\nTag escolhida: MINHA_TAG\nSalvamento concluído.\n")

        self.proximo_passo()

        print("============================ TUTORIAL ===========================\n"
              f"===[7] - Iniciar processamento geral da pasta {self.PASTA_IMAGENS[2:]}===\n"
              "======================== RESULTADO FINAL ========================\n"
              "\nCategoria: Estudo\nTag: EXEMPLO_IA (ou MINHA_TAG)"
              "\nMelhorada: resultados\\EXEMPLO_IA (ou MINHA_TAG)\\melhoradas\\exemplo_ia(ou minha_tag)_a/m/d_h:m:s.jpeg"
              "\nJSON: resultados\\EXEMPLO_IA (ou MINHA_TAG)\\json\\exemplo_ia(ou minha_tag)_a/m/d_h:m:s.json"
              "\nPlano de estudos: resultados\\EXEMPLO_IA (ou MINHA_TAG)\\plano_de_estudos\\exemplo_ia(ou minha_tag)_a/m/d_h:m:s.txt\n")

        self.proximo_passo()

        print("====================== TUTORIAL ======================\n"
              f"===[8] - Iniciar processamento de imagem específica===\n"
              f"\nDigite o nome do arquivo da imagem no formato 'nome_arquivo.extensao' (a imagem deve estar na pasta {self.PASTA_IMAGENS[2:]}):\n"
              "anotacao.jpeg - - - > Você deve digitar o nome do arquivo desejado aqui.\n"
              "O MESMO PROCESSO DO PROCESSAMENTO GERAL\n")

        self.proximo_passo()

        print("================ TUTORIAL ================\n"
              "================[9] - Sair================\n"
              "\nSistema encerrado. - - - > Encerra o sistema.\n")

        self.proximo_passo(True)

    def proximo_passo(self, fim=False):
        str_print = "Pressione ENTER para continuar..." if not fim else "Pressione ENTER para finalizar."
        input(str_print)
        self.limpar_terminal()

    def iniciar_menu_inicial(self):
        #Checa se o sistema foi encerrado pelo comando CTRL+C
        try:
            self.menu_inicial()
        except KeyboardInterrupt:
            print("\nSistema encerrado.")
            self.encerrar_sistema()

    def menu_inicial(self):
        while True:
            self.atualiza_menu_string()
            print(self.menu_string)

            opcao = input()

            if not opcao.isnumeric():
                print("Opção inválida. Tente novamente.")
                self.limpar_terminal()
                continue

            match int(opcao):
                case 1:
                    self.iniciar_tutorial()
                    continue
                case 2:
                    self.selecionar_metodos_salvamento()
                    self.limpar_terminal()
                    continue
                case 3:
                    self.pegar_ultima_tag()
                    self.limpar_terminal()
                    continue
                case 4:
                    self.limpar_terminal()
                    self.criar_tag()
                    continue
                case 5:
                    self.deletar_tag()
                    self.limpar_terminal()
                    continue
                case 6:
                    self.limpar_terminal()
                    self.selecionar_tag_ativa()
                case 7:
                    self.limpar_terminal()
                    self.gerenciar_processamento("", False)
                    self.limpar_terminal()
                    continue
                case 8:
                    print(
                        f"Digite o nome do arquivo da imagem no formato 'nome_arquivo.extensao' (a imagem deve estar na pasta {self.PASTA_IMAGENS[2:]}):")
                    nome_arquivo = str(input())
                    self.limpar_terminal()

                    self.gerenciar_processamento(nome_arquivo)
                    self.limpar_terminal()
                    continue
                case 9:
                    self.limpar_terminal()
                    print("Sistema encerrado.")
                    sys.stdout.flush()
                    self.encerrar_sistema()
                case _:
                    print("Opção inválida. Tente novamente.")
                    self.limpar_terminal()
                    continue

    def selecionar_metodos_salvamento(self):
        self.limpar_terminal()

        print("=============== MÉTODOS DE ARMAZENAMENTO ==============\n"
              "| [1] - Salvar localmente (pasta 'resultados')\n"
              "| [2] - Salvar na nuvem (Google Drive)\n"
              "| [3] - Salvar em ambos (pasta 'resultados' e Google Drive)\n"
              "== Digite qualquer coisa para voltar ao menu inicial ==\n")

        opcao = int(input("Digite o número da opção desejada: "))

        match opcao:
            case 1:
                local = ArmazenamentoLocal()
                self.preprocess.selecionar_armazenamento([local])
                print("Método de armazenamento definido: LOCAL\n")
            case 2:
                drive = ArmazenamentoDrive()
                self.preprocess.selecionar_armazenamento([drive])
                print("Método de armazenamento definido: NUVEM\n")
            case 3:
                local = ArmazenamentoLocal()
                drive = ArmazenamentoDrive()
                self.preprocess.selecionar_armazenamento([local, drive])
                print("Métodos de armazenamento definidos: LOCAL e NUVEM\n")
            case _:
                print("O método de armazenamento não foi alterado.\n")

        input("Pressione ENTER para continuar...")

    def deletar_tag(self):
        self.limpar_terminal()

        if len(self.tag_manager.tags) < 1:
            print("Nenhuma tag criada.")
            self.delay_limpar_terminal(1.5)
            return

        print("=== TAGS CRIADAS ===")
        for i, tag in enumerate(self.tag_manager.tags):
            print(f"[{i + 1}] - {tag}")

        try:
            selecao = int(input("\nEscolha a tag que deseja deletar, pelo número: "))

            if 1 <= selecao <= len(self.tag_manager.tags):
                tag = self.tag_manager.tags[selecao - 1]
                self.tag_manager.tags.pop(selecao - 1)

                if self.default_tag == tag:
                    self.default_tag = ""

                if self.tag_manager.ultima_tag == tag:
                    self.tag_manager.ultima_tag = ""

                self.tag_manager.salvar_tags()
                print(f"\nTag {tag} deletada com sucesso.")
            else:
                print("\nTag inválida. Nenhuma tag deletada.")
        except ValueError:
            print("\nTag inválida. Nenhuma tag deletada.")

        self.delay_limpar_terminal(1.5)

    def pegar_ultima_tag(self):
        tag_agora = self.default_tag
        ultima_tag = self.tag_manager.get_ultima_tag()

        if ultima_tag:
            self.default_tag = ultima_tag
            self.tag_manager.ultima_tag = tag_agora

            self.tag_manager.salvar_tags()
        else:
            print("Nenhuma tag utilizada anteriormente.")
            self.delay_limpar_terminal(1.5)

    def gerenciar_processamento(self, nome_arquivo, unico=True):
        try:
            if self.default_tag == "":
                self.processamento_basico(unico, nome_arquivo)
            else:
                self.processamento_tag_ativa(unico, nome_arquivo)
        except KeyboardInterrupt:
            print("\nProcessamento interrompido.")

    def processamento_basico(self, unico, nome_arquivo):
        if unico:
            self.preprocess.iniciar_processamento_unico(nome_arquivo, self.PASTA_IMAGENS, None, self.tag_manager)
            self.limpar_terminal()
        else:
            self.preprocess.iniciar_processamento_geral(self.PASTA_IMAGENS, None, self.tag_manager)

    def processamento_tag_ativa(self, unico, nome_arquivo):
        if unico:
            self.preprocess.iniciar_processamento_unico(nome_arquivo, self.PASTA_IMAGENS, self.default_tag, self.tag_manager)
            self.limpar_terminal()
        else:
            self.preprocess.iniciar_processamento_geral(self.PASTA_IMAGENS, self.default_tag, self.tag_manager)

    def criar_tag(self):
        tag = str(input("Digite o nome da nova tag: "))
        escolha = str(input(f"\nSe realmente deseja criar a tag {tag}, digite 's': ")).lower()

        if escolha != "s":
            print("\nNehuma tag criada.")
        else:
            if tag in self.tag_manager.tags:
                print("\nTag já existe.")
            else:
                self.tag_manager.tags.append(tag)
                self.tag_manager.salvar_tags()
                print(f"\nTag {tag} criada com sucesso.")

        self.delay_limpar_terminal(1.5)

    def selecionar_tag_ativa(self):
        if len(self.tag_manager.tags) < 1:
            print("Nenhuma tag criada.")
            return

        print("Selecione a tag que deseja ativar:")

        print("[0] - REMOVER TAG ATIVA")
        for i, tag in enumerate(self.tag_manager.tags):
            print(f"[{i + 1}] - {tag}")

        try:
            escolha = int(input())

            if 1 <= escolha <= len(self.tag_manager.tags):
                tag_agora = self.default_tag
                self.default_tag = self.tag_manager.tags[escolha - 1]

                if tag_agora:
                    self.tag_manager.ultima_tag = tag_agora
                else:
                    self.tag_manager.ultima_tag = self.default_tag

                self.tag_manager.salvar_tags()
                print(f"\nTag {self.default_tag} selecionada com sucesso.")
            elif escolha == 0:
                self.default_tag = ""
                print("\nTag removida com sucesso.")
            else:
                print("\nOpção inválida, nenhuma tag selecionada.")
        except ValueError:
            print("\nOpção inválida, nenhuma tag selecionada.")

        self.delay_limpar_terminal(1.5)

    def delay_limpar_terminal(self, segundos):
        for _ in range(int(segundos * 10)):
            time.sleep(0.1)

        self.limpar_terminal()

    def encerrar_sistema(self):
        if self.default_tag:
            self.tag_manager.ultima_tag = self.default_tag

        self.tag_manager.salvar_tags()
        os._exit(0)