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
			self.conectar()

			self.root.mainloop()

		def background(self):
			imagem = Image.open('Imagens/indice.png')
			photo = ImageTk.PhotoImage(imagem)
			fundo = Label(self.root, image= photo, anchor='n', background = 'snow')
			fundo.image = photo
			fundo.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)
			self.root.configure(background = 'snow')

		def frames(self):
			self.framebotao = Frame(self.root)
			self.framebotao.place(relx = 0.0, rely = 0.65, relwidth = 1,
								relheight = 0.35)
			self.framebotao.configure(background = '#FFFAFA')

		def widegets(self):
			bt2 = Image.open('Imagens/clientes.ico')
			img2 = ImageTk.PhotoImage(bt2)
			bt3 = Image.open('Imagens/delivery-man.png')
			img3 = ImageTk.PhotoImage(bt3)
			
			cadastra_cliente = Button(self.framebotao, text = 'Clientes', image=img2, compound=LEFT,
			relief=FLAT, activebackground='#87CEEB',
			activeforeground='#0000FF', anchor='w', command= lambda: 
			[tela_cliente(self.root)])
			cadastra_cliente.place(relx = 0.22, rely = 0.5, relwidth = 0.18,
										relheight = 0.35)
			cadastra_cliente.imagem = img2
			cadastra_cliente['background'] = 'Snow'
			cadastra_cliente.configure(font = ('Helvetica', 16))
			
			consultar = Button(self.framebotao, text = 'Entregas', image=img3, compound=LEFT,
			relief=SUNKEN, activebackground='Crimson',
			activeforeground='DarkGreen', command = lambda: [Janela(self.root)])
			consultar.place(relx = 0.62, rely = 0.5, relwidth = 0.18,
										relheight = 0.35)
			consultar.imagem = img3
			consultar['background'] = 'Snow'
			consultar.configure(font = ('Helvetica', 16))	
					
	except Exception as erro:
		print(erro)

principal = Janela_principal()

principal
