from preprocess import preprocessar
from ocr import analisar_imagem
import cv2
import os
import shutil

pasta_entrada = 'imagens_teste'
pasta_saida = 'resultados'

os.makedirs(pasta_saida, exist_ok=True)

print('iniciou')


def classificar_avancado(labels, objetos, texto):
    labels = [l.lower() for l in labels]
    objetos = [o.lower() for o in objetos]
    texto = texto.lower()

    score = {
        'Estudo': 0,
        'Pessoal': 0,
        'Pet': 0,
        'Trabalho': 0,
        'Outros': 0
    }

    # ESTUDO
    for k in ['text','handwriting','notebook','document','paper','book','page','notes','study','school']:
        if k in labels: score['Estudo'] += 2
        if k in objetos: score['Estudo'] += 1

    if any(p in texto for p in ['matemática','história','geografia','física','química','exercício','prova']):
        score['Estudo'] += 4

    # PESSOAL
    for k in ['person','face','selfie','portrait','people']:
        if k in labels: score['Pessoal'] += 2
        if k in objetos: score['Pessoal'] += 1

    # PET
    for k in ['dog','cat','animal','pet']:
        if k in labels: score['Pet'] += 2
        if k in objetos: score['Pet'] += 1

    # TRABALHO
    for k in ['laptop','computer','keyboard','office','desk','monitor']:
        if k in labels: score['Trabalho'] += 2
        if k in objetos: score['Trabalho'] += 1

    if any(p in texto for p in ['relatório','empresa','projeto','cliente']):
        score['Trabalho'] += 4

    categoria = max(score, key=score.get)
    return categoria, score


# pega lista fixa (evita bug)
arquivos = os.listdir(pasta_entrada)

for arquivo in arquivos:

    if not arquivo.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue

    caminho_imagem = os.path.join(pasta_entrada, arquivo)

    print(f"\nProcessando: {arquivo}")

    # preprocess
    img = preprocessar(caminho_imagem)

    if img is None:
        print(f"Erro no preprocess: {arquivo}")
        continue

    # salvar temp
    caminho_temp = os.path.join(pasta_saida, f'temp_{arquivo}')
    cv2.imwrite(caminho_temp, img)

    try:
        texto, labels, objetos = analisar_imagem(caminho_temp)
    except Exception as e:
        print(f"Erro OCR: {e}")
        continue

    categoria, score = classificar_avancado(labels, objetos, texto)

    # pasta categoria
    pasta_categoria = os.path.join(pasta_saida, categoria)
    os.makedirs(pasta_categoria, exist_ok=True)

    #COPIAR imagem original (não mover!)
    destino_original = os.path.join(pasta_categoria, arquivo)
    shutil.copy2(caminho_imagem, destino_original)

    # salvar imagem processada
    caminho_proc = os.path.join(pasta_categoria, f'proc_{arquivo}')
    cv2.imwrite(caminho_proc, img)

    # salvar txt
    nome_base = os.path.splitext(arquivo)[0]
    caminho_txt = os.path.join(pasta_categoria, f'{nome_base}.txt')

    with open(caminho_txt, 'w', encoding='utf-8') as f:
        f.write("=== TEXTO ===\n")
        f.write(texto + "\n\n")

        f.write("=== LABELS ===\n")
        f.write('\n'.join(labels) + "\n\n")

        f.write("=== OBJETOS ===\n")
        f.write('\n'.join(objetos) + "\n\n")

        f.write("=== SCORE ===\n")
        f.write(str(score))

    # apagar apenas TEMP
    if os.path.exists(caminho_temp):
        os.remove(caminho_temp)

    print(f"✔ Categoria: {categoria}")
    print(f"✔ Salvo em: {pasta_categoria}")