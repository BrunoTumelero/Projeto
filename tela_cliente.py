from os import error
from tkinter import *
from tkinter import ttk
from tkinter import font
from PIL import Image, ImageTk
from Cliente import *
from cardapio_v2 import Cardapio, Modelo_prato
from pedido import *
from bairrosv2 import Local

class tela_cliente(Cliente):
  def __init__(self, root):
    super().__init__()
    self.root = root
    self.root_clientes = Toplevel(root)
    self.root_clientes.title('Cliente')
    self.root_clientes.geometry('800x500')
    self.tabela()
    self.acessorios()
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

    nome_pesquisa = f'%{nome}%'.title()
    c.execute("""SELECT cl.nome_cliente, cl.endereco, COUNT(pe.nome_cliente) FROM clientes as cl
            JOIN pedidos as pe on cl.nome_cliente = pe.nome_cliente
            WHERE cl.nome_cliente LIKE %s
            GROUP BY cl.nome_cliente""", (nome_pesquisa,))

    global contador_cliente
    contador_cliente = 0

    for nome, end, num in c.fetchall():
        if contador_cliente % 2 == 0:
            lista.insert(parent='', index='0', text='',
                           values=(nome, end, num),
                           tags=('cor1',))

        else:
          lista.insert(parent='', index='0', text='',
                                 values=(nome, end, num),
                                 tags=('cor2',))
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

  def acessorios(self):
    data_frame = LabelFrame(self.root_clientes, text= 'Novo cliente')
    data_frame.place(relx=0.05, rely=0.58, relwidth=0.9, relheight=0.25)

    nome_label = Label(data_frame, text="Nome")
    nome_label.configure(font=('helvetica', 16))
    nome_label.place(relx=0.15, rely=0.1, relwidth=0.2, relheight=0.35)
    self.nome_entry = Entry(data_frame)
    self.nome_entry.place(relx=0.1, rely=0.35, relwidth=0.3, relheight=0.25)

    endereco_label = Label(data_frame, text="Bairro")
    endereco_label.configure(font=('helvetica', 16))
    endereco_label.place(relx=0.64, rely=0.1, relwidth=0.2, relheight=0.35)
    self.endereco_entry = Entry(data_frame)
    self.endereco_entry.place(relx=0.585, rely=0.35, relwidth=0.3, relheight=0.25)

  def botoes(self):
    global bt_cadastra
    bt_cadastra = Image.open('Imagens/add.ico')
    img1 = ImageTk.PhotoImage(bt_cadastra)
    lista = self.lista
    botao_salvar = Button(self.root_clientes, text= 'Cadastrar', image= img1, compound=LEFT,
    command= lambda: [self.salvar(self.nome_entry.get().title(), self.endereco_entry.get().title()),
    self.limpa(self.nome_entry, self.endereco_entry)])
    botao_salvar.configure(font=('Roman', 14))
    botao_salvar.place(relx=0.1, rely=0.85, relwidth=0.18, relheight=0.1)
    botao_salvar.imagem = img1

    bt_fpedido = Image.open('Imagens/pagar.png')
    img_fpedido = ImageTk.PhotoImage(bt_fpedido)
    bt_new = Image.open('Imagens/carrinho.ico')
    img_new = ImageTk.PhotoImage(bt_new)
    new_pedido = Button(self.root_clientes, text= 'Novo\nPedido', image= img_new, compound=LEFT,
    command= lambda:[tela_cardapio(self.root, self.root_clientes, self.nome_entry.get().title(),
    self.endereco_entry.get().title())])
    new_pedido.configure(font=('Roman', 14))
    new_pedido.place(relx=0.42, rely=0.85, relwidth=0.15, relheight=0.12)
    new_pedido.imagem = img_new

    bt_pesquisa = Image.open('Imagens/consultar.ico')
    img_pesquisar = ImageTk.PhotoImage(bt_pesquisa)
    pesquisar = Button(self.root_clientes, text= 'Pesquisar', image= img_pesquisar, compound=LEFT,
    command= lambda: [self.pesquisar(self.nome_entry.get(), self.lista), 
    self.limpa(self.nome_entry, self.endereco_entry)])
    pesquisar.configure(font=('Roman', 14))
    pesquisar.place(relx=0.75, rely=0.85, relwidth=0.18, relheight=0.1)
    pesquisar.imagem = img_pesquisar
  
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

