from tkinter import *
from tkinter import ttk
import json

class teste():
    def __init__(self) -> None:
        self.root = Tk()
        self.root.geometry('500x500')
        self.ap
        self.root.mainloop()
        

    def buton(self):
        self.var = BooleanVar(self.root)
        s = Label(self.root, text='Sucesso')
        b = Checkbutton(self.root, text='Verification', variable=self.var, onvalue= True, offvalue=False, 
        command=lambda:[self.check(s)])
        b.place(relx=0.2, rely=0.2, relwidth=0.2, relheight=0.15)

        a = Button(self.root, text='ok', command=lambda:[print(self.var.get())])
        a.grid()

    def ap(self):
        list_control_poke = []
        arq_json = open('create_poke.json', 'r', encoding='utf8')
        arq_poke = json.load(arq_json)
        for x in arq_poke:
            for y in x.keys():
                list_control_poke.append(y)
        indice = 1

        def insert_option(option, control_place, variable):
            try:
                variable = Checkbutton(self.root, text=option,
                highlightbackground='snow', activebackground='snow', activeforeground='blue4', relief=FLAT,
                anchor='w', background='snow')
                variable.place(relx=0.2, rely=control_place, relwidth=0.25, relheight=0.1)
            except Exception as e:
                print(e)
        controle = []
        place = 0.25
        n = 0
        while indice <= len(list_control_poke):
            for key in list_control_poke:
                if key not in controle:
                    controle.append(key)
                    insert_option(controle[n], place, indice)
                    print(controle[n], 'aqui')
            place += 0.10
            indice += 1
            n += 1
        

t = teste()
t  
