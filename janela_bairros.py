from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from bairrosv2 import *

class Tela_bairros(Local):
	"""docstring for Tela_bairros"""
	def __init__(self):
		super(Tela_bairros, self).__init__()
		self.root = Tk()
		self.root.title('Tabela - bairros')
		self.root.geometry('450x600')
		self.tabela()
		self.entradas()
		self.botoes()
		self.root.mainloop()

	def conectar(self):
		return super().conectar()

	def salvar(self, bairro, valor):
		return super().salvar(bairro, valor)

	def mostrar(self):
		return super().mostrar()

	def apagar(self, excluir):
		return super().apagar(excluir)

	def tabela(self):
		estilo = ttk.Style()

		estilo.theme_use('default')

		estilo.configure("Treeview",
                background="#D3D3D3",
                foreground="black",
                rowheight=25,
                fieldbackground="#D3D3D3")

		estilo.map('Treeview',
                background=[('selected', "#347083")])

		bairros_frame = Frame(self.root)
		bairros_frame.place(relx=0.0, rely=0.0, relwidth=0.95, relheight=0.65)

		barra = Scrollbar(bairros_frame)
		barra.place(relx=0.97, rely=0.05, relwidth=0.03, relheight=0.95)

		self.tb_bairros = ttk.Treeview(bairros_frame, yscrollcommand=barra.set,
                             selectmode="extended")
		self.tb_bairros.place(relx=0.05, rely=0.05, relwidth=0.92, relheight=0.98)

		barra.config(command=self.tb_bairros.yview)

		self.tb_bairros['columns'] = ("Bairro", "Valor")
		self.tb_bairros.column("#0", width=0, stretch=NO)
		self.tb_bairros.column("Bairro", anchor=W, width=250)
		self.tb_bairros.column("Valor", anchor=CENTER, width=100)

		self.tb_bairros.heading("#0", text= "", anchor=W)
		self.tb_bairros.heading("Bairro", text= "Bairros", anchor= CENTER)
		self.tb_bairros.heading("Valor", text= "Valor", anchor= CENTER)

		self.tb_bairros.tag_configure('oddrow', background="white")
		self.tb_bairros.tag_configure('evenrow', background="lightblue")

		conn = self.conectar()
		c = conn.cursor()
		c.execute("""SELECT * FROM bairros""")

		global contador
		contador = 0
		for i, b, v in c.fetchall():
			if contador % 2 == 0:
				self.tb_bairros.insert(parent='', index='0', text='',
		                       values=(b, v),
		                       tags=('evenrow',))
			else:
				self.tb_bairros.insert(parent='', index='0', text='',
		                       values=(b, v),
		                       tags=('oddrow',))

			contador += 1
			conn.close()
		self.tb_bairros.bind('<Double-Button-1>', self.seleciona)

	def atualiza_valor(self, valor, bairro):
		return super().atualiza_valor(valor, bairro)

	def atualiza_tabela(self):
		self.tb_bairros.delete(*self.tb_bairros.get_children())
		conn = self.conectar()
		c = conn.cursor()
		c.execute("""SELECT * FROM bairros
			GROUP BY nome_bairro""")
		global contador
		contador = 0

		for i, b, v in c.fetchall():
			if contador % 2 == 0:
				self.tb_bairros.insert(parent='', index='end', text='',
		                       values=(b, v),
		                       tags=('evenrow',))
			else:
				self.tb_bairros.insert(parent='', index='end', text='',
		                       values=(b, v),
		                       tags=('oddrow',))

			contador += 1
		conn.close()

	def seleciona(self, event):
			self.limpa(self.bairro_entry, self.valor_entry)
			for x in self.tb_bairros.selection():
				e, v  = self.tb_bairros.item(x, 'values')
				self.bairro_entry.insert(END, e)
				self.valor_entry.insert(END, v)
			
	def entradas(self):
		bairro_label = Label(self.root, text="Bairro")
		bairro_label.configure(font=('helvetica', 16))
		bairro_label.place(relx=0.18, rely=0.68, relwidth=0.15, relheight=0.1)
		self.bairro_entry = Entry(self.root)
		self.bairro_entry.place(relx=0.05, rely=0.75, relwidth=0.4, relheight=0.05)

		valor_label = Label(self.root, text="Valor")
		valor_label.configure(font=('helvetica', 16))
		valor_label.place(relx=0.72, rely=0.68, relwidth=0.15, relheight=0.1)
		self.valor_entry = Entry(self.root)
		self.valor_entry.place(relx=0.7, rely=0.75, relwidth=0.2, relheight=0.05)

	def botoes(self):
		add = Button(self.root, text="Adicionar", command = lambda: [self.salvar(self.bairro_entry.get().title(),
		self.valor_entry.get()), self.limpa(self.bairro_entry, self.valor_entry), self.atualiza_tabela()])
		add.place(relx=0.1, rely=0.85, relwidth=0.18, relheight=0.08)

		atualizar = Button(self.root, text="Atualizar\nvalor", command=lambda:[
		self.atualiza_valor(self.valor_entry.get() ,self.bairro_entry.get().title()),
		self.atualiza_tabela(), self.limpa(self.bairro_entry, self.valor_entry)])
		atualizar.place(relx=0.4, rely=0.85, relwidth=0.18, relheight=0.08)

		apagar = Button(self.root, text="Apagar", command= lambda: [self.apagar(self.bairro_entry.get().title()),
		self.limpa(self.bairro_entry, self.valor_entry), self.atualiza_tabela()])
		apagar.place(relx=0.7, rely=0.85, relwidth=0.18, relheight=0.08)
