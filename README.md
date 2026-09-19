# Reconhecimento Facial com Python

Esse é um projeto simples de reconhecimento facial feito em Python usando OpenCV.

A ideia do projeto é permitir cadastrar uma pessoa pela webcam e depois reconhecer o rosto dela, mostrando o nome na tela.

O sistema tira algumas fotos do rosto durante o cadastro, treina um modelo com essas imagens e depois usa a webcam para comparar o rosto que está aparecendo com os rostos que já foram cadastrados.

## Tecnologias usadas

* Python
* OpenCV
* NumPy
* LBPH Face Recognizer

## Arquivos principais

`cadastrar.py`

Usado para cadastrar uma nova pessoa. O programa pede o nome, abre a câmera e tira várias fotos do rosto.

`reconhecer.py`

Abre a câmera e tenta reconhecer uma das pessoas que já foram cadastradas.

## Como instalar

Primeiro é necessário ter o Python instalado no computador.

O projeto foi testado usando Python 3.13.

Depois de baixar ou clonar o projeto, abra a pasta no VS Code e abra o terminal.

Instale as bibliotecas necessárias:

```bash
python -m pip install opencv-contrib-python==4.14.0.94
```

E também:

```bash
python -m pip install numpy
```

Para verificar se o OpenCV foi instalado corretamente:

```bash
python -c "import cv2; print(cv2.__version__)"
```

## Como cadastrar uma pessoa

Execute:

```bash
python cadastrar.py
```

O programa vai pedir o nome da pessoa:

```text
Digite o nome da pessoa que será cadastrada:
```

Digite o nome e pressione Enter.

Exemplo:

```text
Eduardo
```

A câmera será aberta.

Durante o cadastro:

* olhe para a câmera;
* movimente um pouco o rosto;
* vire levemente para a esquerda e para a direita;
* aproxime e afaste um pouco o rosto.

O sistema vai tirar 40 fotos automaticamente.

Quando terminar, o modelo de reconhecimento será treinado.

## Como reconhecer uma pessoa

Depois de cadastrar pelo menos uma pessoa, execute:

```bash
python reconhecer.py
```

A webcam será aberta.

Se o rosto for reconhecido, aparecerá o nome da pessoa na tela.

Exemplo:

```text
Ola, Eduardo!
```

Se o sistema não reconhecer o rosto, aparecerá:

```text
ROSTO NAO CADASTRADO
```

Para fechar a câmera, pressione:

```text
Q
```

## Onde ficam os cadastros

Os arquivos do reconhecimento ficam salvos em:

```text
C:\Users\Public\reconhecimento_facial
```

A estrutura fica parecida com:

```text
reconhecimento_facial
│
├── nomes.json
├── modelo_lbph.yml
├── haarcascade_frontalface_default.xml
│
└── rostos
    ├── 1
    │   ├── 1.jpg
    │   ├── 2.jpg
    │   └── ...
    │
    └── 2
        ├── 1.jpg
        ├── 2.jpg
        └── ...
```

O arquivo `nomes.json` guarda os nomes cadastrados.

A pasta `rostos` guarda as imagens usadas para treinar o reconhecimento.

O arquivo `modelo_lbph.yml` guarda o modelo treinado.

## Cadastrar mais pessoas

É só executar novamente:

```bash
python cadastrar.py
```

Digitar outro nome e fazer o cadastro normalmente.

Depois disso o modelo é treinado novamente usando todas as pessoas cadastradas.

## Observação

Esse projeto foi feito para estudo e aprendizado de Python e visão computacional.

O reconhecimento ainda é simples e não deve ser usado como sistema de segurança real, porque por enquanto não existe uma verificação avançada de prova de vida.

Algumas melhorias que pretendo adicionar futuramente são:

* detectar piscada;
* criar uma interface gráfica;
* salvar histórico de acessos;
* cadastrar usuários pela própria interface;
* criar níveis de acesso;
* transformar o projeto em um aplicativo para Windows.

## Autor

Eduardo
