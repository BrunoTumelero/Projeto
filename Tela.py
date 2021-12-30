from tkinter import *
from tkinter import ttk
from datetime import *
from entregadoresv2 import *
from pedido import Pedido
from Cliente import Cliente 
from tela_cliente import tela_cardapio
from tkinter import messagebox
from PIL import Image, ImageTk
from janela_bairros import Tela_bairros

class Janela(Entregador, Pedido):
    def __init__(self, root, fundo, botoes_inicio):
        super().__init__()
        self.root = root
        self.fundo = fundo
        self.botoes_inicio = botoes_inicio
        self.root_entregas = root
        self.root_entregas.title('Restaurante')
        self.root_entregas.configure(background='snow')
        self.cria_tabela()
        self.menu()
        self.view()
        self.widgets()
        self.botoes()
        self.final_dia = []
        
        self.root_entregas.mainloop()

    def conectar(self):
        return super().conectar_func()

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
        self.my_menu = Menu(self.root_entregas)
        self.root_entregas.config(menu=self.my_menu)
        # Configurar menu
        self.my_menu.add_command(label='Inicio', command=lambda:[self.frame_tele.destroy(), self.elimina_caixa(),
        self.data_frame.destroy(), self.button_frame.destroy(), self.fundo, self.botoes_inicio,
        self.my_menu.destroy()])
        option_menu = Menu(self.my_menu, tearoff=0)
        self.my_menu.add_cascade(label="Opções", menu=option_menu)
        
        option_menu.add_command(label="Tabela bairros", command= lambda:[Tela_bairros(self.root_entregas)])
        option_menu.add_command(label="Funcionarios", command= lambda:[self.tela_cadastrar()])
        option_menu.add_command(label="Cardapio", command=lambda:[tela_cardapio(self.root,
        None, None, self.fundo, self.botoes_inicio), self.elimina_caixa(), self.frame_tele.destroy(), self.data_frame.destroy(),
        self.button_frame.destroy()])
        option_menu.add_separator()
        option_menu.add_command(label="Exit", command=self.root_entregas.quit)

        #Pesquisa Menu
        search_menu = Menu(self.my_menu, tearoff=0)
        self.my_menu.add_cascade(label="Fechamento", menu=search_menu)
        # opcoes pesquisa menu
        search_menu.add_command(label="Caixa", command=lambda:[self.caixa(), self.mostra_caixa()] )
        search_menu.add_command(label="Teles", command=lambda:[self.Fechar_teles(), self.valor_teles()])
        search_menu.add_command(label="Entregas", command=lambda:[self.data_frame.destroy(), self.button_frame.destroy(),
        self.view(), self.widgets(), self.botoes()])
#elimina dados do menu 2 para chamar o inicio da janela cardapio ficar correto 
    def elimina(self):
        try:
            self.frame_tele.destroy()
            self.resumo.destroy(), self.botoes_frame.destroy()
        except TypeError as e:
            print(e)
        
    def cria_tabela(self):
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
        self.frame_tele.configure(background='snow')

        # Criar Barra de rolagem Treeview
        tree_rolagem = Scrollbar(self.frame_tele)
        tree_rolagem.place(relx=0.92, rely=0.0, relwidth=0.02, relheight=1)

        # Criar Treeview
        self.tabela_entregas = ttk.Treeview(self.frame_tele, yscrollcommand=tree_rolagem.set,
                               selectmode="extended")
        self.tabela_entregas.place(relx=0.02, rely=0.0, relwidth=0.9, relheight=1)

        # Configurar a barra de rolagem
        tree_rolagem.config(command=self.tabela_entregas.yview)
