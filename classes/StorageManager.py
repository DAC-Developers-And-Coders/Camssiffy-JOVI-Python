import os, json

class StorageManager:
    ARQUIVO_ARMAZENAMENTO = "data/storage_data.json"
    METODOS_ARMAZENAMENTO = ["LOCAL", "NUVEM", "LOCAL E NUVEM"]

    def __init__(self):
        self.armazenamentos = []
        self.armazenamento_selecionado = self.METODOS_ARMAZENAMENTO[0]

        if os.path.isfile(self.ARQUIVO_ARMAZENAMENTO):
            self.carregar_metodo_armazenamento()

    def salvar_dados(self):
        data = {
            "armazenamentos": self.METODOS_ARMAZENAMENTO,
            "armazenamento_selecionado": self.armazenamento_selecionado
        }

        with open(self.ARQUIVO_ARMAZENAMENTO, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def carregar_metodo_armazenamento(self):
        with open(self.ARQUIVO_ARMAZENAMENTO, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.armazenamentos = data["armazenamentos"]
        self.armazenamento_selecionado = data["armazenamento_selecionado"] if data["armazenamento_selecionado"] is not None else self.METODOS_ARMAZENAMENTO[0]

    def get_armazenamento_selecionado(self):
        return self.armazenamento_selecionado

    def set_armazenamento_selecionado(self, metodo_armazenamento):
        self.armazenamento_selecionado = self.METODOS_ARMAZENAMENTO[metodo_armazenamento]