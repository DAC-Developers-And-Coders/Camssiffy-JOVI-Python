from classes.Armazenamento.ArmazenamentoBase import ArmazenamentoBase

class ArmazenamentoDrive(ArmazenamentoBase):
    def salvar(self, categoria, tag_selecionada, arquivo, imagem_processada, caminho_imagem, dados, plano_de_estudos):
        print("salvo")