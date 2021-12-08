from tkinter import *
from tkinter import ttk
from cardapio_v2 import Cardapio, Modelo_prato
from pedido import *
from PIL import Image, ImageTk


class tela_cardapio(Cardapio, Pedido):
    def __init__(self, info_cliente):
        super().__init__()
        self.root = Tk()
        self.root.title('Cardapio')
        self.root.geometry('800x500')
        self.opcoes()
        self.botoes()
        self.info_cliente = info_cliente
        self.nome_pedido(info_cliente)
        self.tabela()
        self.valor_total = 0
        self.total_pedido(self.valor_total)
        self.modelo = Modelo_prato()
        self.carrinho = []
        self.memoria = {}
        self.quant = 1
        self.contador = 0
        self.root.mainloop()

    def conectar(self):
        return super().conectar()

    def adicionar(self, prato, valor):
        return super().adicionar(prato, valor)

    def apagar(self):
        return super().apagar()

    def exibir_pratos(self):
        return super().exibir_pratos()
    
    def novo_pedido(self, nome_c, prato, func):
        return super().novo_pedido(nome_c, prato, func)

    def nome_pedido(self, nome_cliente):
        self.name = LabelFrame(self.root, text=nome_cliente)
        self.name.place(relx=0.65, rely=0.05, relwidth=0.32, relheight=0.5)

    def total_pedido(self, valor):
        self.total = Label(self.root, text=f'TOTAL: {valor}')
        self.total.place(relx=0.7, rely=0.6, relwidth=0.3, relheight=0.15)

    def set_total(self):
        self.valor_total = sum(self.carrinho)
        self.total_pedido(self.valor_total)
        return self.valor_total

    def soma_pratos(self):
        conn = self.conectar()
        c = conn.cursor()
        prato = self.valor.get()
        c.execute('''SELECT valor_prato FROM menu WHERE nome_prato = %s''', (prato,))
        preco = c.fetchall()
        for x in preco:
            self.carrinho.append(x[0])

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
        for x in self.lista.selection():
            quant, prato = self.lista.item(x, 'values')
            if self.memoria[prato] > 1:
                self.memoria[prato] = self.memoria[prato] - 1
                print(self.memoria)
                self.inserir()
            else:
                del self.memoria[prato]
                print(self.memoria)
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

        self.lista = ttk.Treeview(self.name, yscrollcommand=tree_scroll.set,
                             selectmode="extended")
        self.lista.place(relx=0.01, rely=0.02, relwidth=0.935, relheight=0.98)

        tree_scroll.config(command=self.lista.yview)

        self.lista['columns'] = ("Quant", "Prato")
        self.lista.column("#0", width=0, stretch=NO)
        self.lista.column("Quant", anchor=W, width=50)
        self.lista.column("Prato", anchor=W, width=250)

        self.lista.heading("#0", text="", anchor=W)
        self.lista.heading("Prato", text="Prato", anchor=CENTER)
        self.lista.heading("Quant", text="Quant", anchor=CENTER)

        self.lista.bind('<Double-Button-1>', self.seleciona)

    def select_pratos(self):    
        for x in self.memoria.keys():
            return x

    def inserir(self):
        if self.valor.get() not in self.memoria:
            self.quant = 1
        self.memoria[self.valor.get()] = self.quant
        self.lista.delete(*self.lista.get_children())
        for p, q in self.memoria.items():
            self.lista.insert(parent='', index='end', text='',
                            values=(q, p))
        self.quant += 1

    def opcoes(self):
        nb1 = ttk.Notebook(self.root)
        nb1.place(relx = 0.02, rely = 0.02, relwidth = 0.62, relheight = 0.65)
        #Frame Novo Pedido
        fr1 = ttk.Frame(nb1, width=400, height=280)
        fr1.place(relx = 0.02, rely = 0.02, relwidth = 0.8, relheight = 0.95)
        nb1.add(fr1, text = 'Entradas')
        fr2 = ttk.Frame(nb1, width=400, height=280)
        fr2.place(relx = 0.02, rely = 0.02, relwidth = 0.8, relheight = 0.95)
        nb1.add(fr2, text = 'Toasts')
        fr3 = Frame(nb1)
        nb1.add(fr3, text = 'Saladas')
        fr4 = Frame(nb1)
        nb1.add(fr4, text = 'Bowls')
        fr5 = Frame(nb1)
        nb1.add(fr5, text = 'Poke')
        fr6 = Frame(nb1)
        nb1.add(fr6, text = 'Wraps')
        fr7 = Frame(nb1)
        nb1.add(fr7, text = 'Sobremesas')
        fr8 = Frame(nb1)
        nb1.add(fr8, text = 'Bebidas')

    #checkbox entradas
        self.valor = StringVar(fr1)
        
        ent1 = Radiobutton(fr1, text = 'Dadinhos de queijo coalho',
                                var = self.valor, value = 'Dadinhos')
        ent1.place(relx = 0.02, rely = 0.1)
                    
        ent2 = Radiobutton(fr1, text = 'Power Guacamole',
                                     var = self.valor, value = 'Power guacamole')
        ent2.place(relx = 0.02, rely = 0.2)

        ent3 = Radiobutton(fr1, text = 'Tofu',
                                     var = self.valor, value = 'Tofu')
        ent3.place(relx = 0.02, rely = 0.3)

        ent4 = Radiobutton(fr1, text = 'Nuggets De Frango',
                                     var = self.valor, value = 'Nuggets De Frango')
        ent4.place(relx = 0.02, rely = 0.4)

        ent5 = Radiobutton(fr1, text = 'Super Kale',
                                     var = self.valor, value = 'Super Kale')
        ent5.place(relx = 0.02, rely = 0.5)

    #checkbox Toasts
        toa1 = Radiobutton(fr2, text = 'Fig toast',
                            var = self.valor, value = 'Fig toast')
        toa1.place(relx = 0.02, rely = 0.1)
                
        toa2 = Radiobutton(fr2, text = 'Salmon toast',
                                 var = self.valor, value = 'Salmon toast')
        toa2.place(relx = 0.02, rely = 0.2)

        toa3 = Radiobutton(fr2, text = 'Mediterranean toast',
                                 var = self.valor, value = 'Mediterranean toast')
        toa3.place(relx = 0.02, rely = 0.3)

    #checkbox Saladas
        sal1 = Radiobutton(fr3, text = 'Fresh',
                            var = self.valor, value = 'Fresh')
        sal1.place(relx = 0.02, rely = 0.1)
                
        sal2 = Radiobutton(fr3, text = 'Superfood',
                                 var = self.valor, value = 'Superfood')
        sal2.place(relx = 0.02, rely = 0.2)

        sal3 = Radiobutton(fr3, text = 'Raizes',
                                 var = self.valor, value = 'Raizes')
        sal3.place(relx = 0.02, rely = 0.3)

    #checkbox Bowls
        bow1 = Radiobutton(fr4, text = 'Brazilian Bowl',
                            var = self.valor, value = 'Brazilian bowl')
        bow1.place(relx = 0.02, rely = 0.1)
                
        bow2 = Radiobutton(fr4, text = 'Earth Bowl',
                                 var = self.valor, value = 'Earth bowl')
        bow2.place(relx = 0.02, rely = 0.2)

        bow3 = Radiobutton(fr4, text = 'Healthy Bowl',
                                 var = self.valor, value = 'Healthy bowl')
        bow3.place(relx = 0.02, rely = 0.3)

        bow4 = Radiobutton(fr4, text = 'Prevention Bowl',
                                 var = self.valor, value = 'Prevention Bowl')
        bow4.place(relx = 0.02, rely = 0.4)

        bow5 = Radiobutton(fr4, text = 'Sea Bowl',
                                 var = self.valor, value = 'Sea bowl')
        bow5.place(relx = 0.02, rely = 0.5)

        bow6 = Radiobutton(fr4, text = 'Tuna Bowl',
                                 var = self.valor, value = 'Tuna bowl')
        bow6.place(relx = 0.02, rely = 0.6)

        bow7 = Radiobutton(fr4, text = 'Fish Bowl',
                                 var = self.valor, value = 'Fish bowl')
        bow7.place(relx = 0.02, rely = 0.7)

        bow8 = Radiobutton(fr4, text = 'Chicken Bowl',
                                 var = self.valor, value = 'Chicken bowl')
        bow8.place(relx = 0.5, rely = 0.1)

        bow9 = Radiobutton(fr4, text = 'Escondidinho',
                                 var = self.valor, value = 'Escondidinho')
        bow9.place(relx = 0.5, rely = 0.2)

        bow10 = Radiobutton(fr4, text = 'Poke bowl',
                                 var = self.valor, value = 'Poke bowl')
        bow10.place(relx = 0.5, rely = 0.3)

        bow11 = Radiobutton(fr4, text = 'Salmon Bowl',
                                 var = self.valor, value = 'Salmon bowl')
        bow11.place(relx = 0.5, rely = 0.4)

        bow12 = Radiobutton(fr4, text = 'Shrimp Bowl',
                                 var = self.valor, value = 'Shrimp bowl')
        bow12.place(relx = 0.5, rely = 0.5)

        bow13 = Radiobutton(fr4, text = 'Vegan Bowl',
                                 var = self.valor, value = 'Vegan bowl')
        bow13.place(relx = 0.5, rely = 0.6)    

    #checkbox Poke
        pok1 = Radiobutton(fr5, text = 'Poke de atum',
                            var = self.valor, value = 'Poke de atum')
        pok1.place(relx = 0.02, rely = 0.1)
                
        pok2 = Radiobutton(fr5, text = 'Poke vegano',
                                 var = self.valor, value = 'Poke vegano')
        pok2.place(relx = 0.02, rely = 0.2)

        pok3 = Radiobutton(fr5, text = 'Poke De Salmão',
                                 var = self.valor, value = 'Poke De salmão')
        pok3.place(relx = 0.02, rely = 0.3)

        pok3 = Radiobutton(fr5, text = 'Monte seu poke',
                                 var = self.valor, value = 'Monte seu poke')
        pok3.place(relx = 0.02, rely = 0.4)

    #checkbox Burgers, pizza e warps
        piz1 = Radiobutton(fr6, text = 'Pizza De Shitake E Gorgonzola',
                                 var = self.valor, value = 'Pizza De Shitake E Gorgonzola')
        piz1.place(relx = 0.02, rely = 0.1)

        piz2 = Radiobutton(fr6, text = 'Tomate, Mussarela De Búfala E Manjericão',
                                 var = self.valor, value = 'Tomate, Mussarela De Búfala E Manjericão')
        piz2.place(relx = 0.02, rely = 0.2)

        bur1 = Radiobutton(fr6, text = 'Burger of the future',
                                 var = self.valor, value = 'Burger Of The Future')
        bur1.place(relx = 0.02, rely = 0.3)

        bur2 = Radiobutton(fr6, text = 'Wonder burger',
                                 var = self.valor, value = 'Wonder Burger')
        bur2.place(relx = 0.02, rely = 0.4)

        bur3 = Radiobutton(fr6, text = 'Chicken Burger',
                                 var = self.valor, value = 'Chicken Burger')
        bur3.place(relx = 0.02, rely = 0.5)

        war1 = Radiobutton(fr6, text = 'Warp',
                                 var = self.valor, value = 'Warp')
        war1.place(relx = 0.02, rely = 0.6)

    #checkbox Sobremesas
        sob1 = Radiobutton(fr7, text = 'American pancake',
                            var = self.valor, value = 'American Pancake')
        sob1.place(relx = 0.02, rely = 0.1)
                
        sob2 = Radiobutton(fr7, text = 'American pancake duo',
                                 var = self.valor, value = 'American Pancake Duo')
        sob2.place(relx = 0.02, rely = 0.2)

        sob3 = Radiobutton(fr7, text = 'Golden pie',
                                 var = self.valor, value = 'Golden Pie')
        sob3.place(relx = 0.02, rely = 0.3)

        sob4 = Radiobutton(fr7, text = 'Petit gateau zero - chocolate branco',
                                 var = self.valor, value = 'Petit Gateau Zero - Chocolate Branco')
        sob4.place(relx = 0.02, rely = 0.4)

        sob5 = Radiobutton(fr7, text = 'Funcional Pie',
                                 var = self.valor, value = 'Funcional Pie')
        sob5.place(relx = 0.02, rely = 0.5)

        sob6 = Radiobutton(fr7, text = 'Cheesecake Low Carb De Frutas Vermelhas',
                                 var = self.valor, value = 'Cheesecake Low Carb De Frutas Vermelhas')
        sob6.place(relx = 0.02, rely = 0.6)

        sob7 = Radiobutton(fr7, text = 'Petit Gateau',
                                 var = self.valor, value = 'Petit Gateau')
        sob7.place(relx = 0.02, rely = 0.7)

    #checkbox Bebidas
        beb1 = Radiobutton(fr8, text = 'Carrot juice',
                            var = self.valor, value = 'Carrot Juice')
        beb1.place(relx = 0.02, rely = 0.1)
                
        beb2 = Radiobutton(fr8, text = 'Immunity Shot 300ml',
                                 var = self.valor, value = 'Immunity Shot 300ml')
        beb2.place(relx = 0.02, rely = 0.2)

        beb11 = Radiobutton(fr8, text = 'Refreshing Juice',
                                 var = self.valor, value = 'Refreshing Juice')
        beb11.place(relx = 0.02, rely = 0.3)

        beb3 = Radiobutton(fr8, text = 'Chá Mate Zero De Pêssego Adoçado Com Stévia',
                                 var = self.valor, value = 'Chá Mate Zero De Pêssego Adoçado Com Stévia')
        beb3.place(relx = 0.02, rely = 0.4)

        beb10 = Radiobutton(fr8, text = 'Chá Mate Zero De Limão Adoçado Com Stévia',
                                 var = self.valor, value = 'Chá Mate Zero De Limão Adoçado Com Stévia')
        beb10.place(relx = 0.02, rely = 0.5)

        beb4 = Radiobutton(fr8, text = 'Coca cola zero',
                                 var = self.valor, value = 'Coca Cola Zero')
        beb4.place(relx = 0.02, rely = 0.6)

        beb5 = Radiobutton(fr8, text = 'H2O',
                                 var = self.valor, value = 'H2O')
        beb5.place(relx = 0.02, rely = 0.7)

        beb6 = Radiobutton(fr8, text = 'Lemon Juice',
                                 var = self.valor, value = 'Lemon Juice')
        beb6.place(relx = 0.02, rely = 0.8)

        beb7 = Radiobutton(fr8, text = 'Água sem gás',
                                 var = self.valor, value = 'Água Sem Gás')
        beb7.place(relx = 0.5, rely = 0.1)

        beb8 = Radiobutton(fr8, text = 'Água com gás',
                                 var = self.valor, value = 'Água Com Gás')
        beb8.place(relx = 0.5, rely = 0.2)

