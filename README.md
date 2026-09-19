# Reconhecimento Facial com Python

Projeto de reconhecimento facial feito em Python utilizando OpenCV.

O sistema permite cadastrar pessoas pela webcam, reconhecer rostos cadastrados, registrar histórico de acessos e gerenciar usuários através de uma interface gráfica.

Também possui resposta por voz quando o acesso é liberado.

## Funcionalidades

- Cadastro facial pela webcam
- Reconhecimento de pessoas cadastradas
- Interface gráfica
- Histórico de acessos
- Data e hora dos acessos
- Editar nome de usuários
- Excluir usuários
- Recadastrar rosto
- Resposta por voz
- Registro de acesso liberado
- Banco de dados SQLite

## Tecnologias utilizadas

- Python
- OpenCV
- OpenCV Contrib
- NumPy
- Tkinter
- SQLite

## Estrutura do projeto

```text
Facial-com-Python/
│
├── main.py
├── interface.py
├── facial.py
├── banco.py
├── voz.py
└── README.md
```

## Arquivos

### main.py

Arquivo principal do projeto.

É através dele que o sistema é iniciado.

### interface.py

Responsável pela interface gráfica do programa.

Nele estão as telas de início, cadastro, reconhecimento, usuários e histórico.

### facial.py

Responsável pelo reconhecimento facial.

Nesse arquivo estão as funções de abrir a webcam, detectar rostos, tirar fotos, treinar o modelo e reconhecer pessoas cadastradas.

### banco.py

Responsável pelo banco de dados SQLite.

Guarda informações como usuários cadastrados, nome, data do cadastro e histórico de acessos.

### voz.py

Responsável pela resposta de voz do sistema.

Quando uma pessoa é reconhecida, o Windows pode falar:

```text
Olá Eduardo. Acesso liberado.
```

## Requisitos

É necessário ter o Python instalado.

O projeto foi desenvolvido utilizando Python 3.13.

Para verificar a versão:

```bash
python --version
```

## Instalação

Clone o repositório:

```bash
git clone https://github.com/eduardomachadoferla/Facial-com-Python.git
```

Entre na pasta:

```bash
cd Facial-com-Python
```

Instale as bibliotecas necessárias:

```bash
python -m pip install opencv-contrib-python==4.14.0.94 numpy
```

## Como executar

Execute:

```bash
python main.py
```

A interface do sistema será aberta.

## Cadastrar uma pessoa

Na interface clique em:

```text
Cadastrar
```

Digite o nome da pessoa.

A webcam será aberta e o sistema irá tirar várias fotos automaticamente.

Durante o cadastro:

- olhe para a câmera
- movimente um pouco o rosto
- vire levemente para os lados
- aproxime e afaste o rosto

Depois das fotos serem capturadas, o sistema treina novamente o modelo de reconhecimento.

## Reconhecimento

Clique em:

```text
Reconhecer
```

A webcam será aberta.

Se o rosto estiver cadastrado, o sistema irá mostrar o nome da pessoa.

Exemplo:

```text
OLA EDUARDO!
```

Além disso, o computador poderá falar:

```text
Olá Eduardo. Acesso liberado.
```

Para fechar a câmera pressione:

```text
Q
```

## Usuários

Na tela de usuários é possível visualizar as pessoas cadastradas.

Também é possível:

- editar o nome
- excluir uma pessoa
- recadastrar o rosto

Ao excluir uma pessoa, as imagens utilizadas no reconhecimento também são removidas.

## Histórico de acessos

Cada reconhecimento confirmado é registrado no banco de dados.

O histórico mostra:

```text
Pessoa
Status
Data
Hora
```

Exemplo:

```text
Eduardo | Liberado | 19/09/2026 20:30:15
```

O histórico também pode ser apagado pela interface.

## Onde os dados são armazenados

Os dados ficam armazenados localmente no computador em:

```text
C:\Users\Public\reconhecimento_facial
```

A estrutura fica parecida com:

```text
reconhecimento_facial/
│
├── sistema.db
├── modelo.yml
├── haarcascade_frontalface_default.xml
│
└── rostos/
    ├── 1/
    │   ├── 1.jpg
    │   ├── 2.jpg
    │   └── ...
    │
    └── 2/
        ├── 1.jpg
        ├── 2.jpg
        └── ...
```

## Banco de dados

O projeto utiliza SQLite.

O arquivo:

```text
sistema.db
```

armazena os usuários e o histórico de acessos.

## Privacidade

As imagens dos rostos não devem ser enviadas para o GitHub.

É recomendado adicionar ao `.gitignore`:

```gitignore
__pycache__/
*.pyc
*.db
*.yml
rostos/
```

Assim os dados das pessoas cadastradas continuam apenas no computador onde o programa está sendo executado.

## Observação

Esse projeto foi criado para estudo de Python, visão computacional, reconhecimento facial, banco de dados e interface gráfica.

O sistema não deve ser usado como único método de segurança em situações reais.

O reconhecimento atual ainda pode ser melhorado com técnicas como prova de vida.

## Melhorias futuras

- detecção de piscada
- prova de vida
- tela de login
- níveis de acesso
- foto de tentativas de acesso negadas
- exportar histórico
- modo escuro
- transformar em executável `.exe`
- criar instalador para Windows
- melhorar o reconhecimento facial

## Autor

Eduardo Machado Ferla
