import os, io, json

from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload

from classes.Autenticacao.GoogleAuth import GoogleAuth
from classes.Armazenamento.ArmazenamentoBase import ArmazenamentoBase

class ArmazenamentoDrive(ArmazenamentoBase):
    NOME_PASTA = "Camssify"

    def __init__(self):
        creds = GoogleAuth.autenticar()
        self.drive = build('drive', 'v3', credentials=creds)

        self.pasta_id = self.obter_ou_criar_pasta(self.NOME_PASTA)

    def obter_ou_criar_pasta(self, nome, pasta_pai_id=None):
        query = (
            f"name = '{nome}' "
            f"and mimeType = 'application/vnd.google-apps.folder' "
            f"and trashed = false"
        )

        if pasta_pai_id:
            query += f" and '{pasta_pai_id}' in parents"

        resultado = self.drive.files().list(q=query, spaces="drive", fields="files(id, name)").execute()

        pastas = resultado.get("files", [])

        if pastas:
            return pastas[0]["id"]

        metadata = {
            "name": nome,
            "mimeType": "application/vnd.google-apps.folder"
        }

        if pasta_pai_id:
            metadata["parents"] = [pasta_pai_id]

        pasta = self.drive.files().create(body=metadata, fields="id").execute()
        return pasta["id"]

    def salvar(self, categoria, tag_selecionada, arquivo, imagem_processada, caminho_imagem, dados, plano_de_estudos):
        nome_pasta = tag_selecionada if tag_selecionada is not None else categoria

        pasta_categoria = self.obter_ou_criar_pasta(nome_pasta, self.pasta_id)
        pasta_melhoradas = self.obter_ou_criar_pasta("Fotos Melhoradas", pasta_categoria)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")

        nome_base = (nome_pasta.lower() + "_" + timestamp)
        extensao = str(os.path.splitext(arquivo)[1])
        nome_arquivo = nome_base + extensao

        metadata_imagem = {
            "name": nome_arquivo,
            "parents": [pasta_melhoradas]
        }

        media = MediaFileUpload(imagem_processada, resumable=True)
        self.drive.files().create(body=metadata_imagem, media_body=media, fields="id, name").execute()

        if categoria != "Estudo":
            pasta_originais = self.obter_ou_criar_pasta("Fotos Originais", pasta_categoria)

            metadata_imagem_original = {
                "name": nome_arquivo,
                "parents": [pasta_originais]
            }

            media_original = MediaFileUpload(caminho_imagem, resumable=True)
            self.drive.files().create(body=metadata_imagem_original, media_body=media_original, fields="id, name").execute()

        if plano_de_estudos:
            pasta_plano_de_estudos = self.obter_ou_criar_pasta ("Planos de Estudos", pasta_categoria)

            metadata_plano_de_estudos = {
                "name": nome_base + ".txt",
                "parents": [pasta_plano_de_estudos]
            }

            conteudo_plano = json.dumps(plano_de_estudos, ensure_ascii=False, indent=4)
            arquivo_memoria = io.BytesIO(conteudo_plano.encode("utf-8"))

            media_plano_de_estudos = MediaIoBaseUpload(arquivo_memoria, mimetype="text/plain", resumable=False)
            self.drive.files().create(body=metadata_plano_de_estudos, media_body=media_plano_de_estudos, fields="id, name").execute()

        print(f"\nCategoria: {categoria}")
        if tag_selecionada: print(f"Tag: {tag_selecionada}")
        if categoria != "Estudo": print(f"Original: {nome_pasta}\\Fotos Originais\\{nome_arquivo}")
        print(f"Melhorada: {nome_pasta}\\Fotos Melhoradas\\{nome_arquivo}")
        if plano_de_estudos: print(f"Plano de estudos: {nome_pasta}\\Planos de Estudos\\{nome_base}.txt")