#elimina dados da opcao caixa para o inicio ficar correto
    def elimina_caixa(self):
        try:
            self.caixa_frame.destroy()
        except AttributeError:
            pass

    def Fechar_teles(self):
        def novo_menu():
            self.my_menu.destroy()
            self.data_frame.destroy()
            self.button_frame.destroy()
            # Add Menu
            menu2 = Menu(self.root_entregas)
            self.root_entregas.config(menu=menu2)

            # Configurar menu
            # opcoes do menu
            menu2.add_command(label='Inicio', command=lambda:[self.frame_tele.destroy(), self.elimina_caixa(),
            self.resumo.destroy(), self.botoes_frame.destroy(), self.fundo, self.botoes_inicio, self.data_frame.destroy(),
            menu2.destroy()])
            option_menu = Menu(menu2, tearoff=0)
            menu2.add_cascade(label="Opções", menu=option_menu)
            
            option_menu.add_command(label="Tabela bairros", command= lambda:[Tela_bairros(self.root_entregas)])
            option_menu.add_command(label="Funcionarios", command= lambda:[self.tela_cadastrar()])
            option_menu.add_command(label="Cardapio", command=lambda:[tela_cardapio(self.root,
            None, None, self.fundo, self.botoes_inicio), self.elimina()])
            option_menu.add_separator()
            option_menu.add_command(label="Exit", command=self.root_entregas.quit)

            search_menu = Menu(menu2, tearoff=0)
            menu2.add_cascade(label="Fechamento", menu=search_menu)
            search_menu.add_command(label="Caixa", command=lambda:[self.caixa(), self.mostra_caixa()] )
            search_menu.add_command(label="Teles", command=lambda:[self.Fechar_teles(), self.valor_teles()])
            search_menu.add_command(label="Entregas", command=lambda:[self.resumo.destroy(), self.botoes_frame.destroy(),
            self.view(), self.widgets(), self.botoes(), self.menu(), menu2.destroy()])
        try:
            self.resumo.destroy()
            self.botoes_frame.destroy()
            novo_menu()
        except AttributeError:
            novo_menu()

    def tabela_teles(self):
        self.data_frame.destroy()
        self.button_frame.destroy()
        self.tabela_entregas.delete(*self.tabela_entregas.get_children())
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
        conn = self.conectar_func()
        c = conn.cursor()
        c.execute("""SELECT * FROM funcionarios""")
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
        self.data_pagamento = date.today()
        self.data_inicio = date.today() - timedelta(7)
        conn = self.conectar_func()
        c = conn.cursor()
        self.resumo = LabelFrame(self.root_entregas, text="Entregas da semana")
        self.resumo.place(relx=0.05, rely=0.58, relwidth=0.9, relheight=0.2)
        self.resumo.configure(background='snow')
        #botoes
        self.botoes_frame = LabelFrame(self.root_entregas)
        self.botoes_frame.place(relx=0.05, rely=0.8, relwidth=0.9, relheight=0.18)
        self.botoes_frame.configure(background='snow')
        c.execute("""SELECT nome_func FROM funcionarios""")
        l = [x for x in c.fetchall()]
        nomes = ttk.Combobox(self.resumo, values=l)
        nomes.place(relx=0.1, rely=0.15, relwidth=0.2, relheight=0.3)

        bt_finalizar = Image.open('Imagens/pagamento.png')
        img_finalizar = ImageTk.PhotoImage(bt_finalizar)
        finalizar_func = Button(self.botoes_frame, image= img_finalizar, compound= CENTER, relief=FLAT, background='snow',
        activebackground='lightblue', highlightbackground='snow',
        command=lambda:[finalizar(nomes.get())])
        finalizar_func.place(relx=0.45, rely=0.35, relwidth=0.1, relheight=0.55)
        finalizar_func.imagem = img_finalizar

        def finalizar(nomes):
            pagar = [0]
            conta_ifood = 0
            conta_watts = 0
            conn = self.conectar_pedido()
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
                        conect = Cliente.conectar_cliente()
                        conect.execute("""SELECT endereco FROM clientes WHERE nome_cliente = %s""",
                        (nome[0][0],))
                        end = conect.fetchall()
                        c.execute("""SELECT preco FROM bairros WHERE nome_bairro = %s""",
                        (end[0][0],))
                        valor = c.fetchall()
                        pagar.append(valor[0][0])
                        conta_watts += 1

            entregas_ifood = Label(self.resumo, text=f'Ifood: {conta_ifood}')
            entregas_ifood.configure(background='snow')
            entredas_watts = Label(self.resumo, text=f'Tele Wonder: {conta_watts}')
            entredas_watts.configure(background='snow')
            pagar_boy = Label(self.resumo, text=f'Pagar: {sum(pagar)}$')
            pagar_boy.configure(background='snow')
            entregas_ifood.place(relx=0.4, rely=0.15, relwidth=0.2, relheight=0.3),
            entredas_watts.place(relx=0.432, rely=0.4, relwidth=0.2, relheight=0.3),
            pagar_boy.place(relx=0.7, rely=0.15, relwidth=0.2, relheight=0.3)

        self.tabela_entregas.delete(*self.tabela_entregas.get_children())
        # Definir colunas
        self.tabela_entregas['columns'] = ("Data", "Nome", "Numero de entregas")
        # Formatar colunas
        self.tabela_entregas.column("#0", width=0, stretch=NO)
        self.tabela_entregas.column("Data", anchor=W, width=50)
        self.tabela_entregas.column("Nome", anchor=CENTER, width=150)
        self.tabela_entregas.column("Numero de entregas", anchor=CENTER, width=200)
        self.tabela_entregas.column("Data", anchor=CENTER, width=80)

        # Criar nome das colunas
        self.tabela_entregas.heading("#0", text="", anchor=W)
        self.tabela_entregas.heading("Data", text="Data", anchor=CENTER)
        self.tabela_entregas.heading("Nome", text="Nome", anchor=CENTER)
        self.tabela_entregas.heading("Numero de entregas", text="Numero de entregas", anchor=CENTER)


        # Criar as cores para mesclar
        self.tabela_entregas.tag_configure('oddrow', background="white")
        self.tabela_entregas.tag_configure('evenrow', background="lightblue")

        c.execute("""SELECT nome_func, COUNT(nome_func), dia 
        FROM pedidos WHERE dia > %s and dia <= %s
        GROUP BY dia, nome_func""", (self.data_inicio, self.data_pagamento))
        global count
        count = 0
        for func, tipo, day in c.fetchall():
            if count % 2 == 0:
                self.tabela_entregas.insert(parent='', index='0', text='',
                               values=(day, func, tipo),
                               tags=('evenrow',))
            else:
                self.tabela_entregas.insert(parent='', index='0', text='',
                               values=(day, func, tipo),
                               tags=('oddrow',))
            count += 1

        conn.close()
        self.tabela_entregas.bind('<Double-Button-1>', self.seleciona)

    def caixa(self):
        try:
            conn = self.conectar_pedido()
            c = conn.cursor()
            data = datetime.now()
            data = data.strftime("%Y/%m/%d")
            c.execute("""SELECT valor_total FROM pedidos WHERE dia = %s""", (data,))
            for x in c.fetchall():
                self.dinheiro = 0
                self.dinheiro += x[0]
            conn.close()
        except AttributeError:
            erro = messagebox.showwarning('Caixa', 'Numa venda realizada hoje')
            erro
            
    def mostra_caixa(self):
        try:
            self.elimina_caixa()
            self.data_frame.destroy()
            dia = datetime.now()
            dia_caixa = dia.strftime("%d/%m")
            self.caixa_frame = LabelFrame(self.root_entregas, text=f"Caixa dia: {dia_caixa}")
            self.caixa_frame.place(relx=0.05, rely=0.58, relwidth=0.9, relheight=0.2)
            self.caixa_frame.configure(background='snow')

            caixa_total = Label(self.caixa_frame, text=f'Valor total: {self.dinheiro}$')
            caixa_total.place(relx=0.15, rely=0.3, relwidth=0.3, relheight=0.4)
            caixa_total.configure(font=('Helvetica', 20), background='snow')
        except AttributeError:
            info_caixa = messagebox.showwarning('Caixa', 'Numa venda realizada hoje')
            if info_caixa == 'ok':
                self.caixa_frame.destroy()
                self.view()
                self.widgets()
            else:
                info_caixa

    def view(self):
        self.tabela_entregas.delete(*self.tabela_entregas.get_children())
        # Definir colunas
        self.tabela_entregas['columns'] = ("Id", "Nome", "Bairro", "Boy", "Data")

        # Formatar colunas
        self.tabela_entregas.column("#0", width=0, stretch=NO)
        self.tabela_entregas.column("Id", anchor=W, width=50)
        self.tabela_entregas.column("Nome", anchor=W, width=250)
        self.tabela_entregas.column("Bairro", anchor=W, width=140)
        self.tabela_entregas.column("Boy", anchor=CENTER, width=90)
        self.tabela_entregas.column("Data", anchor=CENTER, width=100)


        # Criar nome das colunas
        self.tabela_entregas.heading("#0", text="", anchor=W)
        self.tabela_entregas.heading("Id", text="Id", anchor=CENTER)
        self.tabela_entregas.heading("Nome", text="Nome", anchor=CENTER)
        self.tabela_entregas.heading("Bairro", text="Bairro", anchor=CENTER)
        self.tabela_entregas.heading("Boy", text="Boy", anchor=CENTER)
        self.tabela_entregas.heading("Data", text="Data", anchor=CENTER)

        # Criar as cores para mesclar
        self.tabela_entregas.tag_configure('oddrow', background="white")
        self.tabela_entregas.tag_configure('evenrow', background="lightblue")

        #Add dados na tela
        conn = self.conectar_pedido() 
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
                self.tabela_entregas.insert(parent='', index='0', text='',
                               values=(idd, nome , end, boy, data),
                               tags=('evenrow',))
            else:
                self.tabela_entregas.insert(parent='', index='0', text='',
                               values=(idd, nome, end, boy, data),
                               tags=('oddrow',))
            count += 1

        conn.close()
        self.tabela_entregas.bind('<Double-Button-1>', self.seleciona)

    def seleciona(self, event):
        self.limpa(self.nome_entry, self.bairro_entry, self.boy_entry)
        for x in self.tabela_entregas.selection():
            self.idp, n, e, boy, data  = self.tabela_entregas.item(x, 'values')
            self.nome_entry.insert(END, n)
            self.bairro_entry.insert(END, e)
            self.boy_entry.insert(END, boy)
        return self.nome_entry.get()

    def rusultado_consulta(self, nome, local, boy):
        conn = self.conectar_pedido()
        c = conn.cursor()

        self.tabela_entregas.delete(*self.tabela_entregas.get_children())
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
                    self.tabela_entregas.insert(parent='', index='0', text='',
                                values=(idd, nome , end, entregador, data),
                                tags=('evenrow',))
                else:
                    self.tabela_entregas.insert(parent='', index='0', text='',
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
                    self.tabela_entregas.insert(parent='', index='0', text='',
                                values=(idd, nome , end, entregador, data),
                                tags=('evenrow',))
                else:
                    self.tabela_entregas.insert(parent='', index='0', text='',
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
                    self.tabela_entregas.insert(parent='', index='0', text='',
                                values=(idd, nome , end, entregador, data),
                                tags=('evenrow',))
                else:
                    self.tabela_entregas.insert(parent='', index='0', text='',
                                values=(idd, nome, end, entregador, data),
                                tags=('oddrow',))
                count += 1
        conn.close()

    def widgets(self):
        # Add Dados Entry Boxes
        self.data_frame = LabelFrame(self.root_entregas, text="Dados")
        self.data_frame.place(relx=0.05, rely=0.58, relwidth=0.9, relheight=0.2)
        self.data_frame.configure(background='snow')

        nome_label = Label(self.data_frame, text="Nome")
        nome_label.place(relx=0.0, rely=0.15, relwidth=0.1, relheight=0.15)
        nome_label.configure(background='snow')
        self.nome_entry = Entry(self.data_frame, relief=FLAT)
        self.nome_entry.place(relx=0.1, rely=0.1, relwidth=0.3, relheight=0.3)

        bairro_label = Label(self.data_frame, text="Bairro")
        bairro_label.place(relx=0.45, rely=0.15, relwidth=0.1, relheight=0.15)
        bairro_label.configure(background='snow')
        self.bairro_entry = Entry(self.data_frame, relief=FLAT)
        self.bairro_entry.place(relx=0.55, rely=0.1, relwidth=0.3, relheight=0.3)
        
        boy_label = Label(self.data_frame, text="Boy")
        boy_label.place(relx=0.12, rely=0.5, relwidth=0.3, relheight=0.3)
        boy_label.configure(background='snow')
        self.boy_entry = Entry(self.data_frame, relief=FLAT)
        self.boy_entry.place(relx=0.32, rely=0.5, relwidth=0.3, relheight=0.3)

    def atualiza_tabela(self):
        self.tabela_entregas.delete(*self.tabela_entregas.get_children())
        conn = self.conectar_pedido() 
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
                self.tabela_entregas.insert(parent='', index='0', text='',
                               values=(idd, nome , end, boy, data),
                               tags=('evenrow',))
            else:
                self.tabela_entregas.insert(parent='', index='0', text='',
                               values=(idd, nome, end, boy, data),
                               tags=('oddrow',))
            count += 1

        conn.close()

    def atualiza_pedido(self, alter):
        conn = self.conectar_pedido()
        c = conn.cursor()
        c.execute("""SELECT Id_pedido, pe.nome_cliente,
                cl.endereco, 
                nome_func, dia
                FROM pedidos as pe
                join clientes as cl on cl.nome_cliente = pe.nome_cliente
                ORDER BY dia""")
        for idd, nome_cl, end_cl, func, day in c.fetchall():
            pass
        
        if alter != func[0][0]:
            c.execute("""SELECT nome_func, nome_cliente, tipo_tele FROM pedidos 
            WHERE nome_cliente = %s""", (nome_cl,))
            for boy1, nome, tipo in c.fetchall():
                print(boy1, tipo)
            c.execute("""SELECT endereco FROM clientes WHERE nome_cliente = %s""", (nome_cl,))
            endereco = c.fetchall()
            if tipo == 2:
                c.execute("""SELECT preco FROM bairros WHERE nome_bairro = %s""", (endereco[0][0],))
                valor = c.fetchall()
                desconta = -valor[0][0]
            elif tipo == 1:
                desconta = -10
            else:
                print('tipo errado')

            c.execute("""UPDATE pedidos SET nome_func = %s WHERE nome_cliente = %s
            AND dia = %s""", (alter, nome_cl, day))
            c.execute("""UPDATE funcionarios SET pagar = %s WHERE nome_func = %s""", 
            (desconta, boy1))

            conn.commit()
            conn.close()

    def botoes(self):
        bt1 = Image.open('Imagens/lixo.ico')
        img = ImageTk.PhotoImage(bt1)
        bt2 = Image.open('Imagens/atualizar.png')
        img2 = ImageTk.PhotoImage(bt2)
        bt3 = Image.open('Imagens/consultar.ico')
        img3 = ImageTk.PhotoImage(bt3)
        # Add Buttons
        self.button_frame = Frame(self.root_entregas)
        self.button_frame.place(relx=0.05, rely=0.8, relwidth=0.9, relheight=0.18)
        self.button_frame.configure(background='snow')
        #consultar
        consultar_button = Button(self.button_frame, image= img3, compound=CENTER, relief=FLAT,
        activebackground='lightblue', highlightbackground='snow', command= lambda: [self.rusultado_consulta(self.nome_entry.get(),
        self.bairro_entry.get(), self.boy_entry.get())])
        consultar_button.place(relx=0.13, rely=0.1, relwidth=0.1, relheight=0.55)
        consultar_button.configure(background='snow')
        consultar_button.imagem = img3
        #atualizar
        atualizar_button = Button(self.button_frame, image= img2, compound=CENTER, relief=FLAT,
        activebackground='lightblue', highlightbackground='snow', command= lambda:[
        self.atualiza_pedido(self.boy_entry.get()), self.atualiza_tabela()])
        atualizar_button.place(relx=0.43, rely=0.1, relwidth=0.1, relheight=0.55)
        atualizar_button.configure(background='snow')
        atualizar_button. imagem = img2
        #apagar
        apagar = Button(self.button_frame, image= img, compound=CENTER, relief=FLAT,
        activebackground='lightblue', highlightbackground='snow', command= lambda:[self.apagar(self.idp),
        self.limpa(self.nome_entry, self.bairro_entry, self.boy_entry), self.atualiza_tabela()])
        apagar.place(relx=0.73, rely=0.1, relwidth=0.1, relheight=0.55)
        apagar.configure(background='snow')
        apagar.imagem = img

    def tela_cadastrar(self):
        self.tela = Toplevel(self.root_entregas)
        self.tela.geometry('400x100')
        self.tela.maxsize(400, 100)
        self.tela.title('Cadastrar - Funcionario')
        self.tela.configure(background='snow')

        #Entradas
        self.lb_nome = Label(self.tela, text='Nome')
        self.lb_nome.configure(background='snow')
        self.en_nome = Entry(self.tela)
        self.en_nome.focus()
        self.lb_nome.pack()
        self.en_nome.pack()
        #botao
        self.bt_cadastra = Button(self.tela, text='Cadastrar', background='snow', relief=FLAT, activebackground='snow',
		highlightbackground='snow', activeforeground='green', command=lambda:[self.cadastrar(self.en_nome.get().title()),
        self.en_nome.delete(0, 'end')])
        self.bt_cadastra.place(relx=0.2, rely=0.5, relwidth=0.2, relheight=0.3)
        self.bt_excluir = Button(self.tela, text='Excluir', background='snow', relief=FLAT, activebackground='snow',
		highlightbackground='snow', activeforeground='red', command=lambda:[self.apagar_func(self.en_nome.get().title()),
        self.en_nome.delete(0, 'end')])
        self.bt_excluir.place(relx=0.6, rely=0.5, relwidth=0.2, relheight=0.3)
