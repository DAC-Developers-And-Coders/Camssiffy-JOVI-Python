from PIL import Image
from google import genai
from dotenv import load_dotenv
from google.genai import types

import re, os, json

class OCR:
    client = None

    def __init__(self):
        # Carrega as variáveis de ambiente
        load_dotenv()

        # Cria o cliente Gemini utilizando a chave da API armazenada no .env
        self.client = genai.Client(
            api_key=os.getenv(
                "GEMINI_API_KEY"
            )
        )

    # Função responsável por limpar retorno feito pela IA
    @staticmethod
    def limpar_json(texto):

        texto = texto.strip()

        texto = re.sub(
            r"```json|```",
            "",
            texto
        ).strip()

        return texto

    # Função responsável por analisar imagens
    def analisar_imagem(self, path):

        imagem = Image.open(path)

        # Define o prompt enviado para o Gemini
        prompt = """
        Analise cuidadosamente essa imagem.
    
        Você deve:
    
        1. Extrair TODO o texto visível
        2. Descrever a imagem
        3. Classificar a imagem
    
        Categorias:
        - Estudo
        - Trabalho
        - Pessoa
        - Pet
        - Outros
    
        IMPORTANTE:
    
        Se for categoria "Estudo",
        gere um plano de estudos resumido.
    
        O plano deve conter:
        - assunto
        - nivel
        - topicos
        - exercicios
        - tempo_estimado
        - dicas
    
        Responda APENAS em JSON.
    
        Estrutura:
    
        {
          "texto": "",
          "descricao": "",
          "categoria": "",
          "plano_estudos": {
            "assunto": "",
            "nivel": "",
            "topicos": [],
            "exercicios": [],
            "tempo_estimado": "",
            "dicas": []
          }
        }
    
        Se não for estudo:
        "plano_estudos": null
        """

        # Envia imagem e prompt ao Gemini e coleta a resposta
        resposta = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                prompt,
                imagem
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        texto_limpo = self.limpar_json(
            resposta.text
        )

        # Converte JSON para um dicinário
        dados = json.loads(
            texto_limpo
        )

        return dados