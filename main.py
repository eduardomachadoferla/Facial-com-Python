import cv2
import os
import shutil
import time


# Pasta onde ficam os arquivos usados pelo detector
pasta_detectores = r"C:\Users\Public\opencv_cascades"

os.makedirs(pasta_detectores, exist_ok=True)


arquivo_rosto = os.path.join(
    pasta_detectores,
    "haarcascade_frontalface_default.xml"
)

arquivo_olhos = os.path.join(
    pasta_detectores,
    "haarcascade_eye.xml"
)


# Copia os arquivos do OpenCV para uma pasta sem acentos
if not os.path.exists(arquivo_rosto):
    origem_rosto = os.path.join(
        cv2.data.haarcascades,
        "haarcascade_frontalface_default.xml"
    )

    shutil.copyfile(origem_rosto, arquivo_rosto)


if not os.path.exists(arquivo_olhos):
    origem_olhos = os.path.join(
        cv2.data.haarcascades,
        "haarcascade_eye.xml"
    )

    shutil.copyfile(origem_olhos, arquivo_olhos)


# Carrega os detectores
detector_rosto = cv2.CascadeClassifier(arquivo_rosto)
detector_olhos = cv2.CascadeClassifier(arquivo_olhos)


if detector_rosto.empty():
    print("Erro ao carregar o detector de rosto.")
    exit()


if detector_olhos.empty():
    print("Erro ao carregar o detector de olhos.")
    exit()


print("Detectores carregados.")
print("Olhe para a câmera.")
print("Pressione Q para sair.")


# Abre a webcam
camera = cv2.VideoCapture(0)


if not camera.isOpened():
    print("Não foi possível abrir a câmera.")
    exit()


inicio_deteccao = None
acesso_liberado = False


while True:

    conseguiu, imagem = camera.read()

    if not conseguiu:
        print("Erro ao capturar a imagem.")
        break


    # Deixa a câmera como espelho
    imagem = cv2.flip(imagem, 1)


    imagem_cinza = cv2.cvtColor(
        imagem,
        cv2.COLOR_BGR2GRAY
    )


    rostos = detector_rosto.detectMultiScale(
        imagem_cinza,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(100, 100)
    )


    encontrou_olhos = False


    for x, y, largura, altura in rostos:

        # Marca o rosto
        cv2.rectangle(
            imagem,
            (x, y),
            (x + largura, y + altura),
            (0, 255, 255),
            2
        )


        area_rosto_cinza = imagem_cinza[
            y:y + altura,
            x:x + largura
        ]

        area_rosto = imagem[
            y:y + altura,
            x:x + largura
        ]


        olhos = detector_olhos.detectMultiScale(
            area_rosto_cinza,
            scaleFactor=1.1,
            minNeighbors=8,
            minSize=(25, 25)
        )


        total_olhos = 0


        for ox, oy, largura_olho, altura_olho in olhos:

            # Os olhos devem estar na parte de cima do rosto
            if oy < altura / 2:

                cv2.rectangle(
                    area_rosto,
                    (ox, oy),
                    (ox + largura_olho, oy + altura_olho),
                    (0, 255, 0),
                    2
                )

                total_olhos += 1


                if total_olhos >= 2:
                    break


        if total_olhos >= 2:

            encontrou_olhos = True

            cv2.putText(
                imagem,
                "OLHOS DETECTADOS",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )


    # Começa a contar o tempo quando encontra os dois olhos
    if encontrou_olhos and not acesso_liberado:

        if inicio_deteccao is None:
            inicio_deteccao = time.time()


        tempo = time.time() - inicio_deteccao


        cv2.putText(
            imagem,
            f"Escaneando... {tempo:.1f}s",
            (30, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )


        # Barra de carregamento
        tamanho_barra = min(
            int((tempo / 2) * 400),
            400
        )


        cv2.rectangle(
            imagem,
            (30, 120),
            (430, 145),
            (255, 255, 255),
            2
        )


        cv2.rectangle(
            imagem,
            (30, 120),
            (30 + tamanho_barra, 145),
            (0, 255, 0),
            -1
        )


        # Libera depois de 2 segundos
        if tempo >= 2:
            acesso_liberado = True


    elif not encontrou_olhos and not acesso_liberado:

        inicio_deteccao = None


    # Tela mostrada quando os olhos forem detectados
    if acesso_liberado:

        imagem[:] = (0, 0, 0)


        cv2.putText(
            imagem,
            "IDENTIDADE CONFIRMADA",
            (70, 140),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )


        cv2.putText(
            imagem,
            "ACESSO LIBERADO",
            (100, 220),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.4,
            (0, 255, 0),
            3
        )


        cv2.putText(
            imagem,
            "Ola, bem-vindo Eduardo!",
            (80, 300),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 255, 255),
            2
        )


        cv2.putText(
            imagem,
            "Pressione Q para sair",
            (130, 370),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            1
        )


    cv2.imshow(
        "Detector de olhos",
        imagem
    )


    tecla = cv2.waitKey(1) & 0xFF


    if tecla == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()