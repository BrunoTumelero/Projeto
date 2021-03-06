from tkinter import *
from tkinter import ttk
from tkinter import font
from cardapio_v2 import Cardapio
import json
from tkinter import messagebox
from PIL import Image, ImageTk

class Make_dish(Cardapio):
    def __init__(self, root, info_cliente, end_cliente, fundo, botoes_inicio):
        super().__init__()
        self.root_make = root
        self.root_make.title('Monte seu prato')
        self.root_make.configure(background='snow')
        self.fundo_inicio = fundo
        self.inicio_botoes = botoes_inicio
        self.info_cliente = info_cliente
        self.end_cliente = end_cliente
        self.list_control_poke = []
        self.create_dish()
        self.make_dish()
        self.options_poke()

    def create_dish(self):
        self.frame_menu = Frame(self.root_make)
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

    def make_dish(self):
        def elimination():
            try:
                self.frame_prato.destroy()
            except AttributeError:
                self.frame_categoria.destroy()
        try:
            elimination()
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

            proteina = Label(self.pag1, text='2.PROTE??NAS 120g', anchor='w')
            proteina.place(relx=0.45, rely=0.02, relwidth=0.55, relheight=0.15)
            proteina.configure(font=letra, background='snow')
            escolha_prot = Label(self.pag1, text='Escolha at?? 2 (60g de cada)', foreground='blue',
            anchor='w')
            escolha_prot.place(relx=0.45, rely=0.15, relwidth=0.5, relheight=0.08)
            escolha_prot.configure(font=letra2, background='snow')
            info_prot = Label(self.pag1, text='-Sera considerada a prote??na de maior valor-',
            anchor='w')
            info_prot.place(relx=0.45, rely=0.23, relwidth=0.55, relheight=0.08)
            info_prot.configure(font=letra3, background='snow')

            self.extra_poke = []
            self.escolha_base = []
            self.proteina = []
            self.base_1 = IntVar(self.pag1) 
            self.base_2 = IntVar(self.pag1) 
            self.base_3 = IntVar(self.pag1) 
            self.base_4 = IntVar(self.pag1) 
            self.base_5 = IntVar(self.pag1)

    def options_poke(self):#op????es do poke
        self.read_json()
        letra4 = font.Font(size=35)
        options_frame = Frame(self.root_make)
        options_frame.place(relx=0.0, rely=0.7, relwidth=1, relheight=0.3)
        options_frame.configure(background='snow')

        conf_base = Button(options_frame, text='Base', background='snow', highlightbackground='snow', activebackground='snow',
        activeforeground='lightblue', relief=FLAT, font=letra4, command=lambda:[self.settings_base(options_frame)])
        conf_base.place(relx=0.165, rely=0.4, relwidth=0.145, relheight=0.25)

        conf_prot = Button(options_frame, text='Prote??na', background='snow', highlightbackground='snow', activebackground='snow',
        activeforeground='lightblue', relief=FLAT, font=letra4, command=lambda:[self.settings_protein(options_frame)])
        conf_prot.place(relx=0.6, rely=0.4, relwidth=0.24, relheight=0.25)
    
    def read_json(self):#cria o json que vai armazenar as opcoes
            variable = 1
            control_place = 0.25
            dish_json = open('create_dish.json', 'r', encoding='utf8')
            arq_json = json.load(dish_json)
            dish_json.close()
            dici_dish = arq_json[0]
            for x in dici_dish.keys():
                self.insert_option(x, control_place, variable)
                variable += 1
                control_place += 0.1
            dish_json =  open('create_dish.json', 'w', encoding= 'utf8')
            json.dump(arq_json, dish_json, indent=2)
            dish_json.close()

    def create_json(self):
        try:
            dish_json = open('create_dish.json', 'r', encoding='utf8')
            arq_json = json.load(dish_json)
            dish_json.close()
            dici_dish = arq_json[0]
            for x in dici_dish.keys():
                options = []
                if self.input_op.get() not in dici_dish.keys():
                    arq_json.append({self.input_op.get(): options})
            dish_json =  open('create_dish.json', 'w', encoding= 'utf8')
            json.dump(arq_json, dish_json, indent=2)
            dish_json.close()
        except Exception:
            padrao = [{'': 'Sem categoria'}]
            with open('create_dish.json', 'w', encoding= 'utf8') as f:
                json.dump(padrao, f, indent=2)

    def insert_option(self, option, control_place, variable):
        try:
            variable = Checkbutton(self.pag1, text=option,
            highlightbackground='snow', activebackground='snow', activeforeground='blue4', relief=FLAT,
            anchor='w', background='snow')
            variable.place(relx=0.02, rely=control_place, relwidth=0.25, relheight=0.1)
        except Exception as e:
            print(e)
        for key in self.list_control_poke:
            if key == '':
                pass
            else:
                self.insert_option(key, control_place, variable)
    
    def settings_base(self, frame):
        frame.destroy()
        settings_frame_base = Frame(self.root_make)
        settings_frame_base.place(relx=0.0, rely=0.7, relwidth=1, relheight=0.3)
        settings_frame_base.configure(background='snow')

        op = Label(settings_frame_base, text='Op????o base', anchor='w')
        op.configure(background='snow')
        op.place(relx=0.05, rely=0.15, relwidth=0.2, relheight=0.15)
        self.input_op = Entry(settings_frame_base)
        self.input_op.place(relx=0.05, rely=0.35, relwidth=0.45, relheight=0.15)

        value_collected = IntVar()
        value_extra = Checkbutton(settings_frame_base, text='Valor extra', background='snow', highlightbackground='snow', 
        activebackground='snow', activeforeground='blue4', anchor='w', onvalue= 1, offvalue=0, variable=value_collected,
        command=lambda:[verification_value()])
        value_extra.place(relx=0.75, rely=0.15, relwidth=0.13, relheight=0.15)
        value_extra_entry = Entry(settings_frame_base)

        add_op = Button(settings_frame_base, text='Adicionar', background='snow', highlightbackground='snow', 
        activebackground='snow', activeforeground='green', relief=FLAT, command=lambda:[add_choice_poke(),
        self.input_op.delete(0, 'end')])
        add_op.place(relx=0.65, rely=0.65, relwidth=0.1, relheight=0.2)
        retunr_button = Button(settings_frame_base, text='Retornar', background='snow', highlightbackground='snow', 
        activebackground='snow', activeforeground='yellow', relief=FLAT, command=lambda:[settings_frame_base.destroy(),
        self.options_poke()])
        retunr_button.place(relx=0.42, rely=0.65, relwidth=0.1, relheight=0.2)
        remove_op = Button(settings_frame_base, text='Remover', relief=FLAT, background='snow', highlightbackground='snow', 
        activebackground='snow', activeforeground='red')
        remove_op.place(relx=0.2, rely=0.65, relwidth=0.1, relheight=0.2)
                
        def verification_value():
            if value_collected.get() == 1:
                value_extra_entry.place(relx=0.75, rely=0.35, relwidth=0.12, relheight=0.15)
            if value_collected.get() == 0:
                value_extra_entry.place_forget()

        def add_choice_poke():
            try:
                self.cria_json_base()
            except FileNotFoundError:
                defaultt = [{self.input_op.get(): 0}]
                with open('create_poke.json', 'w', encoding= 'utf8') as f:
                    json.dump(defaultt, f, indent=2)
                self.cria_json_base()

        try:
            self.read_json()
        except FileNotFoundError:
            defaultt = [{self.input_op: 0}]
            with open('create_poke.json', 'w', encoding= 'utf8') as f:
                json.dump(defaultt, f, indent=2)
            self.read_json()

        try:
            arq_json = open('create_poke.json', 'r', encoding='utf8')
            arq_poke = json.load(arq_json)
            for x in arq_poke:
                for y in x.keys():
                    self.list_control_poke.append(y)
        except FileNotFoundError:
            start = [{'':0}]
            with open('create_poke.json', 'w', encoding= 'utf8') as f:
                    json.dump(start, f, indent=2)
                    f.close()

    def settings_protein(self, frame):
        frame.destroy()
        settings_frame_protein = Frame(self.root_make)
        settings_frame_protein.place(relx=0.0, rely=0.7, relwidth=1, relheight=0.3)
        settings_frame_protein.configure(background='snow')

        op = Label(settings_frame_protein, text='Op????o prote??na', anchor='w')
        op.configure(background='snow')
        op.place(relx=0.05, rely=0.1, relwidth=0.2, relheight=0.15)
        input_op = Entry(settings_frame_protein)
        input_op.place(relx=0.05, rely=0.3, relwidth=0.45, relheight=0.15)

        value_collected = IntVar()
        value_extra = Checkbutton(settings_frame_protein, text='Valor extra', background='snow', highlightbackground='snow', 
        activebackground='snow', activeforeground='blue4', anchor='w', onvalue= 1, offvalue=0, variable=value_collected,
        command=lambda:[verification_value()])
        value_extra.place(relx=0.75, rely=0.1, relwidth=0.13, relheight=0.15)
        value_extra_entry = Entry(settings_frame_protein)

        add_op = Button(settings_frame_protein, text='Adicionar', background='snow', highlightbackground='snow', 
        activebackground='snow', activeforeground='green', relief=FLAT, command=lambda:[add_protein(),
        input_op.delete(0, 'end'), value_extra_entry.delete(0, 'end')])
        add_op.place(relx=0.65, rely=0.65, relwidth=0.1, relheight=0.2)
        retunr_button = Button(settings_frame_protein, text='Retornar', background='snow', highlightbackground='snow', 
        activebackground='snow', activeforeground='yellow', relief=FLAT, command=lambda:[settings_frame_protein.destroy(),
        self.options_poke()])
        retunr_button.place(relx=0.42, rely=0.65, relwidth=0.1, relheight=0.2)
        remove_op = Button(settings_frame_protein, text='Remover', relief=FLAT, background='snow', highlightbackground='snow', 
        activebackground='snow', activeforeground='red')
        remove_op.place(relx=0.2, rely=0.65, relwidth=0.1, relheight=0.2)

        def verification_value():
                if value_collected.get() == 1:
                    value_extra_entry.place(relx=0.75, rely=0.35, relwidth=0.12, relheight=0.15)
                if value_collected.get() == 0:
                    value_extra_entry.place_forget()

        def cria_json_protein():
            poke_json = open('create_protein.json', 'r', encoding='utf8')
            arq_json = json.load(poke_json)
            poke_json.close()
            dici_poke = arq_json[0]
            for x in dici_poke.keys():
                indice = len(arq_json) + 1
                if input_op.get() not in dici_poke.keys():
                    arq_json.append({input_op.get(): indice})
            poke_json =  open('create_protein.json', 'w', encoding= 'utf8')
            json.dump(arq_json, poke_json, indent=2)
            poke_json.close()

        def add_protein():
            try:
                cria_json_protein()
            except FileNotFoundError:
                defaultt = [{input_op.get(): 0}]
                with open('create_protein.json', 'w', encoding= 'utf8') as f:
                    json.dump(defaultt, f, indent=2)
                cria_json_protein()

            try:
                list_protein = []
                arq_json = open('create_protein.json', 'r', encoding='utf8')
                arq_poke = json.load(arq_json)
                for x in arq_poke:
                    for y in x.keys():
                        list_protein.append(y)
                indice = 1
            except FileNotFoundError:
                start = [{'':0}]
                with open('create_protein.json', 'w', encoding= 'utf8') as f:
                        json.dump(start, f, indent=2)
                        f.close()

            def insert_option(option, control_place, variable):
                try:
                    variable = Spinbox(self.pag1, text=option,
                    highlightbackground='snow', activebackground='snow', activeforeground='blue4', relief=FLAT,
                    anchor='w', background='snow')
                    variable.place(relx=0.45, rely=control_place, relwidth=0.15, relheight=0.1)
                except Exception as e:
                    print(e)

            place_protein = 0.25
            for option in list_protein:
                if option == '':
                    pass
                else:
                    insert_option(option, place_protein, indice)
                place_protein += 0.10
                indice += 1
            
            self.prot1 = IntVar(self.root_make)
            self.prot2 = IntVar(self.root_make)
            self.prot3 = IntVar(self.root_make)
            self.prot4 = IntVar(self.root_make)

            bt_avancar = Image.open('Imagens/avancar.png')
            img_avancar = ImageTk.PhotoImage(bt_avancar)
            pag2 = Button(self.pag1, image= img_avancar, compound=CENTER, activebackground='lightblue',
            command=lambda:[])
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
                messagebox.showerror('MAKE IT incompleto', 'Escolha no m??ximo 4 op????es do MAKE IT')
                self.make_it.clear()
            elif tamanho == 0:
                messagebox.showerror('MAKE IT incompleto', 'Escolha no min??mo 1 op????o do MAKE IT')
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
        escolha_make = Label(self.pag2, text='Escolha at?? 4', foreground='blue', anchor='w')
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
        highlightbackground='snow', activebackground='lightblue', command=lambda:[self.make_dish()])
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
        op_top4 = Checkbutton(top_master, text='Amend??as', anchor='w', variable= top4,
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
        op_top7 = Checkbutton(top_master, text='Semente de ab??bora', anchor='w', variable= top7,
        highlightbackground='snow', activeforeground='blue4', activebackground='snow')
        op_top7.place(relx=0.1, rely=0.55, relwidth=0.55, relheight=0.1)
        op_top7.configure(background='snow')
        op_top8 = Checkbutton(top_master, text='Linha??a dourada', anchor='w', variable= top8,
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
                    messagebox.showerror('ERRO', 'Selecione apenas 1 op????o de crunch it')
                    self.crunch_it.clear()
                    self.top_it.clear()
                elif len(self.crunch_it) == 0:
                    messagebox.showerror('ERRO', 'Selecione no min??mo 1 op????o de crunch it')
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
                    messagebox.showerror('ERRO', 'Selecione apenas 1 op????o de top it')
                    self.top_it.clear()
                    self.crunch_it.clear()
                elif len(self.top_it) == 0:
                    messagebox.showerror('ERRO', 'Selecione 1 op????o de top it')
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

        op_finish1 = Checkbutton(self.pag4, text='Shoyo cl??ssico', anchor='w',
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
        op_finish5 = Checkbutton(self.pag4, text='Tar??', anchor='w',
        variable= finish5, highlightbackground='snow', activeforeground='blue4',
        activebackground='snow')
        op_finish5.configure(background='snow')
        op_finish5.place(relx=0.05, rely=0.65, relwidth=0.3, relheight=0.1)
        op_finish6 = Checkbutton(self.pag4, text='Tar?? de laranja', anchor='w',
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
                    messagebox.showerror('ERRO', "Selecione apenas 1 op????o de finish it")
                    self.finish_it.clear()
                elif len(self.finish_it) == 0:
                    messagebox.showerror('ERRO', 'Selecione no min??mo 1 op????o de finish it')
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
