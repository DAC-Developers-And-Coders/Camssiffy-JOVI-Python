from abc import ABC, abstractmethod

class ArmazenamentoBase(ABC):
    @abstractmethod
    def salvar(self, categoria, tag_selecionada, arquivo, imagem_processada, caminho_imagem, dados, plano_de_estudos):
        pass