import os, cv2, sys, subprocess

IMAGENS_INICIAIS_PATH = "./imagens_iniciais"
NOME_ARQUIVO_DEFAULT = "foto"

class Camera:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.ultima_foto = None

    def set_camera(self, index):
        if self.camera.isOpened():
            self.camera.release()

        self.camera = cv2.VideoCapture(index)

    def abrir_camera(self):
        if not self.camera.isOpened():
            print("Erro ao abrir a camera")
            return

        print("\nCâmera aberta com sucesso!\n\nPressione 's' para sair.\nPressione 'f' para tirar uma foto.\nPressione 'c' para cortar a última foto tirada.")

        if self.ultima_foto is not None:
            self.ultima_foto = None

        while True:
            ret, frame = self.camera.read()

            if not ret:
                print("Erro ao capturar a imagem")
                break

            cv2.imshow('Camera', frame)

            key = cv2.waitKey(1) & 0xff

            if key == ord('f'):
                cv2.imshow('Foto', frame)

                if os.path.isfile(os.path.join(IMAGENS_INICIAIS_PATH, f'{NOME_ARQUIVO_DEFAULT}.png')):
                    contador_arquivos = len([f for f in os.listdir(IMAGENS_INICIAIS_PATH) if f.endswith('.png') and
                                      os.path.isfile(os.path.join(IMAGENS_INICIAIS_PATH, f))])

                    arquivo_camera = os.path.join(IMAGENS_INICIAIS_PATH, f'{NOME_ARQUIVO_DEFAULT}({contador_arquivos}).png')
                else:
                    arquivo_camera = os.path.join(IMAGENS_INICIAIS_PATH, NOME_ARQUIVO_DEFAULT)

                cv2.imwrite(arquivo_camera, frame)
                print(f"Imagem capturada com sucesso e armazenada em {IMAGENS_INICIAIS_PATH}")

                self.ultima_foto = arquivo_camera
            elif key == ord('c'):
                self.abrir_editor_de_fotos()
            elif key == ord('s'):
                break

        cv2.destroyAllWindows()

    def abrir_editor_de_fotos(self):
        if self.ultima_foto is None:
            print("\nNenhuma foto foi capturada nesta sessão.\n")
            return

        if sys.platform == 'win32':
            subprocess.run(['start', self.ultima_foto], shell=True)
        elif sys.platform == 'darwin':
            subprocess.run(['open', self.ultima_foto])
        else:
            subprocess.run(['xdg-open', self.ultima_foto])

    def fechar_camera(self):
        self.camera.release()

    def verficar_camera(self):
        return self.camera.isOpened()