from google.cloud import vision
import io
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\Davi\Documents\faculdade\chave-cv-api.json'

def analisar_imagem(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.annotate_image({
        'image': image,
        'features': [
            {'type': vision.Feature.Type.TEXT_DETECTION},
            {'type': vision.Feature.Type.LABEL_DETECTION},
            {'type': vision.Feature.Type.OBJECT_LOCALIZATION}
        ]
    })
    texto = ""
    if response.text_annotations:
        texto = response.text_annotations[0].description

    #labels
    labels = [label.description for label in response.label_annotations]

    #objetos
    objetos = [obj.name for obj in response.localized_object_annotations]

    return texto, labels, objetos