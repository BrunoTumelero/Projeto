from os import error
from tkinter import *
from tkinter import ttk
from tkinter import font
from PIL import Image, ImageTk
from Cliente import *
from cardapio_v2 import Cardapio, Modelo_prato
from pedido import *
from bairrosv2 import Local
from configurar_cardapio import conf_cardapio
import json

class tela_cliente(Cliente):
  def __init__(self, root, fundo, botoes_inicio, escquece1, esquece2):
    super().__init__()
    self.root = root
    self.root_clientes = root
    self.fundo = fundo
    self.botoes_inicio = botoes_inicio
    self.esq1 = escquece1
    self.esq2 = esquece2
    self.root_clientes.title('Cliente')
    self.root_clientes.configure(background='snow')
    self.tabela_geral()
    self.clientes_geral()
    self.acessorios()
    self.botoes()
    self.menu()

    self.root_clientes.mainloop()

  def conectar_cliente(self):
    return super().conectar_cliente()

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
    
    conn = self.conectar_cliente()
    c = conn.cursor()
    nome_pesquisa = f'%{nome}%'.title()
    c.execute("""SELECT * FROM clientes
            WHERE nome_cliente LIKE %s""", (nome_pesquisa,))

    global contador_cliente
    contador_cliente = 0

    for num, nome, end in c.fetchall():
        if contador_cliente % 2 == 0:
            lista.insert(parent='', index='0', text='',
                           values=(num, nome, end),
                           tags=('cor1',))

        else:
          lista.insert(parent='', index='0', text='',
                                 values=(num, nome, end),
                                 tags=('cor2',))
        contador_cliente += 1
        conn.close()
  
  def menu(self):
    # Add Menu
    menu_opcoes = Menu(self.root_clientes)
    self.root_clientes.config(menu=menu_opcoes)

    menu_opcoes.add_command(label='Inicio', command=lambda:[self.tree_frame.destroy(),
    menu_opcoes.destroy(), self.data_frame.place_forget(), self.frame_botao.place_forget(),
    self.fundo, self.botoes_inicio])
    # Configurar menu
    menu_cliente = Menu(menu_opcoes, tearoff=0)
    menu_opcoes.add_cascade(label="Opções", menu=menu_cliente)
    # opcoes do menu
    menu_cliente.add_command(label='Clientes', command=lambda:[self.clientes_geral()])
    menu_cliente.add_command(label='Clientes com pedidos', command=lambda:[self.tabela()])

  def tabela_geral(self):
    estilo = ttk.Style()
    estilo.theme_use('default')
    estilo.configure("geral.Treeview", background="#D3D3D3", foreground="black",
                    rowheight=25, fieldbackground="#D3D3D3", font='Helvetica')
    estilo.map('geral.treeview', background=[('selected', "#347083")])
    self.tree_frame = Frame(self.root_clientes)
    self.tree_frame.place(relx=0.02, rely=0.05, relwidth=0.95, relheight=0.5)
    self.tree_frame.configure(background='snow')
    self.barra = Scrollbar(self.tree_frame)
    self.barra.place(relx=0.97, rely=0.0, relwidth=0.02, relheight=1)
    self.barra.configure(background='snow')

    self.tabela_clientes = ttk.Treeview(self.tree_frame, style= 'geral.Treeview', 
                                    yscrollcommand=self.barra.set, selectmode="extended")
    self.tabela_clientes.place(relx=0.02, rely=0.0, relwidth=0.95, relheight=1)

    self.barra.config(command=self.tabela_clientes.yview)

  def clientes_geral(self):
    try:
      self.tabela_clientes.delete(*self.tabela_clientes.get_children())
    except TypeError as er:
      print(er)
    finally:
      self.tabela_clientes['columns'] = ("Id", "Nome", "Endereço")
      self.tabela_clientes.column("#0", width=0, stretch=NO)
      self.tabela_clientes.column("Id", anchor=W, width=20)
      self.tabela_clientes.column("Nome", anchor=CENTER, width=450)
      self.tabela_clientes.column("Endereço", anchor=CENTER, width=200)

      self.tabela_clientes.heading("#0", text="", anchor=W)
      self.tabela_clientes.heading("Id", text="Id", anchor=CENTER)
      self.tabela_clientes.heading("Nome", text="Nome", anchor=CENTER)
      self.tabela_clientes.heading("Endereço", text="Endereço", anchor=CENTER)

      self.tabela_clientes.tag_configure('cor1', background="white")
      self.tabela_clientes.tag_configure('cor2', background="lightblue")

      conn = self.conectar_cliente()

      c = conn.cursor()
      c.execute("""SELECT * FROM clientes""")

      global contador_cliente
      contador_cliente = 0

      for idd, nome, loc in c.fetchall():
          if contador_cliente % 2 == 0:
              self.tabela_clientes.insert(parent='', index='end', text='',
              values=(idd, nome, loc), tags=('cor2',))
          else:
              self.tabela_clientes.insert(parent='', index='end', text='',
              values=(idd, nome, loc), tags=('cor1',))
          contador_cliente += 1
      conn.close()
      self.tabela_clientes.bind('<Double-Button-1>', self.seleciona_cliente)

  def tabela(self):
    self.tabela_clientes.delete(*self.tabela_clientes.get_children())
    self.tabela_clientes['columns'] = ("Nome", "Endereço", "Numero_de_pedidos")
    self.tabela_clientes.column("#0", width=0, stretch=NO)
    self.tabela_clientes.column("Nome", anchor=W, width=250)
    self.tabela_clientes.column("Endereço", anchor=W, width=250)
    self.tabela_clientes.column("Numero_de_pedidos", anchor=CENTER, width=200)

    self.tabela_clientes.heading("#0", text="", anchor=W)
    self.tabela_clientes.heading("Nome", text="Nome", anchor=CENTER)
    self.tabela_clientes.heading("Endereço", text="Endereço", anchor=CENTER)
    self.tabela_clientes.heading("Numero_de_pedidos", text="Numero de pedidos", anchor=CENTER)

    self.tabela_clientes.tag_configure('cor1', background="white")
    self.tabela_clientes.tag_configure('cor2', background="lightblue")

    conn = self.conectar_cliente()
    c = conn.cursor()
    c.execute("""SELECT cl.nome_cliente, cl.endereco, COUNT(pe.nome_cliente) 
                    FROM clientes as cl
                    JOIN pedidos as pe on cl.nome_cliente = pe.nome_cliente
                    GROUP BY cl.nome_cliente""")

    global contador_cliente
    contador_cliente = 0

    for nome, end, num in c.fetchall():
        if contador_cliente % 2 == 0:
            self.tabela_clientes.insert(parent='', index='end', text='',
                        values=(nome, end, num),
                        tags=('cor2',))

        else:
            self.tabela_clientes.insert(parent='', index='end', text='',
                                values=(nome, end, num),
                                tags=('cor1',))
        contador_cliente += 1
    conn.close()
    self.tabela_clientes.bind('<Double-Button-1>', self.seleciona)
        
  def acessorios(self):
    self.data_frame = LabelFrame(self.root_clientes, text= 'Novo cliente')
    self.data_frame.place(relx=0.05, rely=0.58, relwidth=0.9, relheight=0.2)
    self.data_frame.configure(background='snow')

    nome_label = Label(self.data_frame, text="Nome")
    nome_label.configure(font=('helvetica', 16), background='snow')
    nome_label.place(relx=0.15, rely=0.1, relwidth=0.2, relheight=0.35)
    self.nome_entry = Entry(self.data_frame, relief=FLAT, highlightbackground='lightblue')
    self.nome_entry.place(relx=0.1, rely=0.4, relwidth=0.3, relheight=0.28)
    self.nome_entry.focus()

    endereco_label = Label(self.data_frame, text="Bairro")
    endereco_label.configure(font=('helvetica', 16), background='snow')
    endereco_label.place(relx=0.64, rely=0.1, relwidth=0.2, relheight=0.35)
    self.endereco_entry = Entry(self.data_frame, relief=FLAT, highlightbackground='lightblue')
    self.endereco_entry.place(relx=0.585, rely=0.4, relwidth=0.3, relheight=0.28)

  def botoes(self):
    def verificacao():
        def chamar_cardapio():
            tela_cardapio(self.root, self.nome_entry.get().title(),
            self.endereco_entry.get().title(), self.fundo, self.botoes_inicio),
            self.frame_botao.destroy(), self.data_frame.destroy(), self.tree_frame.destroy()
        if self.nome_entry.get() == '':
            messagebox.showinfo('Info', 'Informe o nome do cliente')
        if self.endereco_entry.get() != '':
            conectar = Local.conectar_bairros(self)
            con = conectar.cursor()
            con.execute('''SELECT nome_bairro FROM bairros WHERE nome_bairro = %s''', (self.endereco_entry.get(),))
            bairro = con.fetchall()
            try:
                if bairro[0][0] == self.endereco_entry.get():
                    chamar_cardapio()
            except IndexError:
                messagebox.showwarning('Alerta', f'Bairro {self.endereco_entry.get()} não cadastrado')
                self.nome_entry.delete(0, 'end')
                self.endereco_entry.delete(0, 'end')

    self.frame_botao = Frame(self.root_clientes)
    self.frame_botao.place(relx=0.05, rely=0.8, relwidth=0.9, relheight=0.18)
    self.frame_botao.configure(background='snow')
    bt_cadastra = Image.open('Imagens/add.ico')
    img1 = ImageTk.PhotoImage(bt_cadastra)
    botao_salvar = Button(self.frame_botao, text= 'Cadastrar', image= img1, compound=LEFT,
    relief=FLAT, activebackground='lightblue', background='snow', activeforeground='snow',
    highlightbackground='snow',
    command= lambda: [self.salvar(self.nome_entry.get().title(), self.endereco_entry.get().title()),
    self.limpa(self.nome_entry, self.endereco_entry), self.clientes_geral()])
    botao_salvar.configure(font=('Roman', 14))
    botao_salvar.place(relx=0.1, rely=0.3, relwidth=0.2, relheight=0.45)
    botao_salvar.imagem = img1

    bt_fpedido = Image.open('Imagens/pagar.png')
    img_fpedido = ImageTk.PhotoImage(bt_fpedido)
    bt_new = Image.open('Imagens/carrinho.ico')
    img_new = ImageTk.PhotoImage(bt_new)
    new_pedido = Button(self.frame_botao, text= 'Novo\nPedido', image= img_new, compound=LEFT,
    relief=FLAT, activebackground='lightblue', background='snow', activeforeground='snow',
    highlightbackground='snow',
    command= lambda:[verificacao()])
    new_pedido.configure(font=('Roman', 14))
    new_pedido.place(relx=0.42, rely=0.3, relwidth=0.2, relheight=0.52)
    new_pedido.imagem = img_new

    bt_pesquisa = Image.open('Imagens/consultar.ico')
    img_pesquisar = ImageTk.PhotoImage(bt_pesquisa)
    pesquisar = Button(self.frame_botao, text= 'Pesquisar', image= img_pesquisar, compound=LEFT,
    relief=FLAT, activebackground='lightblue', background='snow', activeforeground='snow',
    highlightbackground='snow',
    command= lambda: [self.clientes_geral() ,self.pesquisar(self.nome_entry.get(), self.tabela_clientes), 
    self.limpa(self.nome_entry, self.endereco_entry)])
    pesquisar.configure(font=('Roman', 14))
    pesquisar.place(relx=0.75, rely=0.3, relwidth=0.2, relheight=0.45)
    pesquisar.imagem = img_pesquisar
  
  def inserir(self, name, end):
    self.nome_entry.insert(name, 'end')
    self.endereco_entry.insert(end, 'end')

  def seleciona(self, event):
    self.limpa(self.nome_entry, self.endereco_entry)
    for x in self.tabela_clientes.selection():
      n, e, p = self.tabela_clientes.item(x, 'values')
      self.nome_entry.insert(END, n)
      self.endereco_entry.insert(END, e)
    return self.nome_entry.get()
  
  def seleciona_cliente(self, event):
    self.limpa(self.nome_entry, self.endereco_entry)
    for x in self.tabela_clientes.selection():
      i, n, e= self.tabela_clientes.item(x, 'values')
      self.nome_entry.insert(END, n)
      self.endereco_entry.insert(END, e)

  def dados(self):
    name = self.nome_entry.get()
    local = self.endereco_entry.get()
    print(name, local)
    return name, local

