from tkinter import *
from tkinter import ttk
from tkinter import font
from PIL import Image, ImageTk
from Cliente import *
from tela_cardapiov2 import *
import pedido

class tela_cliente(Cliente):
  def __init__(self, nome_c, end_c):
    super().__init__()
    self.root_clientes = Tk()
    self.root_clientes.title('Cliente')
    self.root_clientes.geometry('800x500')
    self.tabela()
    self.acessorios(nome_c, end_c)
    self.botoes()
    self.menu()
    self.root_clientes.mainloop()

  def conectar(self):
    return super().conectar()

  def mostrar(self):
    return super().mostrar()

  def salvar(self, nome, end):
    return super().salvar(nome, end)

  def apagar(self):
    return super().apagar()

  def atualizar(self, lista):
    return super().atualizar(lista)

  def limpa(self, nome, endereco):
    return super().limpa(nome, endereco)

  def pesquisar(self, nome, lista):
    lista.delete(*lista.get_children())
    
    conn = self.conectar()

    c = conn.cursor()

    nome_pesquisa =  nome + "%"
    c.execute("""SELECT cl.nome_cliente, cl.endereco, COUNT(pe.nome_cliente) FROM clientes as cl
            JOIN pedidos as pe on cl.nome_cliente = pe.nome_cliente
            WHERE cl.nome_cliente LIKE %s
            GROUP BY cl.nome_cliente""", (nome_pesquisa,))

    global contador_cliente
    contador_cliente = 0

    for nome, end, num in c.fetchall():
        if contador_cliente % 2 == 0:
            lista.insert(parent='', index='end', text='',
                           values=(nome, end, num),
                           tags=('evenrow',))

        else:
          lista.insert(parent='', index='end', text='',
                                 values=(nome, end, num),
                                 tags=('oddrow',))
        contador_cliente += 1
        conn.close()
  
  def menu(self):
    # Add Menu
    menu_opcaoes = Menu(self.root_clientes)
    self.root_clientes.config(menu=menu_opcaoes)
    # Configurar menu
    menu_cliente = Menu(menu_opcaoes, tearoff=0)
    menu_opcaoes.add_cascade(label="Opções", menu=menu_cliente)
        # opcoes do menu
    menu_cliente.add_command(label='Clientes', command=lambda:[self.clientes_geral()])
    menu_cliente.add_command(label='Clientes com pedidos', command=lambda:[self.tabela()])

  def clientes_geral(self):
    self.tree_frame.forget()
    estilo = ttk.Style()
    estilo.theme_use('default')
    estilo.configure("geral.Treeview", background="#D3D3D3", foreground="black",
                    rowheight=25, fieldbackground="#D3D3D3", font='Helvetica')
    estilo.map('geral.treeview', background=[('selected', "#347083")])
    self.geral_cliente_frame = Frame(self.root_clientes)
    self.geral_cliente_frame.place(relx=0.02, rely=0.05, relwidth=0.95, relheight=0.5)

    barra = Scrollbar(self.geral_cliente_frame)
    barra.place(relx=0.97, rely=0.0, relwidth=0.02, relheight=1)

    self.todos_clientes = ttk.Treeview(self.geral_cliente_frame, style= 'geral.Treeview', 
                                      yscrollcommand=barra.set, selectmode="extended")
    self.todos_clientes.place(relx=0.02, rely=0.0, relwidth=0.95, relheight=1)

    barra.config(command=self.todos_clientes.yview)

    self.todos_clientes['columns'] = ("Id", "Nome", "Endereço")
    self.todos_clientes.column("#0", width=0, stretch=NO)
    self.todos_clientes.column("Id", anchor=W, width=20)
    self.todos_clientes.column("Nome", anchor=CENTER, width=450)
    self.todos_clientes.column("Endereço", anchor=CENTER, width=200)

    self.todos_clientes.heading("#0", text="", anchor=W)
    self.todos_clientes.heading("Id", text="Id", anchor=CENTER)
    self.todos_clientes.heading("Nome", text="Nome", anchor=CENTER)
    self.todos_clientes.heading("Endereço", text="Endereço", anchor=CENTER)

    self.todos_clientes.tag_configure('cor1', background="white")
    self.todos_clientes.tag_configure('cor2', background="lightblue")

    conn = self.conectar()

    c = conn.cursor()
    c.execute("""SELECT * FROM clientes""")

    global contador_cliente
    contador_cliente = 0

    for idd, nome, loc in c.fetchall():
        if contador_cliente % 2 == 0:
            self.todos_clientes.insert(parent='', index='end', text='',
            values=(idd, nome, loc), tags=('cor2',))
        else:
          self.todos_clientes.insert(parent='', index='end', text='',
              values=(idd, nome, loc), tags=('cor1',))
        contador_cliente += 1
    conn.close()
    self.todos_clientes.bind('<Double-Button-1>', self.seleciona_cliente)

  def tabela(self):
    style = ttk.Style()
    style.theme_use('default')
    style.configure("cliente.Treeview",
                background="#D3D3D3",
                foreground="black",
                rowheight=25,
                fieldbackground="#D3D3D3",
                font='Helvetica')
    style.map('cliente.Treeview', background=[('selected', "#347083")])
    self.tree_frame = Frame(self.root_clientes)
    self.tree_frame.place(relx=0.02, rely=0.05, relwidth=0.95, relheight=0.5)

    self.tree_scroll = Scrollbar(self.tree_frame)
    self.tree_scroll.place(relx=0.97, rely=0.0, relwidth=0.02, relheight=1)

    self.lista = ttk.Treeview(self.tree_frame, style= 'cliente.Treeview', 
                              yscrollcommand=self.tree_scroll.set, selectmode="extended")
    self.lista.place(relx=0.02, rely=0.0, relwidth=0.95, relheight=1)

    self.tree_scroll.config(command=self.lista.yview)

    self.lista['columns'] = ("Nome", "Endereço", "Numero_de_pedidos")
    self.lista.column("#0", width=0, stretch=NO)
    self.lista.column("Nome", anchor=W, width=250)
    self.lista.column("Endereço", anchor=W, width=250)
    self.lista.column("Numero_de_pedidos", anchor=CENTER, width=200)

    self.lista.heading("#0", text="", anchor=W)
    self.lista.heading("Nome", text="Nome", anchor=CENTER)
    self.lista.heading("Endereço", text="Endereço", anchor=CENTER)
    self.lista.heading("Numero_de_pedidos", text="Numero de pedidos", anchor=CENTER)

    self.lista.tag_configure('cor1', background="white")
    self.lista.tag_configure('cor2', background="lightblue")

    conn = self.conectar()

    c = conn.cursor()
    c.execute("""SELECT cl.nome_cliente, cl.endereco, COUNT(pe.nome_cliente) 
                    FROM clientes as cl
                    JOIN pedidos as pe on cl.nome_cliente = pe.nome_cliente
                    GROUP BY cl.nome_cliente""")

    global contador_cliente
    contador_cliente = 0

    for nome, end, num in c.fetchall():
        if contador_cliente % 2 == 0:
            self.lista.insert(parent='', index='end', text='',
                           values=(nome, end, num),
                           tags=('cor2',))

        else:
          self.lista.insert(parent='', index='end', text='',
                                 values=(nome, end, num),
                                 tags=('cor1',))
        contador_cliente += 1
    conn.close()
    self.lista.bind('<Double-Button-1>', self.seleciona)

  def acessorios(self, nome_c, end_c):
    data_frame = LabelFrame(self.root_clientes, text= 'Novo cliente')
    data_frame.place(relx=0.05, rely=0.58, relwidth=0.9, relheight=0.25)

    nome_label = Label(data_frame, text="Nome")
    nome_label.configure(font=('helvetica', 16))
    nome_label.place(relx=0.15, rely=0.1, relwidth=0.2, relheight=0.35)
    self.nome_entry = Entry(data_frame)
    self.nome_entry.place(relx=0.1, rely=0.35, relwidth=0.3, relheight=0.25)
    self.nome_entry.delete(0, END)
    self.nome_entry.insert(0, nome_c)

    endereco_label = Label(data_frame, text="Bairro")
    endereco_label.configure(font=('helvetica', 16))
    endereco_label.place(relx=0.64, rely=0.1, relwidth=0.2, relheight=0.35)
    self.endereco_entry = Entry(data_frame)
    self.endereco_entry.place(relx=0.585, rely=0.35, relwidth=0.3, relheight=0.25)
    self.endereco_entry.delete(0, END)
    self.endereco_entry.insert(0, end_c)

  def botoes(self):
    lista = self.lista
    botao_salvar = Button(self.root_clientes, text= 'Cadastrar', command= lambda: [self.salvar(self.nome_entry.get().title(), self.endereco_entry.get().title()),
      self.limpa(self.nome_entry, self.endereco_entry)])
    botao_salvar.configure(font=('Roman', 14))
    botao_salvar.place(relx=0.1, rely=0.85, relwidth=0.15, relheight=0.1)

    new_pedido = Button(self.root_clientes, text= 'Novo\nPedido', command= lambda:[
    tela_cardapio(self.root_clientes, self.nome_entry.get().title(), 
    self.endereco_entry.get().title())])
    new_pedido.configure(font=('Roman', 14))
    new_pedido.place(relx=0.42, rely=0.85, relwidth=0.15, relheight=0.12)

    pesquisar = Button(self.root_clientes, text= 'Pesquisar', command= lambda: [self.pesquisar(
    self.nome_entry.get(), self.lista),
    self.limpa(self.nome_entry, self.endereco_entry)])
    pesquisar.configure(font=('Roman', 14))
    pesquisar.place(relx=0.75, rely=0.85, relwidth=0.15, relheight=0.1)
  
  def inserir(self, name, end):
    self.nome_entry.insert(name, 'end')
    self.endereco_entry.insert(end, 'end')

  def seleciona(self, event):
    self.limpa(self.nome_entry, self.endereco_entry)
    for x in self.lista.selection():
      n, e, p = self.lista.item(x, 'values')
      self.nome_entry.insert(END, n)
      self.endereco_entry.insert(END, e)
    return self.nome_entry.get()
  
  def seleciona_cliente(self, event):
    self.limpa(self.nome_entry, self.endereco_entry)
    for x in self.todos_clientes.selection():
      i, n, e= self.todos_clientes.item(x, 'values')
      self.nome_entry.insert(END, n)
      self.endereco_entry.insert(END, e)

  def dados(self):
    name = self.nome_entry.get()
    local = self.endereco_entry.get()
    print(name, local)
    return name, local




#c = tela_cliente('nome', 'end')
#c