from preprocess import preprocessar
from ocr import extrair_texto

img = preprocessar('foto-caderno.jpeg', salvar=True)

texto = extrair_texto(img)

with open('resultado.txt', 'w', encoding='utf-8') as f:
    f.write(texto)

print("Arquivo salvo com sucesso!")