class tela_cardapio(Cardapio, Pedido, Local):
    def __init__(self, root, root_cardapio, info_cliente, end_cliente,):
        super().__init__()
        root_cardapio.destroy()
        self.root_cardapio = Toplevel(root)
        self.root_cardapio.title('Cardapio')
        self.root_cardapio.geometry('800x500')
        self.menu_geral()
        self.monte_poke()
        self.opcoes()
        self.acessorios()
        self.verificacao(info_cliente)
        self.info_cliente = info_cliente
        self.end_cliente = end_cliente
        self.nome_pedido(info_cliente)
        self.tabela()
        self.valor_total = 0
        self.total_pedido(self.valor_total)
        self.modelo = Modelo_prato()
        self.carrinho_compras = []
        self.memoria = {}
        self.quant = 1
        self.contador = 0

    def conectar(self):
        return super().conectar()

    def adicionar(self, prato, valor, categoria):
        return super().adicionar(prato, valor, categoria)

    def apagar(self, prato):
        return super().apagar(prato)

    def atualizar(self, prato, valor):
        return super().atualizar(prato, valor)

    def exibir_pratos(self):
        return super().exibir_pratos()

    def limpa(self, nome, valor):
        return super().limpa(nome, valor)

    def novo_pedido(self, nome_c, prato, func, tele, tipo, data):
        return super().novo_pedido(nome_c, prato, func, tele, tipo, data)

    def valor_ifood(self):
        return super().valor_ifood()

    def retirada(self):
        return super().retirada()

    def valor_tele(self, bairro):
        return super().valor_tele(bairro)

    def nome_pedido(self, nome_cliente):
        self.name = LabelFrame(self.root_cardapio, text=nome_cliente)
        self.name.place(relx=0.665, rely=0.07, relwidth=0.32, relheight=0.55)

    def opcoes(self):
        # Add Menu
        my_menu = Menu(self.root_cardapio)
        self.root_cardapio.config(menu=my_menu)

        # Configurar menu
        option_menu = Menu(my_menu, tearoff=0)
        my_menu.add_cascade(label="Opções", menu=option_menu)
        # opcoes do menu
        option_menu.add_command(label="Cardapio", command= lambda:[self.add_prato()])

    def add_prato(self):
        self.janela = Toplevel(self.root_cardapio)
        self.janela.title('Configurações - cardapio')
        self.janela.geometry('600x200')

        #Labels e Entrys
        lb_prato = Label(self.janela, text='Prato')
        lb_prato.place(relx=0.12, rely=0.08, relwidth=0.15, relheight=0.15)
        ent_prato = Entry(self.janela)
        ent_prato.place(relx=0.05, rely=0.25, relwidth=0.3, relheight=0.12)

        lb_valor = Label(self.janela, text='Valor')
        lb_valor.place(relx=0.45, rely=0.08, relwidth=0.15, relheight=0.15)
        ent_valor = Entry(self.janela)
        ent_valor.place(relx=0.43, rely=0.25, relwidth=0.2, relheight=0.12)

        cat_label = Label(self.janela, text='Catedoria')
        cat_label.place(relx=0.75, rely=0.08, relwidth=0.15, relheight=0.15)
        self.categoria_prato = ttk.Combobox(self.janela, values=['Snack', 'Bowl', 'Salada', 'Brunch',
        'Pizza', 'Burger', 'Poke', 'Doce', 'Café', 'Suco', 'Bebida'])
        self.categoria_prato.place(relx=0.72, rely=0.25, relwidth=0.2, relheight=0.12)

        bt_add = Button(self.janela, text='Adicionar', command=lambda:[self.adicionar(ent_prato.get(),
        ent_valor.get(), self.categoria_prato.get()), self.limpa(ent_prato, ent_valor), self.atualiza_tabela()])
        bt_add.place(relx=0.1, rely=0.6, relwidth=0.18, relheight=0.15)
        bt_atualizar = Button(self.janela, text='Atualizar', command= lambda:[self.atualizar(ent_prato.get(),
        ent_valor.get()), self.limpa(ent_prato, ent_valor), self.atualiza_tabela()])
        bt_atualizar.place(relx=0.4, rely=0.6, relwidth=0.18, relheight=0.15)
        bt_apagar = Button(self.janela, text='Apagar', command=lambda: [self.apagar(ent_prato.get()),
        self.limpa(ent_prato, ent_valor), self.atualiza_tabela()])
        bt_apagar.place(relx=0.7, rely=0.6, relwidth=0.18, relheight=0.15)

    def total_pedido(self, valor):
        self.total = Label(self.root_cardapio, text=f'TOTAL: {valor}$')
        self.total.place(relx=0.7, rely=0.65, relwidth=0.2, relheight=0.1)

    def set_total(self):
        self.tipo_tele()
        self.valor_total = sum(self.carrinho_compras) + self.tipo_tele()
        self.total_pedido(self.valor_total)

    def soma_pratos(self):
        conn = self.conectar()
        c = conn.cursor()
        c.execute('''SELECT valor_prato FROM menu WHERE nome_prato = %s''', (self.prato,))
        preco = c.fetchall()
        for x in preco:
            self.carrinho_compras.append(x[0])

    def acessorios(self):
        self.boy_label = Label(self.root_cardapio, text='Motoboy')
        self.boy_entry = Entry(self.root_cardapio)

        self.data_label = Label(self.root_cardapio, text='Data')
        self.data_label.place(relx=0.4, rely=0.75, relwidth=0.15, relheight=0.1)
            
        self.data_entry = Entry(self.root_cardapio)
        self.data_entry.place(relx=0.4, rely=0.83, relwidth=0.25, relheight=0.05)

        self.tipo = IntVar(self.root_cardapio)
        retirada = Radiobutton(self.root_cardapio, text= 'Retirada', variable= self.tipo, value=1)
        retirada.place(relx=0.05, rely=0.65, relwidth=0.12, relheight=0.08)
        ifood = Radiobutton(self.root_cardapio, text= 'Ifood', variable= self.tipo, value=2)
        ifood.place(relx=0.27, rely=0.65, relwidth=0.1, relheight=0.08)
        particular = Radiobutton(self.root_cardapio, text= 'Tele Wonder', variable= self.tipo, value=3)
        particular.place(relx=0.48, rely=0.65, relwidth=0.15, relheight=0.08)

        bt_fpedido = Image.open('Imagens/pagar.png')
        img_fpedido = ImageTk.PhotoImage(bt_fpedido)
        finalizar = Button(self.root_cardapio, image= img_fpedido, compound=CENTER,
        command=lambda:[self.novo_pedido(self.info_cliente, self.memoria, self.boy_entry.get().title(),
        self.tipo_tele(), self.tipo_pedido, self.data_entry.get()),
        self.carrinho.delete(*self.carrinho.get_children()), self.boy_entry.delete(0, 'end'),
        self.data_entry.delete(0, 'end'), self.total_pedido(0), self.root_cardapio.destroy()])
        finalizar.place(relx=0.8, rely=0.8, relwidth=0.12, relheight=0.1)
        finalizar.imagem = img_fpedido

    def tipo_tele(self):
        try:
            if self.tipo.get() == 1:
                self.boy_entry.delete(0, 'end')
                self.boy_entry.insert('end', 'Wonder')
                self.tipo_pedido = 0
                tele = 0
                self.boy_label.forget()
                self.boy_entry.forget()
                return tele
            elif self.tipo.get() == 2:
                self.tipo_pedido = 1
                tele = 10
                self.boy_label.place(relx=0.1, rely=0.75, relwidth=0.15, relheight=0.1)
                self.boy_entry.place(relx=0.05, rely=0.83, relwidth=0.25, relheight=0.05)
                return tele
            elif self.tipo.get() == 3:
                self.tipo_pedido = 2
                self.boy_label.place(relx=0.1, rely=0.75, relwidth=0.15, relheight=0.1)
                self.boy_entry.place(relx=0.05, rely=0.83, relwidth=0.25, relheight=0.05)
                conn = self.conectar()
                c = conn.cursor()
                c.execute("""SELECT preco FROM bairros WHERE nome_bairro = %s""", (self.end_cliente,))
                valor = c.fetchall()
                print(valor)
                return valor[0][0]
            else:
                print(222)
        except AttributeError:
            messagebox.showerror('Pedido', 'Selecione o tipo de entrega')
            
    def seleciona(self, event):
        for x in self.menu.selection():
            self.prato, self.preco = self.menu.item(x, 'values')
            if self.prato not in self.memoria.keys():
                self.memoria[self.prato] = 1
                self.modelo.set_prato(self.valor.get()), self.inserir(), self.soma_pratos(), 
                self.set_total()
            else:
                self.memoria[self.prato] +=1
                self.modelo.set_prato(self.valor.get()), self.inserir(), self.soma_pratos(), 
                self.set_total()

    def deseleciona(self, event):
        conn = self.conectar()
        c = conn.cursor()
        for x in self.carrinho.selection():
            quant, prato_carrinho= self.carrinho.item(x, 'values')
            print(self.preco, prato_carrinho)
            if self.memoria[prato_carrinho] == 1:
                del self.memoria[prato_carrinho]
                c.execute("""SELECT valor_prato FROM menu WHERE nome_prato = %s""", (prato_carrinho,))
                menos = c.fetchall()
                tira_prato = menos[0][0]
                self.carrinho_compras.append(-tira_prato)
                print(self.carrinho_compras)
                self.inserir()
            else:
                print(prato_carrinho)
                self.memoria[prato_carrinho] -= 1
                print(self.memoria)
                c.execute("""SELECT valor_prato FROM menu WHERE nome_prato = %s""", (prato_carrinho,))
                menos = c.fetchall()
                tira_prato = menos[0][0]
                self.carrinho_compras.append(-tira_prato)
                print(self.carrinho_compras)
                self.inserir()

    def tabela(self):
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",
                background="#D3D3D3",
                foreground="black",
                rowheight=25,
                fieldbackground="#D3D3D3",
                font=('Helvetica', 11))
        style.map('Treeview', background=[('selected', "#347083")])

        tree_scroll = Scrollbar(self.name)
        tree_scroll.place(relx=0.95, rely=0.02, relwidth=0.05, relheight=0.98)

        self.carrinho = ttk.Treeview(self.name, yscrollcommand=tree_scroll.set,
                             selectmode="extended")
        self.carrinho.place(relx=0.01, rely=0.02, relwidth=0.935, relheight=0.98)

        tree_scroll.config(command=self.carrinho.yview)

        self.carrinho['columns'] = ("Quant", "Prato")
        self.carrinho.column("#0", width=0, stretch=NO)
        self.carrinho.column("Quant", anchor=W, width=50)
        self.carrinho.column("Prato", anchor=W, width=250)

        self.carrinho.heading("#0", text="", anchor=W)
        self.carrinho.heading("Prato", text="Prato", anchor=CENTER)
        self.carrinho.heading("Quant", text="Quant", anchor=CENTER)

        self.carrinho.tag_configure('cor1', background="#D7FDF0")
        self.carrinho.tag_configure('cor2', background="#B2FFD6")
        self.carrinho.tag_configure('cor2', background="#B4D6D3")
        self.carrinho.tag_configure('cor2', background="#B8BAC8")

        self.carrinho.bind('<Double-Button-3>', self.deseleciona)

    def select_pratos(self):    
        for x in self.memoria.keys():
            return x

    def inserir(self):
        self.carrinho.delete(*self.carrinho.get_children())
        global contador
        contador = 0
        for p, q in self.memoria.items():
            if contador % 2 == 0:
                self.carrinho.insert(parent='', index='end', text='',
                                values=(q, p), tags=('cor2',))
            else:
                self.carrinho.insert(parent='', index='end', text='',
                                    values=(q, p), tags=('cor1',))
            contador +=1
            self.set_total()
    #Menu
    def menu_geral(self):
        style = ttk.Style()
        style.theme_use('default')
        style.configure("tema_cardapio",
                background="white",
                foreground="black",
                rowheight=25,
                fieldbackground="#D3D3D3",
                font=('Helvetica', 11))
        style.map('tema_cardapio', background=[('selected', "#347083")])

        frame_menu = ttk.Notebook(self.root_cardapio)
        frame_menu.place(relx=0.01, rely=0.02, relwidth=0.65, relheight=0.6)
        aba_menu = ttk.Frame(frame_menu)
        aba_menu.place(relx=0.01, rely=0.02, relwidth=0.65, relheight=0.6)
        self.aba_poke = ttk.Frame(frame_menu)
        self.aba_poke.place(relx=0.01, rely=0.02, relwidth=0.65, relheight=0.6)
        frame_menu.add(aba_menu, text='Menu')
        frame_menu.add(self.aba_poke, text='Monde seu Poke')

        self.valor = StringVar(frame_menu)

        tree_scroll = Scrollbar(aba_menu)
        tree_scroll.place(relx=0.971, rely=0.0, relwidth=0.03, relheight=1)

        self.menu = ttk.Treeview(aba_menu, yscrollcommand=tree_scroll.set, selectmode="browse")
        self.menu.place(relx=0.0, rely=0.0, relwidth=0.972, relheight=1)

        tree_scroll.config(command=self.menu.yview)

        self.menu['columns'] = ("Prato", "Valor")
        self.menu.column("#0", width=0, stretch=NO)
        self.menu.column("Prato", anchor=W, width=250)
        self.menu.column("Valor", anchor=CENTER, width=50)

        self.menu.heading("#0", text="", anchor=W)
        self.menu.heading("Prato", text="Prato", anchor=CENTER)
        self.menu.heading("Valor", text="Valor", anchor=CENTER)

        self.menu.tag_configure('cor1', background="#91C4F2")
        self.menu.tag_configure('cor2', background="#8CA0D7")
        self.menu.tag_configure('cor3', background="#9D79BC")
        self.menu.tag_configure('cor4', background="#A14DA0")
        self.menu.tag_configure('cor5', background="#7E1F86")

        conn = self.conectar()
        c = conn.cursor()
        c.execute("""SELECT nome_prato, valor_prato, categoria FROM menu ORDER BY nome_prato""")
        global count
        count = 0
        self.menu.insert('', 'end', 'Snack', tags=('cor3',), values=('⮯Snacks'))
        self.menu.insert('', 'end', 'Bowl', tags=('cor4',), values='⮯Bowls')
        self.menu.insert('', 'end', 'Salada', tags=('cor3',), values='⮯Saladas')
        self.menu.insert('', 'end', 'Brunch', tags=('cor4',), values='⮯Brunch')            
        self.menu.insert('', 'end', 'Pizza', tags=('cor3',), values='⮯Pizzas')
        self.menu.insert('', 'end', 'Burger', tags=('cor4',), values='⮯Burgers')
        self.menu.insert('', 'end', 'Poke', tags=('cor3',), values='⮯Pokes')
        self.menu.insert('', 'end', 'Doce', tags=('cor4',), values='⮯Doces')
        self.menu.insert('', 'end', 'Cafe', tags=('cor3',), values='⮯Cafés')
        self.menu.insert('', 'end', 'Suco', tags=('cor4',), values='⮯Sucos')
        self.menu.insert('', 'end', 'Bebida', tags=('cor3',), values='⮯Bebidas')

        for prato, valor, categoria in c.fetchall():
            if categoria == 'Snack':
                if count % 2 == 0:
                        self.menu.insert(parent='Snack', index='end', text='',
                                values=(prato, (valor,'$')), tags=('cor2',))
                else:
                    self.menu.insert(parent='Snack', index='end', text='',
                                values=(prato, (valor,'$')), tags=('cor1',))
                count += 1
            elif categoria == 'Bowl':
                if count % 2 == 0:
                    self.menu.insert(parent='Bowl', index='end', text='',
                                values=(prato, (valor,'$')), tags=('cor2',))
                else:
                    self.menu.insert(parent='Bowl', index='end', text='',
                                values=(prato, (valor,'$')), tags=('cor1',))
                count += 1
            elif categoria == 'Salada':
                if count % 2 == 0:
                    self.menu.insert(parent='Salada', index='end', text='',
                                values=(prato, (valor,'$')), tags=('cor2',))
                else:
                    self.menu.insert(parent='Salada', index='end', text='',
                                values=(prato, (valor,'$')), tags=('cor1',))
                count += 1
            elif categoria == 'Brunch':
                if count % 2 == 0:
                    self.menu.insert(parent='Brunch', index='end', text='',
                                values=(prato, (valor,'$')), tags=('cor2',))
                else:
                    self.menu.insert(parent='Brunch', index='end', text='',
                                values=(prato, (valor,'$')), tags=('cor1',))
                count += 1
            elif categoria == 'Pizza':
                if count % 2 == 0:
                    self.menu.insert(parent='Pizza', index='end', text='',
                                values=(prato, (valor,'$')), tags=('cor2',))
                else:
                    self.menu.insert(parent='Pizza', index='end', text='',
                                values=(prato, (valor,'$')), tags=('cor1',))
                count += 1
            elif categoria == 'Burger':
                if count % 2 == 0:
                    self.menu.insert(parent='Burger', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor2',))
                else:
                    self.menu.insert(parent='Burger', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor1',))
                count += 1
            elif categoria == 'Poke':
                if count % 2 == 0:
                    self.menu.insert(parent='Poke', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor2',))
                else:
                    self.menu.insert(parent='Poke', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor1',))
                count += 1
            elif categoria == 'Doce':
                if count % 2 == 0:
                    self.menu.insert(parent='Doce', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor2',))
                else:
                    self.menu.insert(parent='Doce', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor1',))
                count += 1
            elif categoria == 'Cafe':
                if count % 2 == 0:
                    self.menu.insert(parent='Cafe', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor2',))
                else:
                    self.menu.insert(parent='Cafe', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor1',))
                count += 1
            elif categoria == 'Suco':
                if count % 2 == 0:
                    self.menu.insert(parent='Suco', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor2',))
                else:
                    self.menu.insert(parent='Suco', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor1',))
                count += 1
            elif categoria == 'Bebida':
                if count % 2 == 0:
                        self.menu.insert(parent='Bebida', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor2',))
                else:
                    self.menu.insert(parent='Bebida', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor1',))
                count += 1

        self.menu.bind('<Button-3>', self.seleciona)

    def monte_poke(self):
        self.pag1 = Frame(self.aba_poke)
        self.pag1.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)
        letra = font.Font(family='Arial', size= 20, weight='bold')
        letra2 = font.Font(family='Arial', size=12, weight='bold', slant='italic')
        letra3 = font.Font(family='Arial', size=10, weight='bold')

        base = Label(self.pag1, text='1.BASE')
        base.configure(font=letra)
        base.place(relx=0.02, rely=0.03, relwidth=0.2, relheight=0.1)
        escolha_base = Label(self.pag1, text='Escolha 1', foreground='white')
        escolha_base.configure(font=letra2)
        escolha_base.place(relx=0.02, rely=0.13, relwidth=0.2, relheight=0.1)

        self.extra_poke = []
        self.escolha_base = []
        self.proteina = []
        self.base_1 = IntVar(self.aba_poke) 
        self.base_2 = IntVar(self.aba_poke) 
        self.base_3 = IntVar(self.aba_poke) 
        self.base_4 = IntVar(self.aba_poke) 
        self.base_5 = IntVar(self.aba_poke)

        self.op_base_1 = Checkbutton(self.pag1, text='Arroz de sushi', variable= self.base_1, 
        anchor='w')
        self.op_base_1.place(relx=0.02, rely=0.25, relwidth=0.25, relheight=0.1)
        self.op_base_2 = Checkbutton(self.pag1, text='Arroz negro(+ R$4)', anchor='w',
        variable= self.base_2)
        self.op_base_2.place(relx=0.02, rely=0.35, relwidth=0.3, relheight=0.1)
        self.op_base_3 = Checkbutton(self.pag1, text='Quinoa(+R$4)', anchor='w',
        variable= self.base_3)
        self.op_base_3.place(relx=0.02, rely=0.45, relwidth=0.25, relheight=0.1)
        self.op_base_4 = Checkbutton(self.pag1, text='Espaguete de abobrinha', anchor='w',
        variable= self.base_4)
        self.op_base_4.place(relx=0.02, rely=0.55, relwidth=0.4, relheight=0.1)
        self.op_base_5 = Checkbutton(self.pag1, text='Espaguete de palmito de\n pupunha ao pesto(+ R$5)',
        anchor='w', variable= self.base_5)
        self.op_base_5.place(relx=0.02, rely=0.65, relwidth=0.4, relheight=0.25)

        proteina = Label(self.pag1, text='1.PROTEÍNAS 120g', anchor='w')
        proteina.place(relx=0.45, rely=0.02, relwidth=0.55, relheight=0.15)
        proteina.configure(font=letra)
        escolha_prot = Label(self.pag1, text='Escolha até 2 (60g de cada)', foreground='white',
        anchor='w')
        escolha_prot.place(relx=0.45, rely=0.15, relwidth=0.5, relheight=0.08)
        escolha_prot.configure(font=letra2)
        info_prot = Label(self.pag1, text='-Sera considerada a proteína de maior valor-',
        anchor='w')
        info_prot.place(relx=0.45, rely=0.23, relwidth=0.55, relheight=0.08)
        info_prot.configure(font=letra3)

        self.prot1 = IntVar(self.pag1)
        self.prot2 = IntVar(self.pag1)
        self.prot3 = IntVar(self.pag1)
        self.prot4 = IntVar(self.pag1)
        op_prot1 = Checkbutton(self.pag1, text='Salmão', anchor='w', variable=self.prot1)
        op_prot1.place(relx=0.45, rely=0.35, relwidth=0.25, relheight=0.1)
        op_prot2 = Checkbutton(self.pag1, text='Atum', anchor='w', variable=self.prot2)
        op_prot2.place(relx=0.45, rely=0.45, relwidth=0.3, relheight=0.1)
        op_prot3 = Checkbutton(self.pag1, text='Camarão', anchor='w', variable=self.prot3)
        op_prot3.place(relx=0.45, rely=0.55, relwidth=0.25, relheight=0.1)
        op_prot4 = Checkbutton(self.pag1, text='Shitake', anchor='w', variable=self.prot4)
        op_prot4.place(relx=0.45, rely=0.65, relwidth=0.25, relheight=0.1)

        def erros():
            if len(self.escolha_base) > 1:
                messagebox.showerror('ERRO', 'Escolha apenas uma opção para base')
                self.escolha_base.clear()
                self.proteina.clear()
            elif len(self.escolha_base) == 0:
                messagebox.showerror('ERRO', 'Escolha uma opção para base')
                self.proteina.clear()
                self.escolha_base.clear()
            elif len(self.proteina) > 2:
                messagebox.showerror('ERRO', 'Escolha apenas 2 opção de proteína')
                self.proteina.clear()
                self.escolha_base.clear()
            elif len(self.proteina) == 0:
                messagebox.showerror('ERRO', 'Escolha no mínimo uma opção de proteína')
                self.proteina.clear()
                self.escolha_base.clear()
            if len(self.escolha_base) == 1 and len(self.proteina) <= 2 and len(self.proteina) > 0 and len(self.proteina) < 3:
                self.poke_2()
        def verificacao():
            try:
                if self.base_1.get() == 1:
                    self.escolha_base.append(1)
                if self.base_2.get() == 1:
                    self.escolha_base.append(2)
                    self.extra_poke.append(4)
                if self.base_3.get() == 1:
                    self.escolha_base.append(3)
                    self.extra_poke.append(4)
                if self.base_4.get() == 1:
                    self.escolha_base.append(4)
                if self.base_5.get() == 1:
                    self.escolha_base.append(5)
                    self.extra_poke.append(5)
                if self.prot1.get() == 1:
                    self.proteina.append(1)
                    self.extra_poke.append(54)
                if self.prot2.get() == 1:
                    self.proteina.append(2)
                    self.extra_poke.append(54)
                if self.prot3.get() == 1:
                    self.proteina.append(3)
                    self.extra_poke(60)
                if self.prot4.get() == 1:
                    self.proteina.append(4)
                    self.extra_poke.append(50)
                erros()
                self.proteina.clear()
                self.escolha_base.clear()
            except AttributeError as error:
                messagebox.showwarning('ERRO', error)

        pag2 = Button(self.pag1, text='>>>>', command=lambda:[verificacao()])
        pag2.place(relx=0.8, rely=0.85, relwidth=0.1, relheight=0.1)
    
    def poke_2(self):
        self.pag1.forget()
        self.pag2 = Frame(self.aba_poke)
        letra = font.Font(family='Arial', size= 20, weight='bold')
        letra2 = font.Font(family='Arial', size=12, weight='bold', slant='italic')
        self.pag2.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)
        self.make_it = []
        self.make1 = IntVar(self.pag2)
        self.make2 = IntVar(self.pag2)
        self.make3 = IntVar(self.pag2)
        self.make4 = IntVar(self.pag2)
        self.make5 = IntVar(self.pag2)
        self.make6 = IntVar(self.pag2)
        self.make7 = IntVar(self.pag2)
        self.make8 = IntVar(self.pag2)
        self.make9 = IntVar(self.pag2)
        self.make10 = IntVar(self.pag2)
        self.make11= IntVar(self.pag2)
        self.make12 = IntVar(self.pag2)
        def verifica(tamanho):
            if tamanho > 4:
                messagebox.showerror('MAKE IT incompleto', 'Escolha no máximo 4 opções do MAKE IT')
                self.make_it.clear()
            elif tamanho == 0:
                messagebox.showerror('MAKE IT incompleto', 'Escolha no minímo 1 opção do MAKE IT')
                self.make_it.clear()
            elif tamanho < 5 or tamanho >= 1:
                self.make_it.clear()
                self.poke_3()
        def check_make():
            if self.make1.get() == 1:
                self.make_it.append(1)
            if self.make2.get() == 1:
                self.make_it.append(2)
            if self.make3.get() == 1:
                self.make_it.append(3)
            if self.make4.get() == 1:
                self.make_it.append(4)
            if self.make5.get() == 1:
                self.make_it.append(5)
            if self.make6.get() == 1:
                self.make_it.append(6)
            if self.make7.get() == 1:
                self.make_it.append(7)
            if self.make8.get() == 1:
                self.make_it.append(8)
            if self.make9.get() == 1:
                self.make_it.append(9)
            if self.make10.get() == 1:
                self.make_it.append(10)
            if self.make11.get() == 1:
                self.make_it.append(11)
            if self.make12.get() == 1:
                self.make_it.append(12)
            verifica(len(self.make_it))

        make = Label(self.pag2, text='3.MAKE IT', anchor='w')
        make.configure(font=letra)
        make.place(relx=0.02, rely=0.03, relwidth=0.25, relheight=0.1)
        escolha_make = Label(self.pag2, text='Escolha até 4', foreground='white', anchor='w')
        escolha_make.configure(font=letra2)
        escolha_make.place(relx=0.02, rely=0.13, relwidth=0.2, relheight=0.1)

        op_make1 = Checkbutton(self.pag2, text='Sunomono', variable= self.make1 ,anchor='w')
        op_make1.place(relx=0.45, rely=0.25, relwidth=0.25, relheight=0.1)
        op_make2 = Checkbutton(self.pag2, text='Ceviche de manga', variable= self.make2 ,anchor='w',)
        op_make2.place(relx=0.05, rely=0.35, relwidth=0.3, relheight=0.1)
        op_make3 = Checkbutton(self.pag2, text='Abacaxi', variable= self.make3 ,anchor='w',)
        op_make3.place(relx=0.05, rely=0.45, relwidth=0.25, relheight=0.1)
        op_make4 = Checkbutton(self.pag2, text='Tomate confit', variable= self.make4,anchor='w',)
        op_make4.place(relx=0.05, rely=0.55, relwidth=0.25, relheight=0.1)
        op_make5 = Checkbutton(self.pag2, text='Cenoura salteada', variable= self.make5 ,anchor='w',)
        op_make5.place(relx=0.05, rely=0.65, relwidth=0.3, relheight=0.1)
        op_make6 = Checkbutton(self.pag2, text='Cebola roxa caramelizada', variable= self.make6 ,anchor='w',)
        op_make6.place(relx=0.05, rely=0.75, relwidth=0.4, relheight=0.1)
        op_make7 = Checkbutton(self.pag2, text='Moranga assada', variable= self.make7 ,anchor='w',)
        op_make7.place(relx=0.05, rely=0.25, relwidth=0.3, relheight=0.1)
        op_make8 = Checkbutton(self.pag2, text='Damasco', variable= self.make8 ,anchor='w',)
        op_make8.place(relx=0.45, rely=0.35, relwidth=0.25, relheight=0.1)
        op_make9 = Checkbutton(self.pag2, text='Tofu', variable= self.make9 ,anchor='w',)
        op_make9.place(relx=0.45, rely=0.45, relwidth=0.25, relheight=0.1)
        op_make10 = Checkbutton(self.pag2, text='Alga nori', variable= self.make10 ,anchor='w')
        op_make10.place(relx=0.45, rely=0.55, relwidth=0.3, relheight=0.1)
        op_make11 = Checkbutton(self.pag2, text='Edaname', variable= self.make11 ,anchor='w')
        op_make11.place(relx=0.45, rely=0.65, relwidth=0.25, relheight=0.1)
        op_make12 = Checkbutton(self.pag2, text='Manga em cubos', variable= self.make12 ,anchor='w')
        op_make12.place(relx=0.45, rely=0.75, relwidth=0.25, relheight=0.1)

        pag2 = Button(self.pag2, text='>>>>', command=lambda:[check_make()])
        pag2.place(relx=0.8, rely=0.85, relwidth=0.1, relheight=0.1)

        test2 = Button(self.pag2, text='Ver', command=lambda:[check_make()])
        test2.place(relx=0.5, rely=0.85, relwidth=0.1, relheight=0.1)

    def poke_3(self):
        self.pag2.forget()
        self.pag3 = Frame(self.aba_poke)
        letra = font.Font(family='Arial', size= 20, weight='bold')
        letra2 = font.Font(family='Arial', size=12, weight='bold', slant='italic')
        self.pag3.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)
        crunch_it = []
        self.crunch1 = IntVar(self.pag3)
        self.crunch2 = IntVar(self.pag3)
        self.crunch3 = IntVar(self.pag3)

        crunch = Label(self.pag3, text='3.CRUNCH IT', anchor='w')
        crunch.configure(font=letra)
        crunch.place(relx=0.02, rely=0.03, relwidth=0.35, relheight=0.1)
        escolha_crunch = Label(self.pag3, text='Escolha 1', foreground='white', anchor='w')
        escolha_crunch.configure(font=letra2)
        escolha_crunch.place(relx=0.02, rely=0.13, relwidth=0.22, relheight=0.1)

        op_crunch1 = Checkbutton(self.pag3, text='Chips de banana', anchor='w',
        variable= self.crunch1)
        op_crunch1.place(relx=0.02, rely=0.25, relwidth=0.28, relheight=0.1)
        op_crunch2 = Checkbutton(self.pag3, text='Chips de batata doce', anchor='w',
        variable= self.crunch2)
        op_crunch2.place(relx=0.02, rely=0.35, relwidth=0.45, relheight=0.1)
        op_crunch3 = Checkbutton(self.pag3, text='Kale', anchor='w',
        variable= self.crunch3)
        op_crunch3.place(relx=0.02, rely=0.45, relwidth=0.25, relheight=0.1)

        top_master = Frame(self.pag3)
        top_master.place(relx=0.39, rely=0.0, relwidth=0.6, relheight=1)
        top = Label(top_master, text='4.TOP IT', anchor='w')
        top.configure(font=letra)
        top.place(relx=0.45, rely=0.03, relwidth=0.4, relheight=0.1)
        escolha_top = Label(top_master, text='Escolha 1', foreground='white', anchor='w')
        escolha_top.configure(font=letra2)
        escolha_top.place(relx=0.45, rely=0.13, relwidth=0.4, relheight=0.1)

        top_it = []
        top1 = IntVar(top)
        top2 = IntVar(top)
        top3 = IntVar(top)
        top4 = IntVar(top)
        top5 = IntVar(top)
        top6 = IntVar(top)
        top7 = IntVar(top)
        top8 = IntVar(top)

        op_top1 = Checkbutton(top_master, text='Castanhas', anchor='w', variable= top1)
        op_top1.place(relx=0.6, rely=0.45, relwidth=0.35, relheight=0.1)
        op_top2 = Checkbutton(top_master, text='Nozes', anchor='w', variable= top2)
        op_top2.place(relx=0.6, rely=0.25, relwidth=0.35, relheight=0.1)
        op_top3 = Checkbutton(top_master, text='Pistache', anchor='w', variable= top3)
        op_top3.place(relx=0.1, rely=0.35, relwidth=0.35, relheight=0.1)
        op_top4 = Checkbutton(top_master, text='Amendôas', anchor='w', variable= top4)
        op_top4.place(relx=0.6, rely=0.35, relwidth=0.35, relheight=0.1)
        op_top5 = Checkbutton(top_master, text='Gergerlim negro', anchor='w', variable= top5)
        op_top5.place(relx=0.1, rely=0.45, relwidth=0.5, relheight=0.1)
        op_top6 = Checkbutton(top_master, text='Lascas de coco', anchor='w', variable= top6)
        op_top6.place(relx=0.1, rely=0.25, relwidth=0.45, relheight=0.1)
        op_top7 = Checkbutton(top_master, text='Semente de abóbora', anchor='w', variable= top7)
        op_top7.place(relx=0.1, rely=0.55, relwidth=0.55, relheight=0.1)
        op_top8 = Checkbutton(top_master, text='Linhaça dourada', anchor='w', variable= top8)
        op_top8.place(relx=0.1, rely=0.65, relwidth=0.5, relheight=0.1)

        def verifica_pg3():
            try:
                if self.crunch1.get() == 1:
                    crunch_it.append(1)
                if self.crunch2.get() == 1:
                    crunch_it.append(2)
                if self.crunch3.get() == 1:
                    crunch_it.append(3)
                elif len(crunch_it) > 1:
                    messagebox.showerror('ERRO', 'Selecione apenas 1 opção de crunch it')
                    crunch_it.clear()
                    top_it.clear()
                elif len(crunch_it) == 0:
                    messagebox.showerror('ERRO', 'Selecione no minímo 1 opção de crunch it')
                    crunch_it.clear()
                    top_it.clear()
                if top1.get() == 1:
                    top_it.append(1)
                if top2.get() == 1:
                    top_it.append(2)
                if top3.get() == 1:
                    top_it.append(3)
                if top4.get() == 1:
                    top_it.append(4)
                if top5.get() == 1:
                    top_it.append(5)
                if top6.get() == 1:
                    top_it.append(6)
                if top7.get() == 1:
                    top_it.append(7)
                if top8.get() == 1:
                    top_it.append(8)
                elif len(top_it) > 1:
                    messagebox.showerror('ERRO', 'Selecione apenas 1 opção de top it')
                    top_it.clear()
                    crunch_it.clear()
                elif len(top_it) == 0:
                    messagebox.showerror('ERRO', 'Selecione 1 opção de top it')
                    top_it.clear()
                    crunch_it.clear()
                top_it.clear()
                crunch_it.clear()
                self.poke_4()
            except error:
                messagebox.showerror('ERRO', "Erro inesperado, contate o programador")

        pag3 = Button(top_master, text='>>>>', command=lambda:[verifica_pg3()])
        pag3.place(relx=0.8, rely=0.8, relwidth=0.3, relheight=0.1)

    def poke_4(self):
        self.pag3.forget()
        self.pag4 = Frame(self.aba_poke)
        letra = font.Font(family='Arial', size= 20, weight='bold')
        letra2 = font.Font(family='Arial', size=12, weight='bold', slant='italic')

        self.pag4.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)
        self.finish_it = IntVar(self.pag4)

        finish = Label(self.pag4, text='4.FINISH IT', anchor='w')
        finish.configure(font=letra)
        finish.place(relx=0.05, rely=0.03, relwidth=0.3, relheight=0.1)
        escolha_finish = Label(self.pag4, text='Escolha 1', foreground='white', anchor='w')
        escolha_finish.configure(font=letra2)
        escolha_finish.place(relx=0.05, rely=0.13, relwidth=0.2, relheight=0.1)

        finish_it = []
        finish1 = IntVar(self.pag4)
        finish2 = IntVar(self.pag4)
        finish3 = IntVar(self.pag4)
        finish4 = IntVar(self.pag4)
        finish5 = IntVar(self.pag4)
        finish6 = IntVar(self.pag4)
        finish7 = IntVar(self.pag4)
        finish8 = IntVar(self.pag4)
        finish9 = IntVar(self.pag4)

        op_finish1 = Checkbutton(self.pag4, text='Shoyo clássico', anchor='w',
        variable= finish1)
        op_finish1.place(relx=0.05, rely=0.25, relwidth=0.25, relheight=0.1)
        op_finish2 = Checkbutton(self.pag4, text='Wasabi', anchor='w',
        variable= finish2)
        op_finish2.place(relx=0.05, rely=0.35, relwidth=0.3, relheight=0.1)
        op_finish3 = Checkbutton(self.pag4, text='Ponzu', anchor='w',
        variable= finish3)
        op_finish3.place(relx=0.05, rely=0.45, relwidth=0.25, relheight=0.1)
        op_finish4 = Checkbutton(self.pag4, text='Cream cheese', anchor='w',
        variable= finish4)
        op_finish4.place(relx=0.05, rely=0.55, relwidth=0.25, relheight=0.1)
        op_finish5 = Checkbutton(self.pag4, text='Tarê', anchor='w',
        variable= finish5)
        op_finish5.place(relx=0.05, rely=0.65, relwidth=0.3, relheight=0.1)
        op_finish6 = Checkbutton(self.pag4, text='Tarê de laranja', anchor='w',
        variable= finish6)
        op_finish6.place(relx=0.45, rely=0.25, relwidth=0.25, relheight=0.1)
        op_finish7 = Checkbutton(self.pag4, text='Mel com gengibre', anchor='w',
        variable= finish7)
        op_finish7.place(relx=0.45, rely=0.35, relwidth=0.32, relheight=0.1)
        op_finish8 = Checkbutton(self.pag4, text='Molho de pimenta com srirancha', anchor='w',
        variable= finish8)
        op_finish8.place(relx=0.45, rely=0.45, relwidth=0.5, relheight=0.1)
        op_finish9 = Checkbutton(self.pag4, text='Soyo de coco(+ R$3)', anchor='w',
        variable= finish9)
        op_finish9.place(relx=0.45, rely=0.55, relwidth=0.4, relheight=0.1)

        def verifica_pag4():
            try:
                if finish1.get() == 1:
                    finish_it.append(1)
                if finish2.get() == 1:
                    finish_it.append(2)
                if finish3.get() == 1:
                    finish_it.append(3)
                if finish4.get() == 1:
                    finish_it.append(4)
                if finish5.get() == 1:
                    finish_it.append(5)
                if finish6.get() == 1:
                    finish_it.append(6)
                if finish7.get() == 1:
                    finish_it.append(7)
                if finish8.get() == 1:
                    finish_it.append(8)
                if finish9.get() == 1:
                    finish_it.append(9)
                    self.extra_poke.append(3)
                elif len(finish_it) > 1:
                    messagebox.showerror('ERRO', "Selecione apenas 1 opção de finish it")
                    finish_it.clear()
                elif len(finish_it) == 0:
                    messagebox.showerror('ERRO', 'Selecione no minímo 1 opção de finish it')
                    finish_it.clear()
                finish_it.clear()
            except error:
                messagebox.showerror('ERRO', "Erro inesperado, contate o programador")

        def add_poke():
            self.memoria.items()
            self.carrinho.delete(*self.carrinho.get_children())
            global contador
            contador = 0
            if 'Monte seu poke' not in self.memoria.keys():
                self.memoria['Monte seu poke'] = 1
            else:
                self.memoria['Monte seu poke'] +=1
            for p, q in self.memoria.items():
                if contador % 2 == 0:
                    self.carrinho.insert(parent='', index='end', text='',
                                    values=(q, p), tags=('cor2',))
                else:
                    self.carrinho.insert(parent='', index='end', text='',
                                        values=(q, p), tags=('cor1',))
                contador +=1
            self.carrinho_compras.append(sum(self.extra_poke))
            self.set_total()

            conn = self.conectar()
            c = conn.cursor()
            c.execute("""UPDATE menu SET valor_prato = %s WHERE nome_prato = %s""",
            (sum(self.extra_poke), 'Monte seu poke'))

        pag4 = Button(self.pag4, text='ADD', command=lambda:[verifica_pag4(), add_poke()])
        pag4.place(relx=0.8, rely=0.85, relwidth=0.1, relheight=0.1)

    def atualiza_tabela(self):
            self.menu.delete(*self.menu.get_children())
            conn = self.conectar() 
            c = conn.cursor()
            c.execute("""SELECT * FROM menu ORDER BY nome_prato""")
            global count
            count = 0
            self.menu.insert('', 'end', 'Snack', text='Snack', tags=('cor3',), values='>Snacks')
            self.menu.insert('', 'end', 'Bowl', text='Bowls', tags=('cor4',), values='>Bowls')
            self.menu.insert('', 'end', 'Salada', text='Saladas', tags=('cor3',), values='>Saladas')
            self.menu.insert('', 'end', 'Brunch', text='Brunch', tags=('cor4',), values='>Brunch')            
            self.menu.insert('', 'end', 'Pizza', text='Pizzas', tags=('cor3',), values='>Pizzas')
            self.menu.insert('', 'end', 'Burger', text='Burgers', tags=('cor4',), values='>Burgers')
            self.menu.insert('', 'end', 'Poke', text='Poke', tags=('cor3',), values='>Pokes')
            self.menu.insert('', 'end', 'Doce', text='Doces', tags=('cor4',), values='>Doces')
            self.menu.insert('', 'end', 'Cafe', text='Cafe', tags=('cor3',), values='>Cafés')
            self.menu.insert('', 'end', 'Suco', text='Suco', tags=('cor4',), values='>Sucos')
            self.menu.insert('', 'end', 'Bebida', text='Bebida', tags=('cor3',), values='>Bebidas')

            for idd, prato, valor, categoria in c.fetchall():
                if categoria == 'Snack':
                    self.indice = '0'
                    if count == 0:
                        self.menu.insert(parent='Snack', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor2',))
                        count += 1
                    else:
                        self.menu.insert(parent='Snack', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor1',))
                        count -= 1
                if categoria == 'Bowl':
                    if count % 2 == 0:
                        self.menu.insert(parent='Bowl', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor2',))
                    else:
                        self.menu.insert(parent='Bowl', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor1',))
                    count += 1
                elif categoria == 'Salada':
                    if count % 2 == 0:
                        self.menu.insert(parent='Salada', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor2',))
                    else:
                        self.menu.insert(parent='Salada', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor1',))
                    count += 1
                elif categoria == 'Brunch':
                    if count % 2 == 0:
                        self.menu.insert(parent='Brunch', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor2',))
                    else:
                        self.menu.insert(parent='Brunch', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor1',))
                    count += 1
                elif categoria == 'Pizza':
                    if count % 2 == 0:
                        self.menu.insert(parent='Pizza', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor2',))
                    else:
                        self.menu.insert(parent='Pizza', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor1',))
                    count += 1
                elif categoria == 'Burger':
                    if count % 2 == 0:
                        self.menu.insert(parent='Burger', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor2',))
                    else:
                        self.menu.insert(parent='Burger', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor1',))
                    count += 1
                elif categoria == 'Poke':
                    if count % 2 == 0:
                        self.menu.insert(parent='Poke', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor2',))
                    else:
                        self.menu.insert(parent='Poke', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor1',))
                    count += 1
                elif categoria == 'Doce':
                    if count % 2 == 0:
                        self.menu.insert(parent='Doce', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor2',))
                    else:
                        self.menu.insert(parent='Doce', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor1',))
                    count += 1
                elif categoria == 'Cafe':
                    if count % 2 == 0:
                        self.menu.insert(parent='Cafe', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor2',))
                    else:
                        self.menu.insert(parent='Cafe', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor1',))
                    count += 1
                elif categoria == 'Suco':
                    if count % 2 == 0:
                        self.menu.insert(parent='Suco', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor2',))
                    else:
                        self.menu.insert(parent='Suco', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor1',))
                    count += 1
                elif categoria == 'Bebida':
                    if count % 2 == 0:
                        self.menu.insert(parent='Bebida', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor2',))
                    else:
                        self.menu.insert(parent='Bebida', index='end', text='',
                                    values=(prato, (valor,'$')), tags=('cor1',))
                    count += 1

    def verificacao(self, info_cliente):
        try:
            conn = self.conectar()
            c = conn.cursor()
            c.execute("SELECT nome_cliente FROM clientes WHERE nome_cliente = %s", (info_cliente,))
            resposta = c.fetchall()
            if resposta[0][0]:
                return True
        except Exception as erro:
            print(erro)


#c = tela_cliente()
#c