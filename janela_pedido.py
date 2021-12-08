from tkinter import *
from tkinter import ttk
from pedido import *
from PIL import Image, ImageTk
from tela_cardapiov2 import tela_cardapio

class jan_pedido(Pedido):
	"""docstring for janela_pedido"""
	def __init__(self, nome_c):
		super(jan_pedido, self).__init__()
		self.root = Tk()
		self.root.geometry('600x500')
		self.root.title('Novo pedido')
		self.infos(nome_c)
		self.acessorios()
		#self.tabela_pedido(tela_cardapio.tabela())
		self.root.mainloop()


	def conectar(self):
		return super().conectar()

	def salvar(self, nome, end, func):
		return super().salvar(nome, end, func)

	def novo_pedido(self, nome_c, prato, func):
		return super().novo_pedido(nome_c, prato, func)

	def add_prato(self, nome_c, prato):
		return super().add_prato(nome_c, prato)

	def somar(self, nome_c):
		return super().somar(nome_c)

	def seleciona(self):
		return super().seleciona()

	def limpa(self, nome, endereco):
		return super().limpa(nome, endereco)

	def infos(self, nome_c):
		self.lb1 = LabelFrame(self.root, text=nome_c)
		self.lb1.place(relx=0.025, rely=0.05, relwidth=0.95, relheight=0.75)

		conn = self.conectar()
		c = conn.cursor()
		c.execute("""SELECT endereco FROM clientes WHERE nome_cliente = %s""", (nome_c,))
		end_bd = c.fetchall()
		endereco_cliente = end_bd[0][0]
		label_endereco = Label(self.lb1, text='Endereço:')
		label_endereco.place(relx=0.025, rely=0.05, relwidth=0.15, relheight=0.08)
		entry_endereco = Entry(self.lb1)
		entry_endereco.place(relx=0.18, rely=0.05, relwidth=0.4, relheight=0.08)
		entry_endereco.delete(0, END)
		entry_endereco.insert(0, endereco_cliente)

	#def tabela_pedido(self, tabela):
		tree_scroll = Scrollbar(self.lb1)
		tree_scroll.place(relx=0.9, rely=0.2, relwidth=0.02, relheight=0.6)

		tabela = ttk.Treeview(self.lb1, yscrollcommand=tree_scroll.set,
                             selectmode="extended")
		tabela.place(relx=0.05, rely=0.2, relwidth=0.85, relheight=0.6)

		tree_scroll.config(command=tabela.yview)
		

	def acessorios(self):
		cardapio = Button(self.lb1, text='Adicionar Prato', command=lambda:[])
		cardapio.place(relx=0.75, rely=0.85, relwidth=0.2, relheight=0.1)
