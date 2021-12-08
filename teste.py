from tkinter import *
from tkinter import ttk
from cardapio_v2 import Cardapio, Modelo_prato
from pedido import *
from PIL import Image, ImageTk


class tela_cardapio(Cardapio, Pedido):
    def __init__(self, root, info_cliente):
        super().__init__()
        self.root = Toplevel(root)
        self.root.title('Cardapio')
        self.root.geometry('800x500')
        self.menu_geral()
        self.opcoes()
        self.botoes()
        self.info_cliente = info_cliente
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

    def adicionar(self, prato, valor):
        return super().adicionar(prato, valor)

    def apagar(self, prato):
        return super().apagar(prato)

    def exibir_pratos(self):
        return super().exibir_pratos()

    def limpa(self, nome, valor):
        return super().limpa(nome, valor)

    def novo_pedido(self, nome_c, prato, func):
        return super().novo_pedido(nome_c, prato, func)

    def nome_pedido(self, nome_cliente):
        self.name = LabelFrame(self.root, text=nome_cliente)
        self.name.place(relx=0.65, rely=0.05, relwidth=0.32, relheight=0.5)

    def opcoes(self):
        # Add Menu
        my_menu = Menu(self.root)
        self.root.config(menu=my_menu)

        # Configurar menu
        option_menu = Menu(my_menu, tearoff=0)
        my_menu.add_cascade(label="Opções", menu=option_menu)
        # opcoes do menu
        option_menu.add_command(label="Cardapio", command= lambda:[self.add_prato()])

    def add_prato(self):
        self.janela = Toplevel(self.root)
        self.janela.title('Configurações - cardapio')
        self.janela.geometry('500x250')

        #Labels e Entrys
        lb_prato = Label(self.janela, text='Prato')
        lb_prato.place(relx=0.1, rely=0.05, relwidth=0.4, relheight=0.3)
        ent_prato = Entry(self.janela)
        ent_prato.place(relx=0.08, rely=0.25, relwidth=0.4, relheight=0.1)

        lb_valor = Label(self.janela, text='Valor')
        lb_valor.place(relx=0.5, rely=0.05, relwidth=0.4, relheight=0.3)
        ent_valor = Entry(self.janela)
        ent_valor.place(relx=0.6, rely=0.25, relwidth=0.2, relheight=0.1)

        bt_add = Button(self.janela, text='Adicionar', command=lambda:[self.adicionar(ent_prato.get(),
        ent_valor.get()), self.limpa(ent_prato, ent_valor)])
        bt_add.place(relx=0.1, rely=0.5, relwidth=0.18, relheight=0.15)
        bt_atualizar = Button(self.janela, text='Atualizar')
        bt_atualizar.place(relx=0.4, rely=0.5, relwidth=0.18, relheight=0.15)
        bt_apagar = Button(self.janela, text='Apagar', command=lambda: [self.apagar(ent_prato.get()),
        self.limpa(ent_prato, ent_valor)])
        bt_apagar.place(relx=0.7, rely=0.5, relwidth=0.18, relheight=0.15)

    def total_pedido(self, valor):
        self.total = Label(self.root, text=f'TOTAL: {valor}')
        self.total.place(relx=0.7, rely=0.6, relwidth=0.3, relheight=0.15)

    def set_total(self):
        self.valor_total = sum(self.carrinho_compras)
        self.total_pedido(self.valor_total)
        return self.valor_total

    def soma_pratos(self):
        conn = self.conectar()
        c = conn.cursor()
        prato = self.prato
        c.execute('''SELECT valor_prato FROM menu WHERE nome_prato = %s''', (prato,))
        preco = c.fetchall()
        for x in preco:
            self.carrinho_compras.append(x[0])
            print(self.carrinho_compras)

    def botoes(self):
        botao_add = Button(self.root, text = 'Selecionar', command=lambda:[
        self.modelo.set_prato(self.valor.get()), self.inserir(), self.soma_pratos(), 
        self.set_total()])
        botao_add.place(relx=0.1, rely=0.7, relwidth=0.15, relheight=0.1)

        remover = Button(self.root, text = 'Remover', command= lambda:[self.seleciona()])
        remover.place(relx=0.4, rely=0.7, relwidth=0.15, relheight=0.1)

        finalizar = Button(self.root, text='Finalizar\nPedido', 
        command=lambda:[self.novo_pedido(self.info_cliente, self.memoria, 'Bruno')])
        finalizar.place(relx=0.8, rely=0.8, relwidth=0.15, relheight=0.1)

    def seleciona(self, event):
        for x in self.menu.selection():
            self.prato, preco = self.menu.item(x, 'values')
            if self.prato not in self.memoria.keys():
                self.memoria[self.prato] = 1
                self.modelo.set_prato(self.valor.get()), self.inserir(), self.soma_pratos(), 
                self.set_total()
            else:
                self.memoria[self.prato] +=1
                self.modelo.set_prato(self.valor.get()), self.inserir(), self.soma_pratos(), 
                self.set_total()

    def deseleciona(self, event):
        for x in self.carrinho.selection():
            qunat, prato= self.carrinho.item(x, 'values')
            print(prato)
            print(self.memoria)
            self.memoria[prato] -=1
            self.inserir()

    def tabela(self):
        style = ttk.Style()

        style.theme_use('default')

        style.configure("Treeview",
                background="#D3D3D3",
                foreground="black",
                rowheight=25,
                fieldbackground="#D3D3D3")

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

        self.carrinho.bind('<Double-Button-1>', self.deseleciona)

    def select_pratos(self):    
        for x in self.memoria.keys():
            return x

    def inserir(self):
        self.carrinho.delete(*self.carrinho.get_children())
        for p, q in self.memoria.items():
            print(self.memoria)
            self.carrinho.insert(parent='', index='end', text='',
                            values=(q, p))
            self.set_total()

    #Menu
    def menu_geral(self):
        fr1 = Frame(self.root)
        fr1.place(relx=0.01, rely=0.02, relwidth=0.65, relheight=0.6)
        self.valor = StringVar(fr1)
        
        style = ttk.Style()

        style.theme_use('default')

        style.configure("Treeview",
                background="#D3D3D3",
                foreground="black",
                rowheight=25,
                fieldbackground="#D3D3D3")

        tree_scroll = Scrollbar(fr1)
        tree_scroll.place(relx=0.945, rely=0.02, relwidth=0.03, relheight=0.98)

        self.menu = ttk.Treeview(fr1, yscrollcommand=tree_scroll.set,
                             selectmode="extended")
        self.menu.place(relx=0.01, rely=0.02, relwidth=0.935, relheight=0.98)

        tree_scroll.config(command=self.menu.yview)

        self.menu['columns'] = ("Prato", "Valor")
        self.menu.column("#0", width=0, stretch=NO)
        self.menu.column("Prato", anchor=W, width=250)
        self.menu.column("Valor", anchor=CENTER, width=50)

        self.menu.heading("#0", text="", anchor=W)
        self.menu.heading("Prato", text="Prato", anchor=CENTER)
        self.menu.heading("Valor", text="Valor", anchor=CENTER)

        conn = self.conectar()
        c = conn.cursor()
        c.execute("""SELECT * FROM menu""")
        global count
        count = 0
        for idd, prato, valor in c.fetchall():
            if count % 2 == 0:
                self.menu.insert(parent='', index='end', text='',
                               values=(prato, valor),
                               tags=('evenrow',))
            else:
                self.menu.insert(parent='', index='end', text='',
                               values=(prato, valor),
                               tags=('oddrow',))
            count += 1

        self.menu.bind('<Button-1>', self.seleciona)
