import cv2
import os
import json


pasta_sistema = r"C:\Users\Public\reconhecimento_facial"

arquivo_nomes = os.path.join(
    pasta_sistema,
    "nomes.json"
)

arquivo_modelo = os.path.join(
    pasta_sistema,
    "modelo_lbph.yml"
)

arquivo_detector = os.path.join(
    pasta_sistema,
    "haarcascade_frontalface_default.xml"
)


# Verifica se já existe algum cadastro
if not os.path.exists(arquivo_modelo):
    print("Ainda não existe nenhuma pessoa cadastrada.")
    print("Execute primeiro o cadastrar.py")
    exit()


if not os.path.exists(arquivo_nomes):
    print("Não foi possível encontrar o arquivo de nomes.")
    exit()


# Carrega os nomes das pessoas cadastradas
with open(arquivo_nomes, "r", encoding="utf-8") as arquivo:
    nomes = json.load(arquivo)


# Carrega o detector de rosto
detector_rosto = cv2.CascadeClassifier(
    arquivo_detector
)

if detector_rosto.empty():
    print("Erro ao carregar o detector de rosto.")
    exit()


# Carrega o modelo que foi treinado no cadastrar.py
reconhecedor = cv2.face.LBPHFaceRecognizer_create()

reconhecedor.read(
    arquivo_modelo
)


# Quanto menor esse valor, mais parecido precisa ser o rosto
limite_reconhecimento = 65


camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Não foi possível abrir a câmera.")
    exit()


print()
print("Reconhecimento facial iniciado.")
print("Olhe para a câmera.")
print("Pressione Q para sair.")
print()


# Essas variáveis servem para confirmar o rosto por vários frames
ultimo_identificador = None
quantidade_confirmacoes = 0
confirmacoes_necessarias = 8


while True:

    conseguiu, imagem = camera.read()

    if not conseguiu:
        print("Erro ao capturar imagem da câmera.")
        break


    # Espelha a câmera
    imagem = cv2.flip(
        imagem,
        1
    )


    imagem_cinza = cv2.cvtColor(
        imagem,
        cv2.COLOR_BGR2GRAY
    )


    rostos = detector_rosto.detectMultiScale(
        imagem_cinza,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(120, 120)
    )


    mensagem = "PROCURANDO ROSTO..."


    for x, y, largura, altura in rostos:

        rosto = imagem_cinza[
            y:y + altura,
            x:x + largura
        ]


        rosto = cv2.resize(
            rosto,
            (200, 200)
        )


        rosto = cv2.equalizeHist(
            rosto
        )


        identificador, distancia = reconhecedor.predict(
            rosto
        )


        # Quanto menor a distância, mais parecido está com o cadastro
        if distancia < limite_reconhecimento:

            nome = nomes.get(
                str(identificador),
                "Desconhecido"
            )


            # Confirma se o mesmo rosto continua aparecendo
            if ultimo_identificador == identificador:
                quantidade_confirmacoes += 1

            else:
                ultimo_identificador = identificador
                quantidade_confirmacoes = 1


            if quantidade_confirmacoes < confirmacoes_necessarias:

                texto_rosto = "Verificando..."

                cor = (0, 255, 255)

                mensagem = "VERIFICANDO IDENTIDADE..."


            else:

                texto_rosto = nome

                cor = (0, 255, 0)

                mensagem = f"Ola, {nome}!"


        else:

            texto_rosto = "Desconhecido"

            cor = (0, 0, 255)

            mensagem = "ROSTO NAO CADASTRADO"

            ultimo_identificador = None

            quantidade_confirmacoes = 0


        # Desenha o quadrado em volta do rosto
        cv2.rectangle(
            imagem,
            (x, y),
            (x + largura, y + altura),
            cor,
            3
        )


        cv2.putText(
            imagem,
            texto_rosto,
            (x, y - 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            cor,
            2
        )


        # Mostra o valor para ajudar a ajustar o reconhecimento
        cv2.putText(
            imagem,
            f"Distancia: {distancia:.1f}",
            (x, y + altura + 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            cor,
            2
        )


    # Faixa preta na parte de cima
    cv2.rectangle(
        imagem,
        (0, 0),
        (imagem.shape[1], 80),
        (0, 0, 0),
        -1
    )


    cv2.putText(
        imagem,
        mensagem,
        (25, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (255, 255, 255),
        2
    )


    cv2.imshow(
        "Reconhecimento Facial",
        imagem
    )


    tecla = cv2.waitKey(1) & 0xFF

    if tecla == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()