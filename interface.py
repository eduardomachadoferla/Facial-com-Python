import tkinter as tk

from tkinter import (
    ttk,
    messagebox,
    simpledialog
)

import threading


from banco import (
    adicionar_usuario,
    listar_usuarios,
    editar_usuario,
    excluir_usuario,
    listar_acessos,
    limpar_acessos
)


from facial import (
    cadastrar_rosto,
    excluir_rosto,
    reconhecer,
    treinar_modelo
)


class Aplicativo:

    def __init__(
        self,
        janela
    ):

        self.janela = janela

        self.janela.title(
            "Sistema de Acesso Facial"
        )

        self.janela.geometry(
            "900x600"
        )


        self.criar_menu()

        self.mostrar_inicio()


    def criar_menu(self):

        self.menu = tk.Frame(
            self.janela,
            width=200
        )

        self.menu.pack(
            side="left",
            fill="y"
        )


        tk.Label(
            self.menu,
            text="ACESSO FACIAL",
            font=(
                "Arial",
                16,
                "bold"
            )
        ).pack(
            pady=30
        )


        tk.Button(
            self.menu,
            text="Inicio",
            width=20,
            command=self.mostrar_inicio
        ).pack(
            pady=5
        )


        tk.Button(
            self.menu,
            text="Cadastrar",
            width=20,
            command=self.cadastrar
        ).pack(
            pady=5
        )


        tk.Button(
            self.menu,
            text="Reconhecer",
            width=20,
            command=self.iniciar_reconhecimento
        ).pack(
            pady=5
        )


        tk.Button(
            self.menu,
            text="Usuarios",
            width=20,
            command=self.mostrar_usuarios
        ).pack(
            pady=5
        )


        tk.Button(
            self.menu,
            text="Historico",
            width=20,
            command=self.mostrar_historico
        ).pack(
            pady=5
        )


        self.conteudo = tk.Frame(
            self.janela
        )

        self.conteudo.pack(
            fill="both",
            expand=True
        )


    def limpar_tela(self):

        for item in (
            self.conteudo.winfo_children()
        ):

            item.destroy()


    def mostrar_inicio(self):

        self.limpar_tela()


        tk.Label(
            self.conteudo,
            text=(
                "Sistema de "
                "Reconhecimento Facial"
            ),
            font=(
                "Arial",
                24,
                "bold"
            )
        ).pack(
            pady=50
        )


        tk.Label(
            self.conteudo,
            text=(
                "Cadastre pessoas, "
                "reconheca rostos e "
                "acompanhe os acessos."
            ),
            font=(
                "Arial",
                12
            )
        ).pack()


    def cadastrar(self):

        nome = simpledialog.askstring(
            "Cadastro",
            "Digite o nome:"
        )


        if not nome:
            return


        id_usuario = (
            adicionar_usuario(
                nome
            )
        )


        def trabalho():

            sucesso = cadastrar_rosto(
                id_usuario,
                nome
            )


            if sucesso:

                self.janela.after(
                    0,
                    lambda: messagebox.showinfo(
                        "Cadastro",
                        (
                            f"{nome} cadastrado "
                            "com sucesso."
                        )
                    )
                )

            else:

                excluir_usuario(
                    id_usuario
                )


        threading.Thread(
            target=trabalho,
            daemon=True
        ).start()


    def iniciar_reconhecimento(self):

        threading.Thread(
            target=reconhecer,
            daemon=True
        ).start()


    def mostrar_usuarios(self):

        self.limpar_tela()


        tk.Label(
            self.conteudo,
            text="Usuarios cadastrados",
            font=(
                "Arial",
                20,
                "bold"
            )
        ).pack(
            pady=20
        )


        botoes = tk.Frame(
            self.conteudo
        )

        botoes.pack(
            pady=10
        )


        tk.Button(
            botoes,
            text="Editar",
            command=self.editar
        ).pack(
            side="left",
            padx=5
        )


        tk.Button(
            botoes,
            text="Excluir",
            command=self.excluir
        ).pack(
            side="left",
            padx=5
        )


        tk.Button(
            botoes,
            text="Recadastrar rosto",
            command=self.recadastrar
        ).pack(
            side="left",
            padx=5
        )


        self.tabela_usuarios = ttk.Treeview(
            self.conteudo,
            columns=(
                "id",
                "nome",
                "data"
            ),
            show="headings"
        )


        self.tabela_usuarios.heading(
            "id",
            text="ID"
        )

        self.tabela_usuarios.heading(
            "nome",
            text="Nome"
        )

        self.tabela_usuarios.heading(
            "data",
            text="Cadastro"
        )


        self.tabela_usuarios.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )


        for usuario in listar_usuarios():

            self.tabela_usuarios.insert(
                "",
                "end",
                values=usuario
            )


    def pegar_usuario_selecionado(self):

        item = (
            self.tabela_usuarios.selection()
        )


        if not item:

            messagebox.showwarning(
                "Aviso",
                "Selecione um usuario."
            )

            return None


        valores = (
            self.tabela_usuarios.item(
                item[0],
                "values"
            )
        )


        return (
            int(valores[0]),
            valores[1]
        )


    def editar(self):

        usuario = (
            self.pegar_usuario_selecionado()
        )


        if usuario is None:
            return


        id_usuario, nome = usuario


        novo_nome = (
            simpledialog.askstring(
                "Editar",
                "Digite o novo nome:",
                initialvalue=nome
            )
        )


        if not novo_nome:
            return


        editar_usuario(
            id_usuario,
            novo_nome
        )


        self.mostrar_usuarios()


    def excluir(self):

        usuario = (
            self.pegar_usuario_selecionado()
        )


        if usuario is None:
            return


        id_usuario, nome = usuario


        confirmar = messagebox.askyesno(
            "Excluir",
            f"Deseja excluir {nome}?"
        )


        if not confirmar:
            return


        excluir_rosto(
            id_usuario
        )


        excluir_usuario(
            id_usuario
        )


        treinar_modelo()


        self.mostrar_usuarios()


    def recadastrar(self):

        usuario = (
            self.pegar_usuario_selecionado()
        )


        if usuario is None:
            return


        id_usuario, nome = usuario


        threading.Thread(
            target=cadastrar_rosto,
            args=(
                id_usuario,
                nome
            ),
            daemon=True
        ).start()


    def mostrar_historico(self):

        self.limpar_tela()


        tk.Label(
            self.conteudo,
            text="Historico de acessos",
            font=(
                "Arial",
                20,
                "bold"
            )
        ).pack(
            pady=20
        )


        tk.Button(
            self.conteudo,
            text="Limpar historico",
            command=self.limpar_historico
        ).pack(
            pady=10
        )


        tabela = ttk.Treeview(
            self.conteudo,
            columns=(
                "id",
                "nome",
                "status",
                "data"
            ),
            show="headings"
        )


        tabela.heading(
            "id",
            text="ID"
        )

        tabela.heading(
            "nome",
            text="Pessoa"
        )

        tabela.heading(
            "status",
            text="Status"
        )

        tabela.heading(
            "data",
            text="Data e hora"
        )


        tabela.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )


        for acesso in listar_acessos():

            tabela.insert(
                "",
                "end",
                values=acesso
            )


    def limpar_historico(self):

        confirmar = messagebox.askyesno(
            "Historico",
            "Deseja apagar todo o historico?"
        )


        if confirmar:

            limpar_acessos()

            self.mostrar_historico()