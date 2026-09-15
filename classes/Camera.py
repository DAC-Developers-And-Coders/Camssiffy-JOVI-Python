import os
import cv2

IMAGENS_INICIAIS_PATH = "./imagens_iniciais"
NOME_ARQUIVO_DEFAULT = "foto.png"

class Camera:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)

    def abrir_camera(self):
        if not self.camera.isOpened():
            print("Erro ao abrir a camera")
            return

        print("Câmera aberta com sucesso!\n\nPressione 'q' para sair.\nPressione 'c' para capturar uma imagem.")

        while True:
            ret, frame = self.camera.read()

            if not ret:
                print("Erro ao capturar a imagem")
                break

            cv2.imshow('Camera', frame)

            if cv2.waitKey(1) == ord('c'):
                cv2.imshow('Foto', frame)

                if os.path.isfile(os.path.join(IMAGENS_INICIAIS_PATH, NOME_ARQUIVO_DEFAULT)):
                    file_count = len([f for f in os.listdir(IMAGENS_INICIAIS_PATH) if f.endswith('.png') and
                                      os.path.isfile(os.path.join(IMAGENS_INICIAIS_PATH, f))])

                    cv2.imwrite(os.path.join(IMAGENS_INICIAIS_PATH, f'{NOME_ARQUIVO_DEFAULT}({file_count}).png'), frame)
                else:
                    cv2.imwrite(os.path.join(IMAGENS_INICIAIS_PATH, NOME_ARQUIVO_DEFAULT), frame)
                print(f"Imagem capturada com sucesso e armazenada em {IMAGENS_INICIAIS_PATH}")

            if cv2.waitKey(1) == ord('q'):
                break

        cv2.destroyAllWindows()

    def fechar_camera(self):
        self.camera.release()

    def verficar_camera(self):
        return self.camera.isOpened()