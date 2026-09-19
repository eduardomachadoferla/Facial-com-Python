import tkinter as tk

from banco import criar_banco

from interface import Aplicativo


criar_banco()


janela = tk.Tk()


app = Aplicativo(
    janela
)


janela.mainloop()