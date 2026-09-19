from abc import ABC, abstractmethod

class ArmazenamentoBase(ABC):
    @abstractmethod
    def salvar(self, categoria, tag_selecionada, arquivo, imagem_processada, caminho_imagem, dados, plano_de_estudos):
        pass

    @staticmethod
    def processar_plano(plano_estudos):
        topicos_estudo = ""
        exercicios = ""
        dicas = ""

        for topico in plano_estudos["topicos"]:
            topicos_estudo += f"- {topico}\n"

        for exercicio in plano_estudos["exercicios"]:
            exercicios += f"- {exercicio}\n"

        for dica in plano_estudos["dicas"]:
            dicas += f"- {dica}\n"

        return (
            f'Assunto: {plano_estudos["assunto"]}\nNível de dificuldade: {plano_estudos["nivel"]}\n'
            f'Tempo Estimado: {plano_estudos["tempo_estimado"]}\n\n'
            f'Tópicos de estudo:\n{topicos_estudo}\n'
            f'Exercícios recomendados:\n{exercicios}\n'
            f'Dicas:\n{dicas}')