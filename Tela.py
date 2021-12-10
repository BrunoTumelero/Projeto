from tkinter import *
from tkinter import ttk
from datetime import *
import tkinter
from entregadoresv2 import *
from pedido import Pedido
from tela_cliente import tela_cardapio
from tkinter import messagebox
from PIL import Image, ImageTk
from janela_bairros import Tela_bairros

class Janela(Entregador, Pedido):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root_entregas = Toplevel(root)
        self.root_entregas.title('Restaurante')
        self.root_entregas.geometry('800x500')
        self.menu()
        self.view()
        self.widgets()
        self.botoes()
        self.final_dia = []
        
        self.root_entregas.mainloop()

    def conectar(self):
        return super().conectar()

    def cadastrar(self, nome):
        return super().cadastrar(nome)

    def apagar_func(self, nome):
        return super().apagar_func(nome)

    def apagar(self, id_pedido):
        return super().apagar(id_pedido)

    def add_tele(self, nome):
        return super().add_tele(nome)

    def consultar(self, nome, end, boy):
        return super().consultar(nome, end, boy)

    def limpa(self, nome, endereco, boy):
        return super().limpa(nome, endereco, boy)

    def menu(self):
        # Add Menu
        my_menu = Menu(self.root_entregas)
        self.root_entregas.config(menu=my_menu)

        # Configurar menu
        # opcoes do menu
        option_menu = Menu(my_menu, tearoff=0)
        my_menu.add_cascade(label="Opções", menu=option_menu)
        
        option_menu.add_command(label="Tabela bairros", command= lambda:[Tela_bairros()])
        option_menu.add_command(label="Funcionarios", command= lambda:[self.tela_cadastrar()])
        option_menu.add_command(label="Cardapio", command=lambda:[tela_cardapio(self.root,
        self.root_entregas, None, None)])
        option_menu.add_separator()
        option_menu.add_command(label="Exit", command=self.root_entregas.quit)

        #Pesquisa Menu
        search_menu = Menu(my_menu, tearoff=0)
        my_menu.add_cascade(label="Fechamento", menu=search_menu)
        # opcoes pesquisa menu
        search_menu.add_command(label="Caixa", command=lambda:[self.caixa(), self.mostra_caixa()] )
        search_menu.add_command(label="Teles", command=lambda:[self.Fechar_teles(), self.valor_teles()])
        search_menu.add_separator()
        search_menu.add_command(label="Entregas", command=lambda:[self.view(), self.widgets(),
        self.botoes()])

    def Fechar_teles(self):
        self.tree_frame.forget()
        conn = self.conectar()
        c = conn.cursor()
        c.execute("""SELECT * FROM funcionarios""")
        # Add Style
        style = ttk.Style()

        # Pegar Tema
        style.theme_use('classic')

        # Configurar as cores da Treeview
        style.configure("Treeview",
                background="#D3D3D3",
                foreground="black",
                rowheight=25,
                fieldbackground="#D3D3D3")
        
        # Change Selected Color
        style.map('Treeview',
                background=[('selected', "#347083")])
        # Criar Treeview Frame
        self.frame_tele = Frame(self.root_entregas)
        self.frame_tele.place(relx=0.08, rely=0.02, relwidth=0.9, relheight=0.5)

        # Criar Barra de rolagem Treeview
        tree_rolagem = Scrollbar(self.frame_tele)
        tree_rolagem.place(relx=0.92, rely=0.0, relwidth=0.02, relheight=1)

        # Criar Treeview
        self.tabela_entregas = ttk.Treeview(self.frame_tele, yscrollcommand=tree_rolagem.set,
                               selectmode="extended")
        self.tabela_entregas.place(relx=0.02, rely=0.0, relwidth=0.9, relheight=1)

        # Configurar a barra de rolagem
        tree_rolagem.config(command=self.tabela_entregas.yview)

        # Definir colunas
        self.tabela_entregas['columns'] = ("Id", "Nome", "Numero de entregas", "Pagar")

        # Formatar colunas
        self.tabela_entregas.column("#0", width=0, stretch=NO)
        self.tabela_entregas.column("Id", anchor=W, width=5)
        self.tabela_entregas.column("Nome", anchor=CENTER, width=150)
        self.tabela_entregas.column("Numero de entregas", anchor=CENTER, width=200)
        self.tabela_entregas.column("Pagar", anchor=CENTER, width=150)

        # Criar nome das colunas
        self.tabela_entregas.heading("#0", text="", anchor=W)
        self.tabela_entregas.heading("Id", text="Id", anchor=CENTER)
        self.tabela_entregas.heading("Nome", text="Nome", anchor=CENTER)
        self.tabela_entregas.heading("Numero de entregas", text="Numero de entregas", anchor=CENTER)
        self.tabela_entregas.heading("Pagar", text="Pagar", anchor=CENTER)

        # Criar as cores para mesclar
        self.tabela_entregas.tag_configure('oddrow', background="white")
        self.tabela_entregas.tag_configure('evenrow', background="lightblue")
        global count
        count = 0
        for i, func, teles, pagar in c.fetchall():
            if count % 2 == 0:
                self.tabela_entregas.insert(parent='', index='0', text='',
                               values=(i, func, teles, (pagar, '$')),
                               tags=('evenrow',))
            else:
                self.tabela_entregas.insert(parent='', index='0', text='',
                               values=(i, func, teles, (pagar, '$')),
                               tags=('oddrow',))
            count += 1

        conn.close()
        self.tabela_entregas.bind('<Double-Button-1>', self.seleciona)

    def valor_teles(self):
        self.button_frame.forget()
        self.data_frame.forget()
        self.tabela_entregas.forget()
        self.data_pagamento = date.today()
        self.data_inicio = date.today() - timedelta(7)
        conn = self.conectar()
        c = conn.cursor()
        self.resumo = LabelFrame(self.root_entregas, text="Entregas da semana")
        self.resumo.place(relx=0.05, rely=0.58, relwidth=0.9, relheight=0.2)
        #botoes
        botoes_frame = LabelFrame(self.root_entregas)
        botoes_frame.place(relx=0.05, rely=0.8, relwidth=0.9, relheight=0.18)
        c.execute("""SELECT nome_func FROM funcionarios""")
        l = [x for x in c.fetchall()]
        nomes = ttk.Combobox(self.resumo, values=l)
        nomes.place(relx=0.1, rely=0.15, relwidth=0.2, relheight=0.3)

        bt_finalizar = Image.open('Imagens/pagamento.png')
        img_finalizar = ImageTk.PhotoImage(bt_finalizar)
        finalizar_func = Button(botoes_frame, image= img_finalizar, compound= CENTER,
        command=lambda:[finalizar(nomes.get())])
        finalizar_func.place(relx=0.45, rely=0.35, relwidth=0.1, relheight=0.55)
        finalizar_func.imagem = img_finalizar

        def finalizar(nomes):
            pagar = [0]
            conta_ifood = 0
            conta_watts = 0
            conn = self.conectar()
            c = conn.cursor()
            c.execute("""SELECT id_pedido, nome_func, tipo_tele, dia 
            FROM pedidos WHERE dia > %s and dia <= %s""", (self.data_inicio, self.data_pagamento))
            for idd, func, tipo, day in c.fetchall():
                if func == nomes:
                    if tipo == 1:
                        pagar.append(10)
                        conta_ifood += 1
                    if tipo == 2:
                        c.execute("""SELECT nome_cliente FROM pedidos WHERE id_pedido= %s""",
                        (idd,))
                        nome = c.fetchall()
                        c.execute("""SELECT endereco FROM clientes WHERE nome_cliente = %s""",
                        (nome[0][0],))
                        end = c.fetchall()
                        c.execute("""SELECT preco FROM bairros WHERE nome_bairro = %s""",
                        (end[0][0],))
                        valor = c.fetchall()
                        pagar.append(valor[0][0])
                        conta_watts += 1

            entregas_ifood = Label(self.resumo, text=f'Ifood: {conta_ifood}')
            entredas_watts = Label(self.resumo, text=f'Tele Wonder: {conta_watts}')
            pagar_boy = Label(self.resumo, text=f'Pagar: {sum(pagar)}$')
            entregas_ifood.place(relx=0.4, rely=0.15, relwidth=0.2, relheight=0.3),
            entredas_watts.place(relx=0.432, rely=0.4, relwidth=0.2, relheight=0.3),
            pagar_boy.place(relx=0.7, rely=0.15, relwidth=0.2, relheight=0.3)
        
        # Add Style
        style = ttk.Style()

        # Pegar Tema
        style.theme_use('classic')

        # Configurar as cores da Treeview
        style.configure("Treeview",
                background="#D3D3D3",
                foreground="black",
                rowheight=25,
                fieldbackground="#D3D3D3")
        
        # Change Selected Color
        style.map('Treeview', background=[('selected', "#347083")])
        # Criar Treeview Frame
        self.frame_tele = Frame(self.root_entregas)
        self.frame_tele.place(relx=0.08, rely=0.02, relwidth=0.9, relheight=0.5)

        # Criar Barra de rolagem Treeview
        tree_rolagem = Scrollbar(self.frame_tele)
        tree_rolagem.place(relx=0.92, rely=0.0, relwidth=0.02, relheight=1)

        # Criar Treeview
        self.tabela_teles = ttk.Treeview(self.frame_tele, yscrollcommand=tree_rolagem.set,
                               selectmode="extended")
        self.tabela_teles.place(relx=0.02, rely=0.0, relwidth=0.9, relheight=1)

        # Configurar a barra de rolagem
        tree_rolagem.config(command=self.tabela_teles.yview)

        # Definir colunas
        self.tabela_teles['columns'] = ("Data", "Nome", "Numero de entregas")

        # Formatar colunas
        self.tabela_teles.column("#0", width=0, stretch=NO)
        self.tabela_teles.column("Data", anchor=W, width=50)
        self.tabela_teles.column("Nome", anchor=CENTER, width=150)
        self.tabela_teles.column("Numero de entregas", anchor=CENTER, width=200)
        self.tabela_teles.column("Data", anchor=CENTER, width=80)

        # Criar nome das colunas
        self.tabela_teles.heading("#0", text="", anchor=W)
        self.tabela_teles.heading("Data", text="Data", anchor=CENTER)
        self.tabela_teles.heading("Nome", text="Nome", anchor=CENTER)
        self.tabela_teles.heading("Numero de entregas", text="Numero de entregas", anchor=CENTER)


        # Criar as cores para mesclar
        self.tabela_teles.tag_configure('oddrow', background="white")
        self.tabela_teles.tag_configure('evenrow', background="lightblue")

        c.execute("""SELECT nome_func, COUNT(nome_func), dia 
        FROM pedidos WHERE dia > %s and dia <= %s
        GROUP BY dia, nome_func""", (self.data_inicio, self.data_pagamento))
        global count
        count = 0
        for func, tipo, day in c.fetchall():
            if count % 2 == 0:
                self.tabela_teles.insert(parent='', index='0', text='',
                               values=(day, func, tipo),
                               tags=('evenrow',))
            else:
                self.tabela_teles.insert(parent='', index='0', text='',
                               values=(day, func, tipo),
                               tags=('oddrow',))
            count += 1

        conn.close()
        self.tabela_teles.bind('<Double-Button-1>', self.seleciona)

    def caixa(self):
        try:
            conn = self.conectar()
            c = conn.cursor()
            data = datetime.now()
            data = data.strftime("%Y/%m/%d")
            c.execute("""SELECT valor_total FROM pedidos WHERE dia = %s""", (data,))
            for x in c.fetchall():
                self.final_dia.append(x[0])
                self.dinheiro =  sum(self.final_dia)
            conn.close()
        except AttributeError:
            erro = messagebox.showwarning('Caixa', 'Numa venda realizada hoje')
            erro
            self.root_entregas.lower()
        
    def mostra_caixa(self):
        try:
            self.data_frame.forget()
            dia = datetime.now()
            dia_caixa = dia.strftime("%d/%m")
            caixa = LabelFrame(self.root_entregas, text=f"Caixa dia: {dia_caixa}")
            caixa.place(relx=0.05, rely=0.58, relwidth=0.9, relheight=0.2)

            caixa_total = Label(caixa, text=f'Valor total: {self.dinheiro}$')
            caixa_total.place(relx=0.15, rely=0.3, relwidth=0.3, relheight=0.4)
            caixa_total.configure(font=('Helvetica', 20))
        except AttributeError:
            info_caixa = messagebox.showwarning('Caixa', 'Numa venda realizada hoje')
            if info_caixa == 'ok':
                self.view()
                self.widgets()
            else:
                info_caixa

    def view(self):
        # Add Style
        style = ttk.Style()

        # Pegar Tema
        style.theme_use('default')

        # Configurar as cores da Treeview
        style.configure("Treeview",
                background="#D3D3D3",
                foreground="black",
                rowheight=25,
                fieldbackground="#D3D3D3")
        
        # Change Selected Color
        style.map('Treeview',
                background=[('selected', "#347083")])
        # Criar Treeview Frame
        self.tree_frame = Frame(self.root_entregas)
        self.tree_frame.place(relx=0.08, rely=0.02, relwidth=0.9, relheight=0.5)

        # Criar Barra de rolagem Treeview
        tree_scroll = Scrollbar(self.tree_frame)
        tree_scroll.place(relx=0.92, rely=0.0, relwidth=0.02, relheight=1)

        # Criar Treeview
        self.lista = ttk.Treeview(self.tree_frame, yscrollcommand=tree_scroll.set,
                               selectmode="extended")
        self.lista.place(relx=0.02, rely=0.0, relwidth=0.9, relheight=1)

        # Configurar a barra de rolagem
        tree_scroll.config(command=self.lista.yview)

        # Definir colunas
        self.lista['columns'] = ("Id", "Nome", "Bairro", "Boy", "Data")

        # Formatar colunas
        self.lista.column("#0", width=0, stretch=NO)
        self.lista.column("Id", anchor=W, width=50)
        self.lista.column("Nome", anchor=W, width=250)
        self.lista.column("Bairro", anchor=W, width=140)
        self.lista.column("Boy", anchor=CENTER, width=90)
        self.lista.column("Data", anchor=CENTER, width=100)


        # Criar nome das colunas
        self.lista.heading("#0", text="", anchor=W)
        self.lista.heading("Id", text="Id", anchor=CENTER)
        self.lista.heading("Nome", text="Nome", anchor=CENTER)
        self.lista.heading("Bairro", text="Bairro", anchor=CENTER)
        self.lista.heading("Boy", text="Boy", anchor=CENTER)
        self.lista.heading("Data", text="Data", anchor=CENTER)

        # Criar as cores para mesclar
        self.lista.tag_configure('oddrow', background="white")
        self.lista.tag_configure('evenrow', background="lightblue")

        self.conectar()
        #Add dados na tela
        conn = self.conectar() 
        c = conn.cursor()
        c.execute("""SELECT Id_pedido, pe.nome_cliente,
                cl.endereco, 
                nome_func, dia
                FROM pedidos as pe
                join clientes as cl on cl.nome_cliente = pe.nome_cliente
                ORDER BY dia""")

        global count
        count = 0
        for idd, nome , end, boy, data in c.fetchall():
            if count % 2 == 0:
                self.lista.insert(parent='', index='0', text='',
                               values=(idd, nome , end, boy, data),
                               tags=('evenrow',))
            else:
                self.lista.insert(parent='', index='0', text='',
                               values=(idd, nome, end, boy, data),
                               tags=('oddrow',))
            count += 1

        conn.close()
        self.lista.bind('<Double-Button-1>', self.seleciona)

    def seleciona(self, event):
        self.limpa(self.nome_entry, self.bairro_entry, self.boy_entry)
        for x in self.lista.selection():
            self.idp, n, e, boy, data  = self.lista.item(x, 'values')
            self.nome_entry.insert(END, n)
            self.bairro_entry.insert(END, e)
            self.boy_entry.insert(END, boy)
        return self.nome_entry.get()

    def rusultado_consulta(self, nome, local, boy):
        conn = self.conectar()
        c = conn.cursor()

        self.lista.delete(*self.lista.get_children())
        global count
        count = 0
        if len(nome) > 0:
            nome_p = f'%{nome}%'.title()
            c.execute("""SELECT Id_pedido, pe.nome_cliente,
                    cl.endereco, 
                    nome_func, dia
                    FROM pedidos as pe
                    join clientes as cl on cl.nome_cliente = pe.nome_cliente
                    WHERE pe.nome_cliente LIKE %s ORDER BY pe.nome_cliente
                    """, (nome_p,))
            for idd, nome , end, entregador, data in c.fetchall():
                if count % 2 == 0:
                    self.lista.insert(parent='', index='0', text='',
                                values=(idd, nome , end, entregador, data),
                                tags=('evenrow',))
                else:
                    self.lista.insert(parent='', index='0', text='',
                                values=(idd, nome, end, entregador, data),
                                tags=('oddrow',))
                count += 1
        elif len(local) > 0:
            local = f'{local}%'.title()
            c.execute("""SELECT Id_pedido, pe.nome_cliente,
                    cl.endereco, 
                    nome_func, dia
                    FROM pedidos as pe
                    join clientes as cl on cl.nome_cliente = pe.nome_cliente
                    WHERE cl.endereco LIKE %s ORDER BY cl.endereco
                    """, (local,))
            for idd, nome , end, entregador, data in c.fetchall():
                if count % 2 == 0:
                    self.lista.insert(parent='', index='0', text='',
                                values=(idd, nome , end, entregador, data),
                                tags=('evenrow',))
                else:
                    self.lista.insert(parent='', index='0', text='',
                                values=(idd, nome, end, entregador, data),
                                tags=('oddrow',))
                count += 1
        elif len(boy) > 0:
            boy =f'%{boy}%'.title()
            c.execute("""SELECT Id_pedido, pe.nome_cliente,
                    cl.endereco, 
                    nome_func, dia
                    FROM pedidos as pe
                    join clientes as cl on cl.nome_cliente = pe.nome_cliente
                    WHERE nome_func LIKE %s ORDER BY dia
                    """, (boy,))
            for idd, nome , end, entregador, data in c.fetchall():
                if count % 2 == 0:
                    self.lista.insert(parent='', index='0', text='',
                                values=(idd, nome , end, entregador, data),
                                tags=('evenrow',))
                else:
                    self.lista.insert(parent='', index='0', text='',
                                values=(idd, nome, end, entregador, data),
                                tags=('oddrow',))
                count += 1
        conn.close()

    def widgets(self):
        # Add Dados Entry Boxes
        self.data_frame = LabelFrame(self.root_entregas, text="Dados")
        self.data_frame.place(relx=0.05, rely=0.58, relwidth=0.9, relheight=0.2)

        nome_label = Label(self.data_frame, text="Nome")
        nome_label.place(relx=0.0, rely=0.15, relwidth=0.1, relheight=0.15)
        self.nome_entry = Entry(self.data_frame)
        self.nome_entry.place(relx=0.1, rely=0.1, relwidth=0.3, relheight=0.3)

        bairro_label = Label(self.data_frame, text="Bairro")
        bairro_label.place(relx=0.45, rely=0.15, relwidth=0.1, relheight=0.15)
        self.bairro_entry = Entry(self.data_frame)
        self.bairro_entry.place(relx=0.55, rely=0.1, relwidth=0.3, relheight=0.3)
        
        boy_label = Label(self.data_frame, text="Boy")
        boy_label.place(relx=0.12, rely=0.5, relwidth=0.3, relheight=0.3)
        self.boy_entry = Entry(self.data_frame)
        self.boy_entry.place(relx=0.32, rely=0.5, relwidth=0.3, relheight=0.3)

    def atualiza_tabela(self):
        self.lista.delete(*self.lista.get_children())
        conn = self.conectar() 
        c = conn.cursor()
        c.execute("""SELECT Id_pedido, pe.nome_cliente,
                cl.endereco, 
                nome_func, dia
                FROM pedidos as pe
                join clientes as cl on cl.nome_cliente = pe.nome_cliente
                ORDER BY dia""")

        global count
        count = 0
        for idd, nome , end, boy, data in c.fetchall():
            if count % 2 == 0:
                self.lista.insert(parent='', index='0', text='',
                               values=(idd, nome , end, boy, data),
                               tags=('evenrow',))
            else:
                self.lista.insert(parent='', index='0', text='',
                               values=(idd, nome, end, boy, data),
                               tags=('oddrow',))
            count += 1

        conn.close()

    def botoes(self):
        bt1 = Image.open('Imagens/lixo.ico')
        img = ImageTk.PhotoImage(bt1)
        bt2 = Image.open('Imagens/atualizar.png')
        img2 = ImageTk.PhotoImage(bt2)
        bt3 = Image.open('Imagens/consultar.ico')
        img3 = ImageTk.PhotoImage(bt3)
        # Add Buttons
        self.button_frame = LabelFrame(self.root_entregas, text="Comandos")
        self.button_frame.place(relx=0.05, rely=0.8, relwidth=0.9, relheight=0.18)
        #consultar
        consultar_button = Button(self.button_frame, image= img3, compound=CENTER,
        command= lambda: [self.rusultado_consulta(self.nome_entry.get(),
        self.bairro_entry.get(), self.boy_entry.get())])
        consultar_button.place(relx=0.13, rely=0.1, relwidth=0.1, relheight=0.55)
        consultar_button.imagem = img3
        #atualizar
        atualizar_button = Button(self.button_frame, image= img2, compound=CENTER, command= lambda:[
        self.atualiza_tabela()])
        atualizar_button.place(relx=0.43, rely=0.1, relwidth=0.1, relheight=0.55)
        atualizar_button. imagem = img2
        #apagar
        apagar = Button(self.button_frame, image= img, compound=CENTER,
        command= lambda:[self.apagar(self.idp),
        self.limpa(self.nome_entry, self.bairro_entry, self.boy_entry), self.atualiza_tabela()])
        apagar.place(relx=0.73, rely=0.1, relwidth=0.1, relheight=0.55)
        apagar.imagem = img

    def tela_cadastrar(self):
        self.tela = Toplevel(self.root_entregas)
        self.tela.geometry('400x100')
        self.tela.maxsize(400, 100)
        self.tela.title('Cadastrar - Funcionario')

        #Entradas
        self.lb_nome = Label(self.tela, text='Nome')
        self.en_nome = Entry(self.tela)
        self.lb_nome.pack()
        self.en_nome.pack()
        #botao
        self.bt_cadastra = Button(self.tela, text='Cadastrar', 
        command=lambda:[self.cadastrar(self.en_nome.get().title()),
        self.en_nome.delete(0, 'end')])
        self.bt_cadastra.place(relx=0.2, rely=0.5, relwidth=0.2, relheight=0.3)
        self.bt_excluir = Button(self.tela, text='Excluir', 
        command=lambda:[self.apagar_func(self.en_nome.get().title()),
        self.en_nome.delete(0, 'end')])
        self.bt_excluir.place(relx=0.6, rely=0.5, relwidth=0.2, relheight=0.3)

#j = Janela()
#j