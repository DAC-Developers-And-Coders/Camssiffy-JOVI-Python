import os, json

class TagManager:
    ARQUIVO_TAGS = "data/tags.json"

    def __init__(self):
        self.tags = []
        self.ultima_tag = None

        os.makedirs("data", exist_ok=True)

        if os.path.isfile(self.ARQUIVO_TAGS):
            self.carregar_tags()

    def salvar_tags(self):
        data = {
            "tags": self.tags,
            "ultima_tag": self.ultima_tag
        }

        with open(self.ARQUIVO_TAGS, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def carregar_tags(self):
        with open(self.ARQUIVO_TAGS, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.tags = data["tags"]
        self.ultima_tag = data["ultima_tag"]

    def get_ultima_tag(self):
        return self.ultima_tag

    def adicionar_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)