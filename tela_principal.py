from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from Tela import * 
from tela_cardapiov2 import *
from tela_cliente import tela_cliente
from Tela import Janela
from pedido import Pedido

class Janela_principal(Pedido):
	try:
		def __init__(self):
			super(Janela_principal, self).__init__()
			self.root = Tk()
			self.root.title('Restaurante')
			self.root.geometry('800x500')
			self.background()
			self.frames()
			self.widegets()
			self.entradas()
			self.conectar()

			self.root.mainloop()

		def background(self):
			imagem = Image.open('Health.jpeg')
			photo = ImageTk.PhotoImage(imagem)
			fundo = Label(self.root, image= photo)
			fundo.image = photo
			fundo.place(relx=0.0, rely=0.0, relwidth=0.1, relheight=0.1)
			self.root.configure(background = '#FFFAFA')

		def frames(self):
			self.framebotao = Frame(self.root)
			self.framebotao.place(relx = 0.0, rely = 0.65, relwidth = 1,
								relheight = 0.35)
			self.framebotao.configure(background = '#FFFAFA')

		def widegets(self):
			novo_pedido = Button(self.framebotao, text = 'Pedidos', relief=GROOVE, activebackground='#FFB6C1',
			activeforeground='snow' ,command= lambda: 
			[tela_cardapio(self.root, self.nome_entry.get(), self.endereco_entry.get())])
			novo_pedido.place(relx = 0.1, rely = 0.5, relwidth = 0.15,
										relheight = 0.35)
			novo_pedido['background'] = 'Snow'
			novo_pedido.configure(font = ('Helvetica', 16))
			
			cadastra_cliente = Button(self.framebotao, text = 'Clientes', relief=FLAT, activebackground='#87CEEB',
			activeforeground='#0000FF', command= lambda: 
			[tela_cliente(self.root, self.nome_entry.get(), self.endereco_entry.get())])
			cadastra_cliente.place(relx = 0.42, rely = 0.5, relwidth = 0.15,
										relheight = 0.35)
			cadastra_cliente['background'] = 'Snow'
			cadastra_cliente.configure(font = ('Helvetica', 16))
			
			consultar = Button(self.framebotao, text = 'Entregas', relief=SUNKEN, activebackground='Crimson',
			activeforeground='DarkGreen', command = lambda: [Janela(self.root)])
			consultar.place(relx = 0.72, rely = 0.5, relwidth = 0.15,
										relheight = 0.35)
			consultar['background'] = 'Snow'
			consultar.configure(font = ('Helvetica', 16))	
			
		def entradas(self):
			nome_label = Label(self.framebotao, text="Cliente")
			nome_label.configure(font=('helvetica', 16))
			nome_label.place(relx=0.25, rely=0.05, relwidth=0.15, relheight=0.18)
			nome_label['background'] = 'Snow'
			self.nome_entry = Entry(self.framebotao)
			self.nome_entry.place(relx=0.2, rely=0.2, relwidth=0.25, relheight=0.2)

			endereco_label = Label(self.framebotao, text="Endereço")
			endereco_label.configure(font=('helvetica', 16))
			endereco_label.place(relx=0.6, rely=0.05, relwidth=0.15, relheight=0.18)
			endereco_label['background'] = 'Snow'
			self.endereco_entry = Entry(self.framebotao)
			self.endereco_entry.place(relx=0.55, rely=0.2, relwidth=0.25, relheight=0.2)		
	except Exception as erro:
		print(erro)

principal = Janela_principal()

principal
