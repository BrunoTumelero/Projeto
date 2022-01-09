from tkinter import *
from tkinter import ttk
from tkinter import font
from PIL import Image, ImageTk
from cardapio_v2 import Cardapio, Modelo_prato
from pedido import *
from bairrosv2 import Local
from personalize import Make_dish
import json

class conf_cardapio(Cardapio, Pedido, Local):
    def __init__(self, root, info_cliente, end_cliente, fundo, botoes_inicio):
        super().__init__()
        self.root_cardapio = root
        self.root_cardapio.title('Cardapio')
        self.root_cardapio.configure(background='snow')
        self.fundo_inicio = fundo
        self.inicio_botoes = botoes_inicio
        self.cria_menu()
        self.menu_geral()
        self.opcoes()
        self.acessorios()
        self.info_cliente = info_cliente
        self.end_cliente = end_cliente
        self.modelo = Modelo_prato()
        self.lista_cat = []
                
    def conectar_cardapio(self):
        return super().conectar_cardapio()

    def adicionar(self, prato, valor, categoria):
        return super().adicionar(prato, valor, categoria)

    def apagar(self, prato):
        return super().apagar(prato)

    def atualizar(self, prato, valor, category):
        return super().atualizar(prato, valor, category)

    def exibir_pratos(self):
        return super().exibir_pratos()

    def limpa(self, nome, valor, category):
        return super().limpa(nome, valor, category)

    def opcoes(self):
        # Add Menu
        self.my_menu = Menu(self.root_cardapio)
        self.root_cardapio.config(menu=self.my_menu)

        self.my_menu.add_command(label='Inicio', command=lambda:[self.destruir(),
        self.fundo_inicio(), self.inicio_botoes(), self.my_menu.destroy()])
        # Configurar menu
        option_menu = Menu(self.my_menu, tearoff=0)
        self.my_menu.add_cascade(label="Opções", menu=option_menu)
        # opcoes do menu
        option_menu.add_command(label="Monte seu poke", command= lambda:[self.go_personalize(), 
        Make_dish(self.root_cardapio, self.info_cliente, self.end_cliente, self.fundo_inicio, self.inicio_botoes)])
        option_menu.add_command(label="Menu", command= lambda:[self.frame_cardapio.destroy(), self.menu_geral()])

    def go_personalize(self):
        try:
            self.frame_cardapio.destroy()
            self.frame_botao.destroy()
            self.frame_prato.destroy()
        except AttributeError:
            self.go_personalize2()

    def go_personalize2(self):
        try:
            self.frame_cardapio.destroy()
            self.frame_botao.destroy()
            self.frame_categoria.destroy()
        except AttributeError:
            self.frame_cardapio.destroy()
            self.frame_botao.destroy()

    def destruir(self):
        try:
            self.frame_cardapio.destroy()
            self.frame_categoria.destroy()
            self.frame_botao.destroy()
        except AttributeError:
            self.destruir2()

    def destruir2(self):
        try:
            self.frame_cardapio.destroy()
            self.frame_prato.destroy()
            self.frame_botao.destroy()
        except AttributeError:
            self.frame_cardapio.destroy()
            self.frame_botao.destroy()

    def acessorios(self):
        lista = []
        self.frame_botao = Frame(self.root_cardapio)
        self.frame_botao.place(relx=0.0, rely=0.66, relwidth=1, relheight=0.4)
        self.frame_botao.configure(background='snow')
        letra = font.Font(size=28)

        pratos = Button(self.frame_botao, text='Pratos', relief=FLAT, activebackground='snow', highlightbackground='snow',
        background='snow', activeforeground='lightblue', command=lambda:[self.novo_prato(lista)])
        pratos.place(relx=0.21, rely=0.2, relwidth=0.15, relheight=0.2)
        pratos.configure(font=letra)

        catego = Button(self.frame_botao, text='Categoria', relief=FLAT, activebackground='snow', highlightbackground='snow',
        background='snow', activeforeground='lightblue', command=lambda:[self.nova_cat()])
        catego.place(relx=0.6, rely=0.2, relwidth=0.235, relheight=0.235)
        catego.configure(font=letra)

    def novo_prato(self, lista):
        try:
            cat_pratos = open('categoria_pratos.json', 'r', encoding='utf8')
            todas_cat = json.load(cat_pratos)
            cat_pratos.close()
            for x in todas_cat:
                for y in x.values():
                    lista.append(y)
        except FileNotFoundError:
            padrao = [{1: 'Sem categoria'}]
            with open('categoria_pratos.json', 'w', encoding= 'utf8') as f:
                json.dump(padrao, f, indent=2)
                lista.append('Sem categoria')
        finally:
            self.frame_botao.destroy()
            self.frame_prato = Frame(self.root_cardapio)
            self.frame_prato.place(relx=0.0, rely=0.66, relwidth=1, relheight=0.4)
            self.frame_prato.configure(background='snow')

            nome_prato =  Label(self.frame_prato, text='Nome')
            nome_prato.place(relx=0.15, rely=0.1, relwidth=0.15, relheight=0.12)
            nome_prato.configure(background='snow')
            self.prato_entry = Entry(self.frame_prato)
            self.prato_entry.place(relx=0.1, rely=0.25, relwidth=0.25, relheight=0.12)

            valor_prato =  Label(self.frame_prato, text='Valor')
            valor_prato.place(relx=0.45, rely=0.1, relwidth=0.15, relheight=0.12)
            valor_prato.configure(background='snow')
            self.valor_entry = Entry(self.frame_prato)
            self.valor_entry.place(relx=0.45, rely=0.25, relwidth=0.15, relheight=0.12)

            categoria =  Label(self.frame_prato, text='Categoria')
            categoria.place(relx=0.72, rely=0.1, relwidth=0.15, relheight=0.12)
            categoria.configure(background='snow')
            self.categoria_box = ttk.Combobox(self.frame_prato, values=lista)
            self.categoria_box.place(relx=0.7, rely=0.25, relwidth=0.15, relheight=0.12)

            def verification_add(dish, price, cate):
                if dish.get() == '':
                    messagebox.showerror('ERRO', 'Insira um nome válido')
                elif price.get() is int:
                    print(price.get())
                    if price.get() == '' or ' ':
                        messagebox.showerror('ERRO', 'Insira o valor do prato')
                    else:
                        messagebox.showerror('ERRO', 'Insira apenas numeros no valor')
                elif cate.get() == '':
                    print(cate.get())
                    messagebox.showerror('ERRO', 'Selecione a categoria do prato')
                else:
                    self.adicionar(dish.get().title(), price.get(), cate.get().title())
                    self.limpa(dish, price, cate)
                    self.atualiza_tabela()

            def verification_update(dish, price, cate):
                if dish.get() == '':
                    if dish.get() ==  " ":
                        messagebox.showerror('ERRO', 'Insira um nome válido')
                elif price.get() is int: 
                    if price.get() == ' ':
                        messagebox.showerror('ERRO', 'Insira o valor do prato')
                    if price.get() == '':
                        messagebox.showerror('ERRO', 'Insira o valor do prato')
                    else:    
                        messagebox.showerror('ERRO', 'Insira apenas numeros no valor')
                elif cate.get() == '':
                    if cate.get() == ' ':
                        messagebox.showerror('ERRO', 'Selecione a categoria do prato')
                else:
                    self.atualizar(dish.get().title(), price.get(), cate.get().title())
                    self.limpa(dish, price, cate)
                    self.atualiza_tabela()

            def verification_remove(dish, price, cate):
                if dish.get == '':
                    if dish.get == ' ':
                        messagebox.showerror('ERRO', 'Informe o nome do prato antes de remove-lo')
                else:
                    self.apagar(dish.get().title())
                    self.limpa(dish, price, cate)
                    self.atualiza_tabela()

            add_button = Button(self.frame_prato, text='Adicionar', relief=FLAT, activebackground='snow',
			highlightbackground='snow', activeforeground='green', background='snow', command=lambda:[verification_add(
            self.prato_entry, self.valor_entry, self.categoria_box)])
            add_button.place(relx=0.7, rely=0.6, relwidth=0.15, relheight=0.12)

            update_button = Button(self.frame_prato, text='Atualizar', relief=FLAT, activebackground='snow',
			highlightbackground='snow', activeforeground='gold', background='snow', command=lambda:[verification_update(
            self.prato_entry, self.valor_entry, self.categoria_box)])
            update_button.place(relx=0.45, rely=0.6, relwidth=0.15, relheight=0.12)

            remove_button = Button(self.frame_prato, text='Remover', relief=FLAT, activebackground='snow',
			highlightbackground='snow', activeforeground='red', background='snow', command=lambda:[verification_remove(
            self.prato_entry, self.valor_entry, self.categoria_box)])
            remove_button.place(relx=0.2, rely=0.6, relwidth=0.15, relheight=0.12)

            back = Image.open('Imagens/voltar.png')
            back_img = ImageTk.PhotoImage(back)
            return_bt = Button(self.frame_prato, image=back_img, relief=FLAT, activebackground='lightblue',
			highlightbackground='snow', background='snow',
            command=lambda:[self.frame_prato.destroy(), self.acessorios()])
            return_bt.imagem = back_img
            return_bt.place(relx=0.05, rely=0.6, relwidth=0.05, relheight=0.12)

    def nova_cat(self):
        self.frame_botao.destroy()
        self.frame_categoria = Frame(self.root_cardapio)
        self.frame_categoria.place(relx=0.0, rely=0.66, relwidth=1, relheight=0.4)
        self.frame_categoria.configure(background='snow')

        nome_categoria =  Label(self.frame_categoria, text='Nome')
        nome_categoria.place(relx=0.425, rely=0.1, relwidth=0.15, relheight=0.12)
        nome_categoria.configure(background='snow')
        self.cat_entry = Entry(self.frame_categoria)
        self.cat_entry.place(relx=0.385, rely=0.25, relwidth=0.25, relheight=0.12)
        
        def add_cat(new_cat):
            def cria_json():
                cat_pratos = open('categoria_pratos.json', 'r', encoding='utf8')
                todas_cat = json.load(cat_pratos)
                cat_pratos.close()
                dici_cat = todas_cat[0]
                print(dici_cat)
                for x in dici_cat.values():
                    indice = len(todas_cat) + 1
                    if new_cat not in dici_cat.values():
                        todas_cat.append({indice: new_cat})
                        self.lista_cat.append(new_cat)
                cat_pratos =  open('categoria_pratos.json', 'w', encoding= 'utf8')
                json.dump(todas_cat, cat_pratos, indent=2)
                cat_pratos.close()
            try:
                 cria_json()
            except FileNotFoundError:
                padrao = [{1: 'Sem categoria'}]
                with open('categoria_pratos.json', 'w', encoding= 'utf8') as f:
                    json.dump(padrao, f, indent=2)
                cria_json()                    

        add_categoria = Button(self.frame_categoria, text='Add categoria', relief=FLAT, activebackground='snow', background='snow',
		highlightbackground='snow', activeforeground='green', command=lambda:[add_cat(self.cat_entry.get().title()),
        self.cat_entry.delete(0, 'end')])
        add_categoria.place(relx=0.385, rely=0.55, relwidth=0.25, relheight=0.12)

        back2 = Image.open('Imagens/voltar.png')
        back_img2 = ImageTk.PhotoImage(back2)
        return_bt_category = Button(self.frame_categoria, image=back_img2, relief=FLAT, activebackground='lightblue',
        highlightbackground='snow', background='snow',
        command=lambda:[self.frame_categoria.destroy(), self.acessorios()])
        return_bt_category.imagem = back_img2
        return_bt_category.place(relx=0.05, rely=0.6, relwidth=0.05, relheight=0.12)

    def seleciona(self, event):
        for x in self.menu.selection():
            self.dish, self.price = self.menu.item(x, 'values')
            self.prato_entry.delete(0, 'end')
            self.valor_entry.delete(0, 'end')
            remove = '$'
            for l in range(len(remove)):
                self.price = self.price.replace(remove[l], "")
            self.price = self.price.rstrip()
            self.prato_entry.insert(END, self.dish)
            self.valor_entry.insert(END, self.price)
    #Menu
    def cria_menu(self):
        self.frame_cardapio = Frame(self.root_cardapio)
        self.frame_cardapio.place(relx=0.01, rely=0.02, relwidth=0.98, relheight=0.65)
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

    def menu_geral(self):
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
        bd_menu = c.fetchall()
        global count
        count = 0
        self.l = []
        arq_json = open('categoria_pratos.json', 'r', encoding='utf8')
        list_cat = json.load(arq_json)
        for x in list_cat:
            for y in x.values():
                self.l.append(y)
        indice = 1
        count_color = 0
        
        def inserir_cat(count_color, nome_cat, control):
            try:
                self.menu.insert('', 'end', nome_cat, tags=('cor3',), values=(('⮯', nome_cat), ''))
            except Exception as e:
                pass
        controle = []
        while indice <= len(self.l):
            for a in self.l:
                for categoria in bd_menu:
                    if a == categoria[2]:
                        inserir_cat(count_color, a, self.l)
                        if categoria[2] == a:
                            if categoria[0] not in controle:
                                controle.append(categoria[0])
                                if count % 2 == 0:
                                    self.menu.insert(a, 'end', values=(categoria[0], (categoria[1],'$')), tags=('cor2',))
                                else:
                                    self.menu.insert(a, 'end', values=(categoria[0], (categoria[1],'$')), tags=('cor1',))
                                count += 1
                            else:
                                pass
            indice += 1
        self.menu.bind('<Double-Button-3>', self.seleciona)

    def atualiza_tabela(self):
        self.menu.delete(*self.menu.get_children())
        conn = self.conectar_cardapio() 
        c = conn.cursor()
        c.execute("""SELECT nome_prato, valor_prato, categoria FROM menu ORDER BY nome_prato""")
        bd_menu = c.fetchall()
        global count
        count = 0
        self.l = []
        arq_json = open('categoria_pratos.json', 'r', encoding='utf8')
        list_cat = json.load(arq_json)
        for x in list_cat:
            for y in x.values():
                self.l.append(y)
        indice = 1

        def inserir_cat(indice, nome_cat):
            try:
                self.menu.insert('', 'end', nome_cat, tags=('cor3',), values=(('⮯', nome_cat), ''))
            except Exception:
                pass

        controle = []
        while indice <= len(self.l):
            for a in self.l:
                for categoria in bd_menu:
                    if a == categoria[2]:
                        inserir_cat(indice, a)
                        if categoria[2] == a:
                            if categoria[0] not in controle:
                                controle.append(categoria[0])
                                print(controle)
                                if count % 2 == 0:
                                        self.menu.insert(a, 'end',
                                                values=(categoria[0], (categoria[1],'$')), tags=('cor2',))
                                else:
                                    self.menu.insert(a, 'end',
                                                values=(categoria[0], (categoria[1],'$')), tags=('cor1',))
                                count += 1
                            else:
                                pass
            indice += 1
        self.menu.bind('<Double-Button-3>', self.seleciona)
