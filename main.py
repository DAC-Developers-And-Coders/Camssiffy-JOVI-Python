from preprocess import preprocessar
from ocr import extrair_texto

# processar imagem
img = preprocessar('foto-caderno.jpeg', salvar=True)

# extrair texto
texto = extrair_texto(img)

# 🔥 salvar resultado
with open('resultado.txt', 'w', encoding='utf-8') as f:
    f.write(texto)

print("Arquivo salvo com sucesso!")