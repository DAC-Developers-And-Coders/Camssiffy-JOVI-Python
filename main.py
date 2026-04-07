from preprocess import preprocessar
from ocr import extrair_texto

img = preprocessar('imagem.jpeg')
texto = extrair_texto(img)

# salvar em arquivo
with open('resultado.txt', 'w', encoding='utf-8') as f:
    f.write(texto)

print("Arquivo salvo!")