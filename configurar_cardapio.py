from tkinter import *
from tkinter import ttk
from tkinter import font
from PIL import Image, ImageTk
from cardapio_v2 import Cardapio, Modelo_prato
from pedido import *
from bairrosv2 import Local
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
        self.cria_poke()
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

    def atualizar(self, prato, valor):
        return super().atualizar(prato, valor)

    def exibir_pratos(self):
        return super().exibir_pratos()

    def limpa(self, nome, valor):
        return super().limpa(nome, valor)

    def opcoes(self):
        # Add Menu
        my_menu = Menu(self.root_cardapio)
        self.root_cardapio.config(menu=my_menu)

        my_menu.add_command(label='Inicio', command=lambda:[
        self.frame_menu.destroy(), self.frame_botao.destroy(), self.frame_cardapio.destroy(),
        self.fundo_inicio, self.inicio_botoes, my_menu.destroy()])
        # Configurar menu
        option_menu = Menu(my_menu, tearoff=0)
        my_menu.add_cascade(label="Opções", menu=option_menu)
        # opcoes do menu
        option_menu.add_command(label="Configurar pratos", command= lambda:[])
        option_menu.add_command(label="Monte seu poke", command= lambda:[self.monte_poke()])
        option_menu.add_command(label="Menu", command= lambda:[self.frame_cardapio.destroy(), self.menu_geral()])

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
            print(todas_cat)
            for x in todas_cat:
                for y in x.values():
                    lista.append(y)
        except FileNotFoundError:
            padrao = [{1: 'Sem categoria'}]
            with open('categoria_pratos.json', 'w', encoding= 'utf8') as f:
                json.dump(padrao, f, indent=2)
                lista.append('Sem categoria')

        self.frame_botao.destroy()
        frame_prato = Frame(self.root_cardapio)
        frame_prato.place(relx=0.0, rely=0.66, relwidth=1, relheight=0.4)
        frame_prato.configure(background='snow')

        nome_prato =  Label(frame_prato, text='Nome')
        nome_prato.place(relx=0.15, rely=0.1, relwidth=0.15, relheight=0.12)
        nome_prato.configure(background='snow')
        prato_entry = Entry(frame_prato)
        prato_entry.place(relx=0.1, rely=0.25, relwidth=0.25, relheight=0.12)
        self.prato_entry = prato_entry.get().title()

        valor_prato =  Label(frame_prato, text='Valor')
        valor_prato.place(relx=0.45, rely=0.1, relwidth=0.15, relheight=0.12)
        valor_prato.configure(background='snow')
        valor_entry = Entry(frame_prato)
        valor_entry.place(relx=0.45, rely=0.25, relwidth=0.15, relheight=0.12)

        categoria =  Label(frame_prato, text='Categoria')
        categoria.place(relx=0.72, rely=0.1, relwidth=0.15, relheight=0.12)
        categoria.configure(background='snow')
        categoria_box = ttk.Combobox(frame_prato, values=lista)
        categoria_box.place(relx=0.7, rely=0.25, relwidth=0.15, relheight=0.12)

    def nova_cat(self):
        self.frame_botao.destroy()
        frame_categoria = Frame(self.root_cardapio)
        frame_categoria.place(relx=0.0, rely=0.66, relwidth=1, relheight=0.4)
        frame_categoria.configure(background='snow')

        nome_categoria =  Label(frame_categoria, text='Nome')
        nome_categoria.place(relx=0.425, rely=0.1, relwidth=0.15, relheight=0.12)
        nome_categoria.configure(background='snow')
        self.cat_entry = Entry(frame_categoria)
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

        add_categoria = Button(frame_categoria, text='Add categoria', relief=FLAT, activebackground='snow', background='snow',
		highlightbackground='snow', activeforeground='green', command=lambda:[add_cat(self.cat_entry.get().title()),
        self.cat_entry.delete(0, 'end')])
        add_categoria.place(relx=0.385, rely=0.55, relwidth=0.25, relheight=0.12)

    def seleciona(self, event):
        for x in self.menu.selection():
            self.prato, self.preco = self.menu.item(x, 'values')
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

    def cria_poke(self):
        self.frame_menu = Frame(self.root_cardapio)
        self.frame_menu.place(relx=0.01, rely=0.02, relwidth=0.98, relheight=0.65)
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
'''
    def monte_poke(self):
        try:
            self.frame_cardapio.place_forget()
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
            except TypeError as e:
                print(e)
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
            except TypeError as e:
                print(e)
                
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
'''