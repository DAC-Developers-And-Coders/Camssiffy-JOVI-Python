from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image

import json
import re
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv(
        "GEMINI_API_KEY"
    )
)


def limpar_json(texto):

    texto = texto.strip()

    texto = re.sub(
        r"```json|```",
        "",
        texto
    ).strip()

    return texto


def analisar_imagem(path):

    imagem = Image.open(path)

    prompt = """
    Analise cuidadosamente essa imagem.

    Você deve:

    1. Extrair TODO o texto visível
    2. Descrever a imagem
    3. Classificar a imagem

    Categorias:
    - Estudo
    - Trabalho
    - Pessoal
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

    resposta = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            prompt,
            imagem
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

    texto_limpo = limpar_json(
        resposta.text
    )

    dados = json.loads(
        texto_limpo
    )

    return dados