import cv2
import os
import shutil
import numpy as np

from banco import (
    listar_usuarios,
    buscar_usuario,
    registrar_acesso
)

from voz import falar


pasta_sistema = r"C:\Users\Public\reconhecimento_facial"

pasta_rostos = os.path.join(
    pasta_sistema,
    "rostos"
)

arquivo_modelo = os.path.join(
    pasta_sistema,
    "modelo.yml"
)

arquivo_detector = os.path.join(
    pasta_sistema,
    "haarcascade_frontalface_default.xml"
)


os.makedirs(
    pasta_rostos,
    exist_ok=True
)


def preparar_detector():

    if not os.path.exists(
        arquivo_detector
    ):

        origem = os.path.join(
            cv2.data.haarcascades,
            "haarcascade_frontalface_default.xml"
        )

        shutil.copyfile(
            origem,
            arquivo_detector
        )


def pegar_detector():

    preparar_detector()

    detector = cv2.CascadeClassifier(
        arquivo_detector
    )

    return detector


def cadastrar_rosto(
    id_usuario,
    nome
):

    detector = pegar_detector()

    pasta_pessoa = os.path.join(
        pasta_rostos,
        str(id_usuario)
    )

    if os.path.exists(
        pasta_pessoa
    ):
        shutil.rmtree(
            pasta_pessoa
        )

    os.makedirs(
        pasta_pessoa
    )


    camera = cv2.VideoCapture(0)

    if not camera.isOpened():

        return False


    fotos = 0

    total_fotos = 40

    contador = 0


    while fotos < total_fotos:

        conseguiu, imagem = camera.read()

        if not conseguiu:
            break


        imagem = cv2.flip(
            imagem,
            1
        )


        cinza = cv2.cvtColor(
            imagem,
            cv2.COLOR_BGR2GRAY
        )


        rostos = detector.detectMultiScale(
            cinza,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(120, 120)
        )


        if len(rostos) > 0:

            x, y, largura, altura = max(
                rostos,
                key=lambda r: r[2] * r[3]
            )


            cv2.rectangle(
                imagem,
                (x, y),
                (
                    x + largura,
                    y + altura
                ),
                (0, 255, 0),
                2
            )


            contador += 1


            if contador >= 5:

                contador = 0


                rosto = cinza[
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


                fotos += 1


                cv2.imwrite(
                    os.path.join(
                        pasta_pessoa,
                        f"{fotos}.jpg"
                    ),
                    rosto
                )


        cv2.putText(
            imagem,
            f"{nome}: {fotos}/{total_fotos}",
            (30, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )


        cv2.putText(
            imagem,
            "Movimente um pouco o rosto",
            (30, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )


        cv2.putText(
            imagem,
            "Q para cancelar",
            (30, 115),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )


        cv2.imshow(
            "Cadastro Facial",
            imagem
        )


        tecla = cv2.waitKey(1) & 0xFF


        if tecla == ord("q"):

            camera.release()

            cv2.destroyAllWindows()

            return False


    camera.release()

    cv2.destroyAllWindows()


    treinar_modelo()

    return True


def treinar_modelo():

    imagens = []

    ids = []


    usuarios = listar_usuarios()


    for id_usuario, nome, data in usuarios:

        pasta_pessoa = os.path.join(
            pasta_rostos,
            str(id_usuario)
        )


        if not os.path.exists(
            pasta_pessoa
        ):
            continue


        for arquivo in os.listdir(
            pasta_pessoa
        ):

            caminho = os.path.join(
                pasta_pessoa,
                arquivo
            )


            imagem = cv2.imread(
                caminho,
                cv2.IMREAD_GRAYSCALE
            )


            if imagem is None:
                continue


            imagem = cv2.resize(
                imagem,
                (200, 200)
            )


            imagens.append(
                imagem
            )

            ids.append(
                id_usuario
            )


    if len(imagens) == 0:

        if os.path.exists(
            arquivo_modelo
        ):

            os.remove(
                arquivo_modelo
            )

        return


    reconhecedor = (
        cv2.face.LBPHFaceRecognizer_create()
    )


    reconhecedor.train(
        imagens,
        np.array(ids)
    )


    reconhecedor.write(
        arquivo_modelo
    )


def excluir_rosto(
    id_usuario
):

    pasta_pessoa = os.path.join(
        pasta_rostos,
        str(id_usuario)
    )


    if os.path.exists(
        pasta_pessoa
    ):

        shutil.rmtree(
            pasta_pessoa
        )


    treinar_modelo()


def reconhecer():

    if not os.path.exists(
        arquivo_modelo
    ):

        return False


    detector = pegar_detector()


    reconhecedor = (
        cv2.face.LBPHFaceRecognizer_create()
    )


    reconhecedor.read(
        arquivo_modelo
    )


    camera = cv2.VideoCapture(0)


    if not camera.isOpened():

        return False


    ultimo_id = None

    confirmacoes = 0

    acesso_registrado = False

    limite = 65


    while True:

        conseguiu, imagem = camera.read()


        if not conseguiu:
            break


        imagem = cv2.flip(
            imagem,
            1
        )


        cinza = cv2.cvtColor(
            imagem,
            cv2.COLOR_BGR2GRAY
        )


        rostos = detector.detectMultiScale(
            cinza,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(120, 120)
        )


        mensagem = "PROCURANDO ROSTO..."


        for x, y, largura, altura in rostos:

            rosto = cinza[
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


            id_usuario, distancia = (
                reconhecedor.predict(
                    rosto
                )
            )


            usuario = buscar_usuario(
                id_usuario
            )


            if (
                distancia < limite
                and usuario is not None
            ):

                nome = usuario[1]


                if ultimo_id == id_usuario:

                    confirmacoes += 1

                else:

                    ultimo_id = id_usuario

                    confirmacoes = 1

                    acesso_registrado = False


                if confirmacoes >= 8:

                    mensagem = (
                        f"OLA {nome.upper()}!"
                    )

                    texto = nome

                    cor = (
                        0,
                        255,
                        0
                    )


                    if not acesso_registrado:

                        registrar_acesso(
                            id_usuario,
                            nome,
                            "Liberado"
                        )


                        falar(
                            f"Ola {nome}. "
                            "Acesso liberado."
                        )


                        acesso_registrado = True


                else:

                    mensagem = (
                        "VERIFICANDO..."
                    )

                    texto = (
                        "Verificando"
                    )

                    cor = (
                        0,
                        255,
                        255
                    )


            else:

                texto = "Desconhecido"

                mensagem = (
                    "ACESSO NEGADO"
                )

                cor = (
                    0,
                    0,
                    255
                )


            cv2.rectangle(
                imagem,
                (x, y),
                (
                    x + largura,
                    y + altura
                ),
                cor,
                3
            )


            cv2.putText(
                imagem,
                texto,
                (
                    x,
                    y - 15
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                cor,
                2
            )


            cv2.putText(
                imagem,
                f"Distancia: {distancia:.1f}",
                (
                    x,
                    y + altura + 30
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                cor,
                2
            )


        cv2.rectangle(
            imagem,
            (0, 0),
            (
                imagem.shape[1],
                70
            ),
            (0, 0, 0),
            -1
        )


        cv2.putText(
            imagem,
            mensagem,
            (20, 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
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

    return True