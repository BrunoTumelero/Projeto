from tkinter import *
from tkinter import ttk
import tkinter.font as font
from tkinter import messagebox
from cardapio_v2 import Cardapio, Modelo_prato
from pedido import *
from bairrosv2 import Local
from PIL import Image, ImageTk


class tela_cardapio(Cardapio, Pedido, Local):
    def __init__(self, root_cardapio, info_cliente, end_cliente):
        super().__init__()
        self.root_cardapio = Toplevel(root_cardapio)
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
        return self.valor_total

    def soma_pratos(self):
        conn = self.conectar()
        c = conn.cursor()
        prato = self.prato
        c.execute('''SELECT valor_prato FROM menu WHERE nome_prato = %s''', (prato,))
        preco = c.fetchall()
        for x in preco:
            print(x)
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

        finalizar = Button(self.root_cardapio, text='Finalizar\nPedido', 
        command=lambda:[self.novo_pedido(self.info_cliente, self.memoria, self.boy_entry.get().title(),
        self.tipo_tele(), self.tipo_pedido, self.data_entry.get()),
        self.carrinho.delete(*self.carrinho.get_children()), self.boy_entry.delete(0, 'end'),
        self.data_entry.delete(0, 'end'), self.total_pedido(0)])
        finalizar.place(relx=0.8, rely=0.8, relwidth=0.12, relheight=0.1)

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
        base = Label(self.pag1, text='1.BASE')
        letra = font.Font(family='Arial', size= 20, weight='bold')
        letra2 = font.Font(family='Arial', size=12, weight='bold', slant='italic')
        letra3 = font.Font(family='Arial', size=10, weight='bold')
        base.configure(font=letra)
        base.place(relx=0.02, rely=0.03, relwidth=0.2, relheight=0.1)
        escolha_base = Label(self.pag1, text='Escolha 1', foreground='white')
        escolha_base.configure(font=letra2)
        escolha_base.place(relx=0.02, rely=0.13, relwidth=0.2, relheight=0.1)

        op_base_1 = Radiobutton(self.pag1, text='Arroz de sushi', anchor='w', value= 1)
        op_base_1.place(relx=0.02, rely=0.25, relwidth=0.25, relheight=0.1)
        op_base_2 = Radiobutton(self.pag1, text='Arroz negro(+ R$4)', anchor='w', value= 2)
        op_base_2.place(relx=0.02, rely=0.35, relwidth=0.3, relheight=0.1)
        op_base_3 = Radiobutton(self.pag1, text='Quinoa(+R$4)', anchor='w', value= 3)
        op_base_3.place(relx=0.02, rely=0.45, relwidth=0.25, relheight=0.1)
        op_base_4 = Radiobutton(self.pag1, text='Espaguete de abobrinha', anchor='w', value= 4)
        op_base_4.place(relx=0.02, rely=0.55, relwidth=0.4, relheight=0.1)
        op_base_5 = Radiobutton(self.pag1, text='Espaguete de palmito de\n pupunha ao pesto(+ R$5',
        anchor='w', value= 5)
        op_base_5.place(relx=0.02, rely=0.65, relwidth=0.4, relheight=0.25)

        proteina = Label(self.pag1, text='1.PROTEÍNAS 120g', anchor='w')
        letra = font.Font(family='Arial', size= 20, weight='bold')
        letra2 = font.Font(family='Arial', size=14, weight='bold', slant='italic')
        proteina.configure(font=letra)
        proteina.place(relx=0.45, rely=0.03, relwidth=0.4, relheight=0.1)
        escolha_prot = Label(self.pag1, text='Escolha até 2 (60g de cada)', foreground='white',
        anchor='w')
        info_prot = Label(self.pag1, text='-Sera considerada a proteína de maior valor-',
        anchor='w')
        info_prot.place(relx=0.45, rely=0.22, relwidth=0.55, relheight=0.1)
        info_prot.configure(font=letra3)
        escolha_prot.configure(font=letra2)
        escolha_prot.place(relx=0.45, rely=0.13, relwidth=0.5, relheight=0.1)

        op_prot1 = Checkbutton(self.pag1, text='Salmão', anchor='w')
        op_prot1.place(relx=0.45, rely=0.35, relwidth=0.25, relheight=0.1)
        op_prot2 = Checkbutton(self.pag1, text='Atum', anchor='w')
        op_prot2.place(relx=0.45, rely=0.45, relwidth=0.3, relheight=0.1)
        op_prot3 = Checkbutton(self.pag1, text='Camarão', anchor='w')
        op_prot3.place(relx=0.45, rely=0.55, relwidth=0.25, relheight=0.1)
        op_prot4 = Checkbutton(self.pag1, text='Shitake', anchor='w')
        op_prot4.place(relx=0.45, rely=0.65, relwidth=0.25, relheight=0.1)

        pag2 = Button(self.pag1, text='>>>>', command=lambda:[self.poke_2()])
        pag2.place(relx=0.8, rely=0.85, relwidth=0.1, relheight=0.1)
    
    def poke_2(self):
        self.pag1.forget()
        self.pag2 = Frame(self.aba_poke)
        letra = font.Font(family='Arial', size= 20, weight='bold')
        letra2 = font.Font(family='Arial', size=12, weight='bold', slant='italic')
        letra3 = font.Font(family='Arial', size=10, weight='bold')
        self.pag2.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)
        self.make_it = []
        self.make1 = IntVar()
        self.make2 = IntVar()
        self.make3 = IntVar()
        self.make4 = IntVar()
        self.make5 = IntVar()
        self.make6 = IntVar()
        self.make7 = IntVar()
        self.make8 = IntVar()
        self.make9 = IntVar()
        self.make10 = IntVar()
        self.make11= IntVar()
        self.make12 = IntVar()
        def verifica(tamanho):
            if tamanho > 4:
                messagebox.showerror('MAKE IT incompleto', 'Escolha no máximo 4 opções do MAKE IT')
            if tamanho == 0:
                messagebox.showerror('MAKE IT incompleto', 'Escolha no minímo 1 opção do MAKE IT')
        def check_make():
            if self.make1.get() == 1:
                self.make_it.append(1)
            elif self.make2.get() == 1:
                self.make_it.append(2)
            elif self.make3.get() == 1:
                self.make_it.append(3)
            elif self.make4.get() == 1:
                self.make_it.append(4)
            elif self.make5.get() == 1:
                self.make_it.append(5)
            elif self.make6.get() == 1:
                self.make_it.append(6)
            elif self.make7.get() == 1:
                self.make_it.append(7)
            elif self.make8.get() == 1:
                self.make_it.append(8)
            elif self.make9.get() == 1:
                self.make_it.append(9)
            elif self.make10.get() == 1:
                self.make_it.append(10)
            elif self.make11.get() == 1:
                self.make_it.append(11)
            elif self.make12.get() == 1:
                self.make_it.append(12)
            print(self.make_it)
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
        letra3 = font.Font(family='Arial', size=10, weight='bold')
        self.pag3.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)
        self.crunch_it = IntVar(self.pag3)

        crunch = Label(self.pag3, text='3.CRUNCH IT', anchor='w')
        crunch.configure(font=letra)
        crunch.place(relx=0.02, rely=0.03, relwidth=0.35, relheight=0.1)
        escolha_crunch = Label(self.pag3, text='Escolha 1', foreground='white', anchor='w')
        escolha_crunch.configure(font=letra2)
        escolha_crunch.place(relx=0.02, rely=0.13, relwidth=0.22, relheight=0.1)

        op_crunch1 = Radiobutton(self.pag3, text='Chips de banana', anchor='w', value= 1,
        variable= self.crunch_it)
        op_crunch1.place(relx=0.02, rely=0.25, relwidth=0.25, relheight=0.1)
        op_crunch2 = Radiobutton(self.pag3, text='Chips de batata doce', anchor='w', value= 2,
        variable= self.crunch_it)
        op_crunch2.place(relx=0.02, rely=0.35, relwidth=0.3, relheight=0.1)
        op_crunch3 = Radiobutton(self.pag3, text='Kale', anchor='w', value= 3,
        variable= self.crunch_it)
        op_crunch3.place(relx=0.02, rely=0.45, relwidth=0.25, relheight=0.1)

        crunch = Label(self.pag3, text='4.TOP IT', anchor='w')
        crunch.configure(font=letra)
        crunch.place(relx=0.45, rely=0.03, relwidth=0.25, relheight=0.1)
        escolha_crunch = Label(self.pag3, text='Escolha 1', foreground='white', anchor='w')
        escolha_crunch.configure(font=letra2)
        escolha_crunch.place(relx=0.45, rely=0.13, relwidth=0.2, relheight=0.1)

        op_top1 = Radiobutton(self.pag3, text='Castanhas', anchor='w', value= 1)
        op_top1.place(relx=0.4, rely=0.25, relwidth=0.25, relheight=0.1)
        op_top2 = Radiobutton(self.pag3, text='Nozes', anchor='w', value= 2)
        op_top2.place(relx=0.7, rely=0.25, relwidth=0.3, relheight=0.1)
        op_top3 = Radiobutton(self.pag3, text='Pistache', anchor='w', value= 3)
        op_top3.place(relx=0.4, rely=0.35, relwidth=0.25, relheight=0.1)
        op_top4 = Radiobutton(self.pag3, text='Amendôas', anchor='w', value= 4)
        op_top4.place(relx=0.7, rely=0.35, relwidth=0.25, relheight=0.1)
        op_top5 = Radiobutton(self.pag3, text='Gergerlim negro', anchor='w', value= 5)
        op_top5.place(relx=0.4, rely=0.45, relwidth=0.3, relheight=0.1)
        op_top6 = Radiobutton(self.pag3, text='Lascas de coco', anchor='w', value= 6)
        op_top6.place(relx=0.7, rely=0.45, relwidth=0.25, relheight=0.1)
        op_top7 = Radiobutton(self.pag3, text='Semente de abóbora', anchor='w', value= 7)
        op_top7.place(relx=0.4, rely=0.55, relwidth=0.32, relheight=0.1)
        op_top8 = Radiobutton(self.pag3, text='Linhaça dourada', anchor='w', value= 8)
        op_top8.place(relx=0.4, rely=0.65, relwidth=0.3, relheight=0.1)

        pag3 = Button(self.pag3, text='>>>>', command=lambda:[self.poke_4()])
        pag3.place(relx=0.8, rely=0.85, relwidth=0.1, relheight=0.1)

    def poke_4(self):
        self.pag3.forget()
        self.pag4 = Frame(self.aba_poke)
        letra = font.Font(family='Arial', size= 20, weight='bold')
        letra2 = font.Font(family='Arial', size=12, weight='bold', slant='italic')
        letra3 = font.Font(family='Arial', size=10, weight='bold')
        self.pag4.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)
        self.finish_it = IntVar(self.pag4)

        finish = Label(self.pag4, text='4.FINISH IT', anchor='w')
        finish.configure(font=letra)
        finish.place(relx=0.45, rely=0.03, relwidth=0.25, relheight=0.1)
        escolha_finish = Label(self.pag4, text='Escolha 1', foreground='white', anchor='w')
        escolha_finish.configure(font=letra2)
        escolha_finish.place(relx=0.45, rely=0.13, relwidth=0.2, relheight=0.1)

        op_finish1 = Radiobutton(self.pag4, text='Shoyo clássico', anchor='w', value= 1,
        variable= self.finish_it)
        op_finish1.place(relx=0.4, rely=0.25, relwidth=0.25, relheight=0.1)
        op_finish2 = Radiobutton(self.pag4, text='Wasabi', anchor='w', value= 2,
        variable= self.finish_it)
        op_finish2.place(relx=0.7, rely=0.25, relwidth=0.3, relheight=0.1)
        op_finish3 = Radiobutton(self.pag4, text='Ponzu', anchor='w', value= 3,
        variable= self.finish_it)
        op_finish3.place(relx=0.4, rely=0.35, relwidth=0.25, relheight=0.1)
        op_finish4 = Radiobutton(self.pag4, text='Cream cheese', anchor='w', value= 4,
        variable= self.finish_it)
        op_finish4.place(relx=0.7, rely=0.35, relwidth=0.25, relheight=0.1)
        op_finish5 = Radiobutton(self.pag4, text='Tarê', anchor='w', value= 5,
        variable= self.finish_it)
        op_finish5.place(relx=0.4, rely=0.45, relwidth=0.3, relheight=0.1)
        op_finish6 = Radiobutton(self.pag4, text='Tarê de laranja', anchor='w', value= 6,
        variable= self.finish_it)
        op_finish6.place(relx=0.7, rely=0.45, relwidth=0.25, relheight=0.1)
        op_finish7 = Radiobutton(self.pag4, text='Mel com gengibre', anchor='w', value= 7,
        variable= self.finish_it)
        op_finish7.place(relx=0.4, rely=0.55, relwidth=0.32, relheight=0.1)
        op_finish8 = Radiobutton(self.pag4, text='Molho de pimenta com srirancha', anchor='w', value= 8,
        variable= self.finish_it)
        op_finish8.place(relx=0.4, rely=0.65, relwidth=0.3, relheight=0.1)
        op_finish9 = Radiobutton(self.pag4, text='Soyo de coco(+ R$3)', anchor='w', value= 9,
        variable= self.finish_it)
        op_finish9.place(relx=0.4, rely=0.75, relwidth=0.3, relheight=0.1)

        pag3 = Button(self.pag3, text='>>>>', command=lambda:[self.poke_4()])
        pag3.place(relx=0.8, rely=0.85, relwidth=0.1, relheight=0.1)

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