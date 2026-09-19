import sqlite3
import os
from datetime import datetime


pasta_sistema = r"C:\Users\Public\reconhecimento_facial"

os.makedirs(
    pasta_sistema,
    exist_ok=True
)

arquivo_banco = os.path.join(
    pasta_sistema,
    "sistema.db"
)


def conectar():
    return sqlite3.connect(
        arquivo_banco
    )


def criar_banco():

    with conectar() as conexao:

        conexao.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                criado_em TEXT NOT NULL
            )
        """)

        conexao.execute("""
            CREATE TABLE IF NOT EXISTS acessos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                nome TEXT NOT NULL,
                status TEXT NOT NULL,
                data_hora TEXT NOT NULL
            )
        """)


def adicionar_usuario(nome):

    data = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )

    with conectar() as conexao:

        cursor = conexao.execute(
            """
            INSERT INTO usuarios (
                nome,
                criado_em
            )
            VALUES (?, ?)
            """,
            (
                nome,
                data
            )
        )

        return cursor.lastrowid


def listar_usuarios():

    with conectar() as conexao:

        return conexao.execute(
            """
            SELECT id, nome, criado_em
            FROM usuarios
            ORDER BY nome
            """
        ).fetchall()


def buscar_usuario(id_usuario):

    with conectar() as conexao:

        resultado = conexao.execute(
            """
            SELECT id, nome
            FROM usuarios
            WHERE id = ?
            """,
            (id_usuario,)
        ).fetchone()

        return resultado


def editar_usuario(
    id_usuario,
    novo_nome
):

    with conectar() as conexao:

        conexao.execute(
            """
            UPDATE usuarios
            SET nome = ?
            WHERE id = ?
            """,
            (
                novo_nome,
                id_usuario
            )
        )


def excluir_usuario(
    id_usuario
):

    with conectar() as conexao:

        conexao.execute(
            """
            DELETE FROM usuarios
            WHERE id = ?
            """,
            (id_usuario,)
        )


def registrar_acesso(
    usuario_id,
    nome,
    status
):

    data = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )

    with conectar() as conexao:

        conexao.execute(
            """
            INSERT INTO acessos (
                usuario_id,
                nome,
                status,
                data_hora
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                usuario_id,
                nome,
                status,
                data
            )
        )


def listar_acessos():

    with conectar() as conexao:

        return conexao.execute(
            """
            SELECT id, nome, status, data_hora
            FROM acessos
            ORDER BY id DESC
            """
        ).fetchall()


def limpar_acessos():

    with conectar() as conexao:

        conexao.execute(
            "DELETE FROM acessos"
        )