class tela_cardapio(Cardapio, Pedido, Local):
    def __init__(self, root, info_cliente, end_cliente, fundo, botoes_inicio):
        super().__init__()
        self.root_cardapio = root
        self.root_cardapio.title('Cardapio')
        self.root_cardapio.configure(background='snow')
        self.fundo_inicio = fundo
        self.inicio_botoes = botoes_inicio
        self.cria_menu()
        self.cria_poke()
        self.menu_geral()
        self.opcoes()
        self.acessorios()
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
                
    def conectar_cardapio(self):
        return super().conectar_cardapio()

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
        self.name.configure(background='snow')

    def opcoes(self):
        # Add Menu
        my_menu = Menu(self.root_cardapio)
        self.root_cardapio.config(menu=my_menu)

        my_menu.add_command(label='Inicio', command=lambda:[self.name.destroy(),
        self.frame_menu.destroy(), self.frame_botao.destroy(), self.total.destroy(), self.frame_cardapio.destroy(),
        self.fundo_inicio, self.inicio_botoes, my_menu.destroy(), self.frame_total.destroy()])
        # Configurar menu
        option_menu = Menu(my_menu, tearoff=0)
        my_menu.add_cascade(label="Opções", menu=option_menu)
        # opcoes do menu
        option_menu.add_command(label="Configurar pratos", command= lambda:[conf_cardapio(self.root_cardapio, self.info_cliente,
        self.end_cliente, self.fundo_inicio, self.inicio_botoes)])
        option_menu.add_command(label="Monte seu poke", command= lambda:[self.monte_poke()])
        option_menu.add_command(label="Menu", command= lambda:[self.frame_cardapio.destroy(), self.menu_geral()])

    def total_pedido(self, valor):
        self.frame_total = Frame(self.root_cardapio)
        self.frame_total.place(relx=0.7, rely=0.65, relwidth=0.2, relheight=0.1)
        self.total = Label(self.frame_total, text=f'TOTAL: {valor}$')
        self.total.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)
        self.total.configure(background='snow')

    def set_total(self):
        try:
            self.frame_total.destroy()
            self.tipo_tele()
            self.valor_total = sum(self.carrinho_compras) + self.tipo_tele()
            self.total_pedido(self.valor_total)
        except AttributeError:
            self.tipo_tele()
            self.valor_total = sum(self.carrinho_compras) + self.tipo_tele()
            self.total_pedido(self.valor_total)
        except TypeError as erro:
            messagebox.showinfo('ERRO', 'Escolha o tipo de entrega')

    def soma_pratos(self):
        conn = self.conectar_cardapio()
        c = conn.cursor()
        c.execute("""SELECT valor_prato FROM menu WHERE nome_prato = %s""", (self.prato,))
        preco = c.fetchall()
        for x in preco:
            self.carrinho_compras.append(x[0])

    def acessorios(self):
        self.frame_botao = Frame(self.root_cardapio)
        self.frame_botao.place(relx=0.0, rely=0.63, relwidth=1, relheight=0.4)
        self.frame_botao.configure(background='snow')
        self.boy_label = Label(self.frame_botao, text='Motoboy')
        self.boy_label.configure(background='snow')
        self.boy_entry = Entry(self.frame_botao)

        self.data_label = Label(self.frame_botao, text='Data')
        self.data_label.configure(background='snow')
        self.data_label.place(relx=0.4, rely=0.35, relwidth=0.15, relheight=0.08)
            
        self.data_entry = Entry(self.frame_botao)
        self.data_entry.place(relx=0.4, rely=0.5, relwidth=0.2, relheight=0.1)

        self.tipo = IntVar(self.frame_botao)
        retirada = Radiobutton(self.frame_botao, text= 'Retirada', variable= self.tipo, value=1,
        activeforeground='blue', highlightbackground='snow', activebackground='snow')
        retirada.place(relx=0.05, rely=0.15, relwidth=0.12, relheight=0.1)
        retirada.configure(background='snow')
        ifood = Radiobutton(self.frame_botao, text= 'Ifood', variable= self.tipo, value=2,
        activeforeground='blue', highlightbackground='snow', activebackground='snow')
        ifood.place(relx=0.27, rely=0.15, relwidth=0.1, relheight=0.1)
        ifood.configure(background='snow')
        particular = Radiobutton(self.frame_botao, text= 'Tele Wonder', variable= self.tipo, value=3,
        activeforeground='blue', highlightbackground='snow', activebackground='snow')
        particular.place(relx=0.48, rely=0.15, relwidth=0.15, relheight=0.1)
        particular.configure(background='snow')

        bt_fpedido = Image.open('Imagens/pagar.png')
        img_fpedido = ImageTk.PhotoImage(bt_fpedido)
        finalizar = Button(self.frame_botao, image= img_fpedido, compound=CENTER, background='snow',
        activebackground='lightblue', highlightbackground='snow', relief=FLAT,
        command=lambda:[self.novo_pedido(self.info_cliente, self.memoria, self.boy_entry.get().title(),
        self.tipo_tele(), self.tipo_pedido, self.data_entry.get()),
        self.carrinho.delete(*self.carrinho.get_children()), self.boy_entry.delete(0, 'end'),
        self.data_entry.delete(0, 'end')])
        finalizar.place(relx=0.8, rely=0.5, relwidth=0.1, relheight=0.18)
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
                self.boy_label.place(relx=0.1, rely=0.4, relwidth=0.15, relheight=0.08)
                self.boy_entry.place(relx=0.05, rely=0.52, relwidth=0.25, relheight=0.1)
                return tele
            elif self.tipo.get() == 3:
                self.tipo_pedido = 2
                self.boy_label.place(relx=0.1, rely=0.75, relwidth=0.15, relheight=0.1)
                self.boy_entry.place(relx=0.05, rely=0.83, relwidth=0.25, relheight=0.05)
                conn = self.conectar_cardapio()
                c = conn.cursor()
                c.execute("""SELECT preco FROM bairros WHERE nome_bairro = %s""", (self.end_cliente,))
                valor = c.fetchall()
                print(valor)
                return valor[0][0]
        except AttributeError:
            messagebox.showerror('Pedido', 'Selecione o tipo de entrega')
            
    def seleciona(self, event):
        for x in self.menu.selection():
            self.prato, self.preco = self.menu.item(x, 'values')
            if self.prato not in self.memoria.keys():
                self.memoria[self.prato] = 1
                self.modelo.set_prato(self.valor.get()), self.inserir(), self.soma_pratos(), self.total.destroy()
                self.set_total()
            else:
                self.memoria[self.prato] +=1
                self.modelo.set_prato(self.valor.get()), self.inserir(), self.soma_pratos(), 
                self.set_total()
            
    def deseleciona(self, event):
        conn = self.conectar_cardapio()
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
        tree_scroll.configure(background='snow')

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
    def cria_menu(self):
        self.frame_cardapio = Frame(self.root_cardapio)
        self.frame_cardapio.place(relx=0.01, rely=0.02, relwidth=0.65, relheight=0.6)
        self.frame_cardapio.configure(background='snow')
        style = ttk.Style()
        style.theme_use('default')
        style.configure("tema_cardapio",
                background="white",
                foreground="black",
                rowheight=25,
                fieldbackground="#D3D3D3",
                font=('Helvetica', 11))
        style.map('tema_cardapio', background=[('selected', "#347083")])

        self.valor = StringVar(self.frame_cardapio)

        self.menu = ttk.Treeview(self.frame_cardapio, selectmode="browse")
        self.menu.place(relx=0.0, rely=0.0, relwidth=0.972, relheight=1)

    def cria_poke(self):
        self.frame_menu = Frame(self.root_cardapio)
        self.frame_menu.place(relx=0.01, rely=0.02, relwidth=0.65, relheight=0.6)
        self.frame_menu.configure(background='snow')
        style = ttk.Style()
        style.theme_use('default')
        style.configure("tema_cardapio",
                background="white",
                foreground="black",
                rowheight=25,
                fieldbackground="#D3D3D3",
                font=('Helvetica', 11))
        style.map('tema_cardapio', background=[('selected', "#347083")])

        self.valor = StringVar(self.frame_menu)

        self.menu = ttk.Treeview(self.frame_menu, selectmode="browse")
        self.menu.place(relx=0.0, rely=0.0, relwidth=0.972, relheight=1)

    def menu_geral(self):
        try:
            self.pag1.destroy()
            self.cria_menu()
        except:
            pass
        finally:
            self.menu.delete(*self.menu.get_children())
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

            conn = self.conectar_cardapio()
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
                    count += 2
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
        try:
            self.frame_cardapio.destroy()
        except:
            pass
        finally:
            self.pag1 = Frame(self.frame_menu)
            self.pag1.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)
            self.pag1.configure(background='snow')
            letra = font.Font(family='Arial', size= 20, weight='bold')
            letra2 = font.Font(family='Arial', size=12, weight='bold', slant='italic')
            letra3 = font.Font(family='Arial', size=10, weight='bold')

            base = Label(self.pag1, text='1.BASE')
            base.configure(font=letra, background='snow')
            base.place(relx=0.02, rely=0.03, relwidth=0.2, relheight=0.1)
            escolha_base = Label(self.pag1, text='Escolha 1', foreground='blue')
            escolha_base.configure(font=letra2, background='snow')
            escolha_base.place(relx=0.02, rely=0.13, relwidth=0.2, relheight=0.1)

            self.extra_poke = []
            self.escolha_base = []
            self.proteina = []
            self.base_1 = IntVar(self.pag1) 
            self.base_2 = IntVar(self.pag1) 
            self.base_3 = IntVar(self.pag1) 
            self.base_4 = IntVar(self.pag1) 
            self.base_5 = IntVar(self.pag1)

            self.op_base_1 = Checkbutton(self.pag1, text='Arroz de sushi', variable= self.base_1,
            highlightbackground='snow', activebackground='snow', activeforeground='blue4', relief=FLAT,
            anchor='w')
            self.op_base_1.place(relx=0.02, rely=0.25, relwidth=0.25, relheight=0.1)
            self.op_base_1.configure(background='snow')
            self.op_base_2 = Checkbutton(self.pag1, text='Arroz negro(+ R$4)', anchor='w', relief=FLAT,
            variable= self.base_2, highlightbackground='snow', activeforeground='blue4',
            activebackground='snow')
            self.op_base_2.place(relx=0.02, rely=0.35, relwidth=0.3, relheight=0.1)
            self.op_base_2.configure(background='snow')
            self.op_base_3 = Checkbutton(self.pag1, text='Quinoa(+R$4)', anchor='w', relief=FLAT,
            variable= self.base_3, highlightbackground='snow', activeforeground='blue4',
            activebackground='snow')
            self.op_base_3.place(relx=0.02, rely=0.45, relwidth=0.25, relheight=0.1)
            self.op_base_3.configure(background='snow')
            self.op_base_4 = Checkbutton(self.pag1, text='Espaguete de abobrinha', anchor='w', relief=FLAT,
            variable= self.base_4, highlightbackground='snow', activeforeground='blue4',
            activebackground='snow')
            self.op_base_4.place(relx=0.02, rely=0.55, relwidth=0.4, relheight=0.1)
            self.op_base_4.configure(background='snow')
            self.op_base_5 = Checkbutton(self.pag1, text='Espaguete de palmito de\n pupunha ao pesto(+ R$5)',
            relief=FLAT, anchor='w', variable= self.base_5, highlightbackground='snow', 
            activeforeground='blue4', activebackground='snow')
            self.op_base_5.place(relx=0.02, rely=0.65, relwidth=0.4, relheight=0.25)
            self.op_base_5.configure(background='snow')

            proteina = Label(self.pag1, text='1.PROTEÍNAS 120g', anchor='w')
            proteina.place(relx=0.45, rely=0.02, relwidth=0.55, relheight=0.15)
            proteina.configure(font=letra, background='snow')
            escolha_prot = Label(self.pag1, text='Escolha até 2 (60g de cada)', foreground='blue',
            anchor='w')
            escolha_prot.place(relx=0.45, rely=0.15, relwidth=0.5, relheight=0.08)
            escolha_prot.configure(font=letra2, background='snow')
            info_prot = Label(self.pag1, text='-Sera considerada a proteína de maior valor-',
            anchor='w')
            info_prot.place(relx=0.45, rely=0.23, relwidth=0.55, relheight=0.08)
            info_prot.configure(font=letra3, background='snow')

            self.prot1 = IntVar(self.root_cardapio)
            self.prot2 = IntVar(self.root_cardapio)
            self.prot3 = IntVar(self.root_cardapio)
            self.prot4 = IntVar(self.root_cardapio)
            op_prot1 = Checkbutton(self.pag1, text='Salmão', anchor='w', variable=self.prot1,
            highlightbackground='snow', activeforeground='blue4',)
            op_prot1.place(relx=0.45, rely=0.35, relwidth=0.25, relheight=0.1)
            op_prot1.configure(background='snow')
            op_prot2 = Checkbutton(self.pag1, text='Atum', anchor='w', variable=self.prot2,
            highlightbackground='snow', activeforeground='blue4',)
            op_prot2.place(relx=0.45, rely=0.45, relwidth=0.3, relheight=0.1)
            op_prot2.configure(background='snow')
            op_prot3 = Checkbutton(self.pag1, text='Camarão', anchor='w', variable=self.prot3,
            highlightbackground='snow', activeforeground='blue4',)
            op_prot3.place(relx=0.45, rely=0.55, relwidth=0.25, relheight=0.1)
            op_prot3.configure(background='snow')
            op_prot4 = Checkbutton(self.pag1, text='Shitake', anchor='w', variable=self.prot4,
            highlightbackground='snow', activeforeground='blue4')
            op_prot4.place(relx=0.45, rely=0.65, relwidth=0.25, relheight=0.1)
            op_prot4.configure(background='snow')

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
                        self.extra_poke.append(60)
                    if self.prot4.get() == 1:
                        self.proteina.append(4)
                        self.extra_poke.append(50)
                    erros()
                except AttributeError as error:
                    messagebox.showwarning('ERRO', error)

            bt_avancar = Image.open('Imagens/avancar.png')
            img_avancar = ImageTk.PhotoImage(bt_avancar)
            pag2 = Button(self.pag1, image= img_avancar, compound=CENTER, activebackground='lightblue',
            command=lambda:[verificacao()])
            pag2.place(relx=0.8, rely=0.85, relwidth=0.1, relheight=0.1)
            pag2.configure(background='snow')
            pag2.imagem = img_avancar
    
    def poke_2(self):
        self.pag1.place_forget()
        self.pag2 = Frame(self.frame_menu)
        self.pag2.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)
        self.pag2.configure(background='snow')
        letra = font.Font(family='Arial', size= 20, weight='bold')
        letra2 = font.Font(family='Arial', size=12, weight='bold', slant='italic')
        
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
        make.configure(font=letra, background='snow')
        make.place(relx=0.02, rely=0.03, relwidth=0.25, relheight=0.1)
        escolha_make = Label(self.pag2, text='Escolha até 4', foreground='blue', anchor='w')
        escolha_make.configure(font=letra2, background='snow')
        escolha_make.place(relx=0.02, rely=0.13, relwidth=0.2, relheight=0.1)

        op_make1 = Checkbutton(self.pag2, text='Sunomono', variable= self.make1 ,anchor='w',
        highlightbackground='snow', activeforeground='blue4', activebackground='snow')
        op_make1.place(relx=0.45, rely=0.25, relwidth=0.25, relheight=0.1)
        op_make1.configure(background='snow')
        op_make2 = Checkbutton(self.pag2, text='Ceviche de manga', variable= self.make2 ,anchor='w',
        highlightbackground='snow', activeforeground='blue4', activebackground='snow')
        op_make2.configure(background='snow')
        op_make2.place(relx=0.05, rely=0.35, relwidth=0.3, relheight=0.1)
        op_make2.configure(background='snow')
        op_make3 = Checkbutton(self.pag2, text='Abacaxi', variable= self.make3 ,anchor='w',
        highlightbackground='snow', activeforeground='blue4', activebackground='snow')
        op_make3.configure(background='snow')
        op_make3.place(relx=0.05, rely=0.45, relwidth=0.25, relheight=0.1)
        op_make3.configure(background='snow')
        op_make4 = Checkbutton(self.pag2, text='Tomate confit', variable= self.make4,anchor='w',
        highlightbackground='snow', activeforeground='blue4', activebackground='snow')
        op_make4.configure(background='snow')
        op_make4.place(relx=0.05, rely=0.55, relwidth=0.25, relheight=0.1)
        op_make4.configure(background='snow')
        op_make5 = Checkbutton(self.pag2, text='Cenoura salteada', variable= self.make5 ,anchor='w',
        highlightbackground='snow', activeforeground='blue4', activebackground='snow')
        op_make5.configure(background='snow')
        op_make5.place(relx=0.05, rely=0.65, relwidth=0.3, relheight=0.1)
        op_make5.configure(background='snow')
        op_make6 = Checkbutton(self.pag2, text='Cebola roxa caramelizada', variable= self.make6 ,anchor='w',
        highlightbackground='snow', activeforeground='blue4', activebackground='snow')
        op_make6.configure(background='snow')
        op_make6.place(relx=0.05, rely=0.75, relwidth=0.4, relheight=0.1)
        op_make6.configure(background='snow')
        op_make7 = Checkbutton(self.pag2, text='Moranga assada', variable= self.make7 ,anchor='w',
        highlightbackground='snow', activeforeground='blue4', activebackground='snow')
        op_make7.configure(background='snow')
        op_make7.place(relx=0.05, rely=0.25, relwidth=0.3, relheight=0.1)
        op_make7.configure(background='snow')
        op_make8 = Checkbutton(self.pag2, text='Damasco', variable= self.make8 ,anchor='w',
        highlightbackground='snow', activeforeground='blue4', activebackground='snow')
        op_make8.configure(background='snow')
        op_make8.place(relx=0.45, rely=0.35, relwidth=0.25, relheight=0.1)
        op_make8.configure(background='snow')
        op_make9 = Checkbutton(self.pag2, text='Tofu', variable= self.make9 ,anchor='w',
        highlightbackground='snow', activeforeground='blue4', activebackground='snow')
        op_make9.configure(background='snow')
        op_make9.place(relx=0.45, rely=0.45, relwidth=0.25, relheight=0.1)
        op_make9.configure(background='snow')
        op_make10 = Checkbutton(self.pag2, text='Alga nori', variable= self.make10 ,anchor='w',
        highlightbackground='snow', activeforeground='blue4', activebackground='snow')
        op_make10.configure(background='snow')
        op_make10.place(relx=0.45, rely=0.55, relwidth=0.3, relheight=0.1)
        op_make10.configure(background='snow')
        op_make11 = Checkbutton(self.pag2, text='Edaname', variable= self.make11 ,anchor='w',
        highlightbackground='snow', activeforeground='blue4', activebackground='snow')
        op_make11.configure(background='snow')
        op_make11.place(relx=0.45, rely=0.65, relwidth=0.25, relheight=0.1)
        op_make11.configure(background='snow')
        op_make12 = Checkbutton(self.pag2, text='Manga em cubos', variable= self.make12 ,anchor='w',
        highlightbackground='snow', activeforeground='blue4', activebackground='snow')
        op_make12.configure(background='snow')
        op_make12.place(relx=0.45, rely=0.75, relwidth=0.25, relheight=0.1)
        op_make12.configure(background='snow')

        bt_avancar = Image.open('Imagens/avancar.png')
        img_avancar = ImageTk.PhotoImage(bt_avancar)
        pag2 = Button(self.pag2, image= img_avancar, compound=CENTER, relief=FLAT,
        highlightbackground='snow', activebackground='lightblue', command=lambda:[check_make()])
        pag2.place(relx=0.8, rely=0.85, relwidth=0.1, relheight=0.1)
        pag2.configure(background='snow')
        pag2.imagem = img_avancar

        bt_voltar = Image.open('Imagens/voltar.png')
        img_voltar = ImageTk.PhotoImage(bt_voltar)
        pag1 = Button(self.pag2, image= img_voltar, compound=CENTER, relief=FLAT,
        highlightbackground='snow', activebackground='lightblue', command=lambda:[self.monte_poke()])
        pag1.place(relx=0.2, rely=0.85, relwidth=0.1, relheight=0.1)
        pag1.configure(background='snow')
        pag1.imagem = img_voltar

    def poke_3(self):
        self.pag2.forget()
        self.pag3 = Frame(self.frame_menu)
        self.pag3.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)
        self.pag3.configure(background='snow')
        letra = font.Font(family='Arial', size= 20, weight='bold')
        letra2 = font.Font(family='Arial', size=12, weight='bold', slant='italic')
        
        self.crunch_it = []
        self.crunch1 = IntVar(self.pag3)
        self.crunch2 = IntVar(self.pag3)
        self.crunch3 = IntVar(self.pag3)

        crunch = Label(self.pag3, text='3.CRUNCH IT', anchor='w')
        crunch.configure(font=letra, background='snow')
        crunch.place(relx=0.02, rely=0.03, relwidth=0.35, relheight=0.1)
        escolha_crunch = Label(self.pag3, text='Escolha 1', foreground='blue', anchor='w')
        escolha_crunch.configure(font=letra2, background='snow')
        escolha_crunch.place(relx=0.02, rely=0.13, relwidth=0.22, relheight=0.1)

        op_crunch1 = Checkbutton(self.pag3, text='Chips de banana', anchor='w',
        highlightbackground='snow', activeforeground='blue4', activebackground='snow',
        variable= self.crunch1)
        op_crunch1.place(relx=0.02, rely=0.25, relwidth=0.28, relheight=0.1)
        op_crunch1.configure(background='snow')
        op_crunch2 = Checkbutton(self.pag3, text='Chips de batata doce', anchor='w',
        highlightbackground='snow', activeforeground='blue4', activebackground='snow',
        variable= self.crunch2)
        op_crunch2.place(relx=0.02, rely=0.35, relwidth=0.45, relheight=0.1)
        op_crunch2.configure(background='snow')
        op_crunch3 = Checkbutton(self.pag3, text='Kale', anchor='w',
        highlightbackground='snow', activeforeground='blue4', activebackground='snow',
        variable= self.crunch3)
        op_crunch3.place(relx=0.02, rely=0.45, relwidth=0.25, relheight=0.1)
        op_crunch3.configure(background='snow')

        top_master = Frame(self.pag3)
        top_master.place(relx=0.39, rely=0.0, relwidth=0.6, relheight=1)
        top_master.configure(background='snow')
        top = Label(top_master, text='4.TOP IT', anchor='w')
        top.configure(font=letra, background='snow')
        top.place(relx=0.45, rely=0.03, relwidth=0.4, relheight=0.1)
        escolha_top = Label(top_master, text='Escolha 1', foreground='blue', anchor='w')
        escolha_top.configure(font=letra2, background='snow')
        escolha_top.place(relx=0.45, rely=0.13, relwidth=0.4, relheight=0.1)

        self.top_it = []
        top1 = IntVar(top)
        top2 = IntVar(top)
        top3 = IntVar(top)
        top4 = IntVar(top)
        top5 = IntVar(top)
        top6 = IntVar(top)
        top7 = IntVar(top)
        top8 = IntVar(top)

        op_top1 = Checkbutton(top_master, text='Castanhas', anchor='w', variable= top1,
        highlightbackground='snow', activeforeground='blue4', activebackground='snow')
        op_top1.place(relx=0.6, rely=0.45, relwidth=0.35, relheight=0.1)
        op_top1.configure(background='snow')
        op_top2 = Checkbutton(top_master, text='Nozes', anchor='w', variable= top2,
        highlightbackground='snow', activeforeground='blue4', activebackground='snow')
        op_top2.place(relx=0.6, rely=0.25, relwidth=0.35, relheight=0.1)
        op_top2.configure(background='snow')
        op_top3 = Checkbutton(top_master, text='Pistache', anchor='w', variable= top3,
        highlightbackground='snow', activeforeground='blue4', activebackground='snow')
        op_top3.place(relx=0.1, rely=0.35, relwidth=0.35, relheight=0.1)
        op_top3.configure(background='snow')
        op_top4 = Checkbutton(top_master, text='Amendôas', anchor='w', variable= top4,
        highlightbackground='snow', activeforeground='blue4', activebackground='snow')
        op_top4.place(relx=0.6, rely=0.35, relwidth=0.35, relheight=0.1)
        op_top4.configure(background='snow')
        op_top5 = Checkbutton(top_master, text='Gergerlim negro', anchor='w', variable= top5,
        highlightbackground='snow', activeforeground='blue4', activebackground='snow')
        op_top5.place(relx=0.1, rely=0.45, relwidth=0.5, relheight=0.1)
        op_top5.configure(background='snow')
        op_top6 = Checkbutton(top_master, text='Lascas de coco', anchor='w', variable= top6,
        highlightbackground='snow', activeforeground='blue4', activebackground='snow')
        op_top6.place(relx=0.1, rely=0.25, relwidth=0.45, relheight=0.1)
        op_top6.configure(background='snow')
        op_top7 = Checkbutton(top_master, text='Semente de abóbora', anchor='w', variable= top7,
        highlightbackground='snow', activeforeground='blue4', activebackground='snow')
        op_top7.place(relx=0.1, rely=0.55, relwidth=0.55, relheight=0.1)
        op_top7.configure(background='snow')
        op_top8 = Checkbutton(top_master, text='Linhaça dourada', anchor='w', variable= top8,
        highlightbackground='snow', activeforeground='blue4', activebackground='snow')
        op_top8.place(relx=0.1, rely=0.65, relwidth=0.5, relheight=0.1)
        op_top8.configure(background='snow')

        def verifica_pg3():
            try:
                if self.crunch1.get() == 1:
                    self.crunch_it.append(1)
                if self.crunch2.get() == 1:
                    self.crunch_it.append(2)
                if self.crunch3.get() == 1:
                    self.crunch_it.append(3)
                elif len(self.crunch_it) > 1:
                    messagebox.showerror('ERRO', 'Selecione apenas 1 opção de crunch it')
                    self.crunch_it.clear()
                    self.top_it.clear()
                elif len(self.crunch_it) == 0:
                    messagebox.showerror('ERRO', 'Selecione no minímo 1 opção de crunch it')
                    self.crunch_it.clear()
                    self.top_it.clear()
                if top1.get() == 1:
                    self.top_it.append(1)
                if top2.get() == 1:
                    self.top_it.append(2)
                if top3.get() == 1:
                    self.top_it.append(3)
                if top4.get() == 1:
                    self.top_it.append(4)
                if top5.get() == 1:
                    self.top_it.append(5)
                if top6.get() == 1:
                    self.top_it.append(6)
                if top7.get() == 1:
                    self.top_it.append(7)
                if top8.get() == 1:
                    self.top_it.append(8)
                elif len(self.top_it) > 1:
                    messagebox.showerror('ERRO', 'Selecione apenas 1 opção de top it')
                    self.top_it.clear()
                    self.crunch_it.clear()
                elif len(self.top_it) == 0:
                    messagebox.showerror('ERRO', 'Selecione 1 opção de top it')
                    self.top_it.clear()
                    self.crunch_it.clear()
                
                self.poke_4()
            except error:
                messagebox.showerror('ERRO', "Erro inesperado, contate o programador")

        bt_avancar = Image.open('Imagens/avancar.png')
        img_avancar = ImageTk.PhotoImage(bt_avancar)
        pag3 = Button(top_master, image= img_avancar, compound=CENTER, activebackground='lightblue',
        highlightbackground='snow', command=lambda:[verifica_pg3()])
        pag3.place(relx=0.68, rely=0.85, relwidth=0.15, relheight=0.1)
        pag3.configure(background='snow')
        pag3.imagem = img_avancar

        bt_voltar = Image.open('Imagens/voltar.png')
        img_voltar = ImageTk.PhotoImage(bt_voltar)
        pag2 = Button(self.pag3, image= img_voltar, compound=CENTER, activebackground='lightblue',
        highlightbackground='snow', command=lambda:[self.poke_2()])
        pag2.place(relx=0.2, rely=0.85, relwidth=0.1, relheight=0.1)
        pag2.configure(background='snow')
        pag2.imagem = img_voltar

    def poke_4(self):
        self.pag3.forget()
        self.pag4 = Frame(self.frame_menu)
        self.pag4.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)
        self.pag4.configure(background='snow')
        letra = font.Font(family='Arial', size= 20, weight='bold')
        letra2 = font.Font(family='Arial', size=12, weight='bold', slant='italic')

        self.finish_it = IntVar(self.pag4)

        finish = Label(self.pag4, text='4.FINISH IT', anchor='w')
        finish.configure(font=letra, background='snow')
        finish.place(relx=0.05, rely=0.03, relwidth=0.3, relheight=0.1)
        escolha_finish = Label(self.pag4, text='Escolha 1', foreground='blue', anchor='w')
        escolha_finish.configure(font=letra2, background='snow')
        escolha_finish.place(relx=0.05, rely=0.13, relwidth=0.2, relheight=0.1)

        self.finish_it = []
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
        variable= finish1, highlightbackground='snow', activeforeground='blue4',
        activebackground='snow')
        op_finish1.configure(background='snow')
        op_finish1.place(relx=0.05, rely=0.25, relwidth=0.25, relheight=0.1)
        op_finish2 = Checkbutton(self.pag4, text='Wasabi', anchor='w',
        variable= finish2, highlightbackground='snow', activeforeground='blue4',
        activebackground='snow')
        op_finish2.configure(background='snow')
        op_finish2.place(relx=0.05, rely=0.35, relwidth=0.3, relheight=0.1)
        op_finish3 = Checkbutton(self.pag4, text='Ponzu', anchor='w',
        variable= finish3, highlightbackground='snow', activeforeground='blue4',
        activebackground='snow')
        op_finish3.configure(background='snow')
        op_finish3.place(relx=0.05, rely=0.45, relwidth=0.25, relheight=0.1)
        op_finish4 = Checkbutton(self.pag4, text='Cream cheese', anchor='w',
        variable= finish4, highlightbackground='snow', activeforeground='blue4',
        activebackground='snow')
        op_finish4.configure(background='snow')
        op_finish4.place(relx=0.05, rely=0.55, relwidth=0.25, relheight=0.1)
        op_finish5 = Checkbutton(self.pag4, text='Tarê', anchor='w',
        variable= finish5, highlightbackground='snow', activeforeground='blue4',
        activebackground='snow')
        op_finish5.configure(background='snow')
        op_finish5.place(relx=0.05, rely=0.65, relwidth=0.3, relheight=0.1)
        op_finish6 = Checkbutton(self.pag4, text='Tarê de laranja', anchor='w',
        variable= finish6, highlightbackground='snow', activeforeground='blue4',
        activebackground='snow')
        op_finish6.configure(background='snow')
        op_finish6.place(relx=0.45, rely=0.25, relwidth=0.25, relheight=0.1)
        op_finish7 = Checkbutton(self.pag4, text='Mel com gengibre', anchor='w',
        variable= finish7, highlightbackground='snow', activeforeground='blue4',
        activebackground='snow')
        op_finish7.configure(background='snow')
        op_finish7.place(relx=0.45, rely=0.35, relwidth=0.32, relheight=0.1)
        op_finish8 = Checkbutton(self.pag4, text='Molho de pimenta com srirancha', anchor='w',
        variable= finish8, highlightbackground='snow', activeforeground='blue4',
        activebackground='snow')
        op_finish8.configure(background='snow')
        op_finish8.place(relx=0.45, rely=0.45, relwidth=0.5, relheight=0.1)
        op_finish9 = Checkbutton(self.pag4, text='Soyo de coco(+ R$3)', anchor='w',
        variable= finish9, highlightbackground='snow', activeforeground='blue4',
        activebackground='snow')
        op_finish9.configure(background='snow')
        op_finish9.place(relx=0.45, rely=0.55, relwidth=0.4, relheight=0.1)

        def verifica_pag4():
            try:
                if finish1.get() == 1:
                    self.finish_it.append(1)
                if finish2.get() == 1:
                    self.finish_it.append(2)
                if finish3.get() == 1:
                    self.finish_it.append(3)
                if finish4.get() == 1:
                    self.finish_it.append(4)
                if finish5.get() == 1:
                    self.finish_it.append(5)
                if finish6.get() == 1:
                    self.finish_it.append(6)
                if finish7.get() == 1:
                    self.finish_it.append(7)
                if finish8.get() == 1:
                    self.finish_it.append(8)
                if finish9.get() == 1:
                    self.finish_it.append(9)
                    self.extra_poke.append(3)
                elif len(self.finish_it) > 1:
                    messagebox.showerror('ERRO', "Selecione apenas 1 opção de finish it")
                    self.finish_it.clear()
                elif len(self.finish_it) == 0:
                    messagebox.showerror('ERRO', 'Selecione no minímo 1 opção de finish it')
                    self.finish_it.clear()
                self.finish = self.finish_it
                #self.finish_it.clear()
                
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

            conn = self.conectar_cardapio()
            c = conn.cursor()
            c.execute("""UPDATE menu SET valor_prato = %s WHERE nome_prato = %s""",
            (sum(self.extra_poke), 'Monte seu poke'))
            c.execute("""SELECT id_pedido FROM pedidos WHERE nome_cliente = %s""",
            (self.info_cliente,))
            idd = c.fetchall()

            #salva as opcoes do poke
            opcoes_poke = {'base': self.escolha_base, 'proteina': self.proteina,
            'make_it': self.make_it, 'crunch_it': self.crunch_it, 'top_it': self.top_it,
            'finish_it': self.finish}
            try:
                memory = open('Escolhas.json', 'r', encoding='utf8')
                memoria = json.load(memory)
                memory.close()
                pok = {self.info_cliente: {idd[0][0]: opcoes_poke}}
                memoria.append(pok)
                memory =  open('Escolhas.json', 'w', encoding= 'utf8')
                json.dump(memoria, memory, indent=2)
                memory.close() 
            except FileNotFoundError:
                poke = [{self.info_cliente: {idd[0][0]: opcoes_poke}}]
                with open('Escolhas.json', 'w', encoding= 'utf8') as f:
                    json.dump(poke, f, indent=2)
                memory = open('Escolhas.json', 'r')
                 
        pag4 = Button(self.pag4, text='ADD', activebackground='lightblue', highlightbackground='snow',
        command=lambda:[verifica_pag4(), add_poke()])
        pag4.place(relx=0.8, rely=0.85, relwidth=0.1, relheight=0.1)
        pag4.configure(background='snow')

        bt_voltar = Image.open('Imagens/voltar.png')
        img_voltar = ImageTk.PhotoImage(bt_voltar)
        pag3 = Button(self.pag4, image= img_voltar, compound=CENTER, activebackground='lightblue',
        highlightbackground='snow', command=lambda:[self.poke_3()])
        pag3.place(relx=0.2, rely=0.85, relwidth=0.1, relheight=0.1)
        pag3.configure(background='snow')
        pag3.imagem = img_voltar

    def atualiza_tabela(self):
            self.menu.delete(*self.menu.get_children())
            conn = self.conectar_cardapio() 
            c = conn.cursor()
            c.execute("""SELECT * FROM menu ORDER BY nome_prato""")
            global count
            count = 0
            self.menu.insert('', 'end', 'Snack', text='Snack', tags=('cor3',), values='⮯Snacks')
            self.menu.insert('', 'end', 'Bowl', text='Bowls', tags=('cor4',), values='⮯Bowls')
            self.menu.insert('', 'end', 'Salada', text='Saladas', tags=('cor3',), values='⮯Saladas')
            self.menu.insert('', 'end', 'Brunch', text='Brunch', tags=('cor4',), values='⮯Brunch')            
            self.menu.insert('', 'end', 'Pizza', text='Pizzas', tags=('cor3',), values='⮯Pizzas')
            self.menu.insert('', 'end', 'Burger', text='Burgers', tags=('cor4',), values='⮯Burgers')
            self.menu.insert('', 'end', 'Poke', text='Poke', tags=('cor3',), values='⮯Pokes')
            self.menu.insert('', 'end', 'Doce', text='Doces', tags=('cor4',), values='⮯Doces')
            self.menu.insert('', 'end', 'Cafe', text='Cafe', tags=('cor3',), values='⮯Cafés')
            self.menu.insert('', 'end', 'Suco', text='Suco', tags=('cor4',), values='⮯Sucos')
            self.menu.insert('', 'end', 'Bebida', text='Bebida', tags=('cor3',), values='⮯Bebidas')

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
