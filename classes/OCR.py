from PIL import Image
from google import genai
from dotenv import load_dotenv
from google.genai import types

import re, os, json

class OCR:
    client = None

    def __init__(self):
        load_dotenv()

        self.client = genai.Client(
            api_key=os.getenv(
                "GEMINI_API_KEY"
            )
        )

    @staticmethod
    def limpar_json(texto):

        texto = texto.strip()

        texto = re.sub(
            r"```json|```",
            "",
            texto
        ).strip()

        return texto

    def analisar_imagem(self, path):

        imagem = Image.open(path)

        prompt = """
        Analise cuidadosamente a imagem fornecida.
    
        Sua tarefa é:
    
        1. EXTRAÇÃO DE TEXTO
        - Extraia todo o texto que estiver visível e legível na imagem.
        - Preserve o conteúdo e a ordem do texto da forma mais fiel possível.
        - Não invente ou complete palavras que não estejam legíveis.
        
        2. DESCRIÇÃO DA IMAGEM
        - Descreva objetivamente o conteúdo visual da imagem.
        - Não faça suposições desnecessárias sobre elementos que não podem ser identificados.
        
        3. CLASSIFICAÇÃO
        Classifique a imagem em EXATAMENTE UMA das seguintes categorias:
    
        - "Estudo"
        - "Pessoa"
        - "Pet"
        - "Outros"
        
        4. TAGS
        - Se a categoria for "Estudo", gere APENAS 4 tags relevantes para a imagem.
        - As tags devem representar a matéria, assunto ou conteúdo identificado.
        - Se não for "Estudo", "tags" deve ser null.
        - As tags devem ser curtas e relevantes.
    
        5. PLANO DE ESTUDOS
        - Identifique o assunto principal com base no conteúdo da imagem.
        - Gere um plano de estudos resumido e prático.
        - O nível deve ser exatamente um dos seguintes:
          - "iniciante"
          - "intermediario"
          - "avancado"
        - Os tópicos devem ser uma lista de assuntos que devem ser estudados.
        - Os exercícios devem ser uma lista de atividades práticas para fixação.
        - O tempo_estimado deve ser uma estimativa clara, como "1 hora", "2 horas" ou "3 horas".
        - As dicas devem ser curtas e úteis.
        - Não invente conteúdos que não tenham relação com o assunto identificado.
    
        O plano deve conter:
        - assunto
        - nivel
        - topicos
        - exercicios
        - tempo_estimado
        - dicas
    
        RETORNE APENAS JSON VÁLIDO.
        Não utilize Markdown, não utilize blocos de código e não adicione explicações fora do JSON.
    
        Use EXATAMENTE esta estrutura::
    
        {
          "texto": "",
          "descricao": "",
          "categoria": "",
          "tags": [],
          "plano_estudos": {
            "assunto": "",
            "nivel": "",
            "topicos": [],
            "exercicios": [],
            "tempo_estimado": "",
            "dicas": []
          }
        }
    
        Quando a categoria não for "Estudo", use:

        {
          "texto": "",
          "descricao": "",
          "categoria": "",
          "tags": null,
          "plano_estudos": null
        }
        """

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
            resposta.text or ""
        )

        dados = json.loads(
            texto_limpo
        )

        return dados