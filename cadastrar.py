import cv2
import os
import json
import shutil
import numpy as np


# Pastas usadas pelo programa
pasta_sistema = r"C:\Users\Public\reconhecimento_facial"
pasta_rostos = os.path.join(pasta_sistema, "rostos")

arquivo_nomes = os.path.join(pasta_sistema, "nomes.json")
arquivo_modelo = os.path.join(pasta_sistema, "modelo_lbph.yml")
arquivo_detector = os.path.join(
    pasta_sistema,
    "haarcascade_frontalface_default.xml"
)

os.makedirs(pasta_rostos, exist_ok=True)


# Copia o detector de rosto caso ainda não exista
if not os.path.exists(arquivo_detector):
    origem = os.path.join(
        cv2.data.haarcascades,
        "haarcascade_frontalface_default.xml"
    )

    shutil.copyfile(origem, arquivo_detector)


detector_rosto = cv2.CascadeClassifier(arquivo_detector)

if detector_rosto.empty():
    print("Não foi possível carregar o detector de rosto.")
    exit()


# Lê as pessoas que já foram cadastradas
if os.path.exists(arquivo_nomes):
    with open(arquivo_nomes, "r", encoding="utf-8") as arquivo:
        nomes = json.load(arquivo)
else:
    nomes = {}


nome = input("Digite o nome da pessoa que será cadastrada: ").strip()

if nome == "":
    print("Nome inválido.")
    exit()


# Procura se a pessoa já existe
id_pessoa = None

for identificador, nome_cadastrado in nomes.items():
    if nome_cadastrado.lower() == nome.lower():
        id_pessoa = int(identificador)
        break


# Se for uma pessoa nova, cria um novo número para ela
if id_pessoa is None:

    if len(nomes) == 0:
        id_pessoa = 1
    else:
        id_pessoa = max(int(numero) for numero in nomes.keys()) + 1

    nomes[str(id_pessoa)] = nome


# Salva a lista de pessoas
with open(arquivo_nomes, "w", encoding="utf-8") as arquivo:
    json.dump(
        nomes,
        arquivo,
        ensure_ascii=False,
        indent=4
    )


# Cria uma pasta para guardar as fotos da pessoa
pasta_pessoa = os.path.join(
    pasta_rostos,
    str(id_pessoa)
)

os.makedirs(pasta_pessoa, exist_ok=True)


print()
print("-----------------------------")
print("CADASTRO FACIAL")
print("-----------------------------")
print(f"Pessoa: {nome}")
print()
print("Olhe para a câmera.")
print("Movimente um pouco o rosto.")
print("Olhe para a esquerda e para a direita.")
print("Aproxime e afaste um pouco.")
print()
print("Aperte Q para cancelar.")
print()


# Abre a webcam
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Não foi possível abrir a câmera.")
    exit()


fotos_tiradas = 0
total_fotos = 40
contador = 0


while fotos_tiradas < total_fotos:

    conseguiu, imagem_camera = camera.read()

    if not conseguiu:
        print("Erro ao pegar imagem da câmera.")
        break


    # Espelha a imagem
    imagem_camera = cv2.flip(imagem_camera, 1)


    # O detector funciona melhor em escala de cinza
    imagem_cinza = cv2.cvtColor(
        imagem_camera,
        cv2.COLOR_BGR2GRAY
    )


    rostos = detector_rosto.detectMultiScale(
        imagem_cinza,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(120, 120)
    )


    if len(rostos) > 0:

        # Caso apareça mais de um rosto, usa o maior
        rosto_encontrado = max(
            rostos,
            key=lambda rosto: rosto[2] * rosto[3]
        )

        x, y, largura, altura = rosto_encontrado


        # Desenha o quadrado em volta do rosto
        cv2.rectangle(
            imagem_camera,
            (x, y),
            (x + largura, y + altura),
            (0, 255, 0),
            2
        )


        contador += 1


        # Não salva todos os frames para as fotos ficarem mais variadas
        if contador >= 5:

            contador = 0

            rosto = imagem_cinza[
                y:y + altura,
                x:x + largura
            ]

            rosto = cv2.resize(rosto, (200, 200))

            rosto = cv2.equalizeHist(rosto)

            fotos_tiradas += 1


            caminho_foto = os.path.join(
                pasta_pessoa,
                f"{fotos_tiradas}.jpg"
            )

            cv2.imwrite(
                caminho_foto,
                rosto
            )


    # Faz a barra mostrando o andamento do cadastro
    tamanho_barra = int(
        (fotos_tiradas / total_fotos) * 400
    )


    cv2.rectangle(
        imagem_camera,
        (30, 40),
        (430, 70),
        (255, 255, 255),
        2
    )

    cv2.rectangle(
        imagem_camera,
        (30, 40),
        (30 + tamanho_barra, 70),
        (0, 255, 0),
        -1
    )


    cv2.putText(
        imagem_camera,
        f"Cadastrando {nome}: {fotos_tiradas}/{total_fotos}",
        (30, 110),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )


    cv2.putText(
        imagem_camera,
        "Movimente lentamente o rosto",
        (30, 145),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )


    cv2.imshow(
        "Cadastro Facial",
        imagem_camera
    )


    tecla = cv2.waitKey(1) & 0xFF

    if tecla == ord("q"):
        camera.release()
        cv2.destroyAllWindows()

        print("Cadastro cancelado.")
        exit()


camera.release()
cv2.destroyAllWindows()


# Agora pega todas as fotos cadastradas para treinar o reconhecimento
print()
print("Treinando reconhecimento facial...")


imagens = []
identificadores = []


for numero_pessoa in os.listdir(pasta_rostos):

    caminho_pessoa = os.path.join(
        pasta_rostos,
        numero_pessoa
    )


    if not os.path.isdir(caminho_pessoa):
        continue


    try:
        identificador = int(numero_pessoa)
    except ValueError:
        continue


    for nome_foto in os.listdir(caminho_pessoa):

        if not nome_foto.lower().endswith(
            (".jpg", ".jpeg", ".png")
        ):
            continue


        caminho_imagem = os.path.join(
            caminho_pessoa,
            nome_foto
        )


        imagem = cv2.imread(
            caminho_imagem,
            cv2.IMREAD_GRAYSCALE
        )


        if imagem is None:
            continue


        imagem = cv2.resize(
            imagem,
            (200, 200)
        )


        imagens.append(imagem)

        identificadores.append(
            identificador
        )


if len(imagens) == 0:
    print("Nenhuma imagem foi encontrada.")
    exit()


# Cria o modelo que vai aprender os rostos
reconhecedor = cv2.face.LBPHFaceRecognizer_create()

reconhecedor.train(
    imagens,
    np.array(identificadores)
)

reconhecedor.write(
    arquivo_modelo
)


print()
print("-----------------------------")
print("CADASTRO FINALIZADO")
print("-----------------------------")
print()
print(f"{nome} foi cadastrado com sucesso.")
print(f"Fotos utilizadas: {fotos_tiradas}")
print()
print("Agora você pode executar o reconhecer.py")