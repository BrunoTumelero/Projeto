from tkinter import *
from tkinter import ttk
import json

class teste():
    def __init__(self) -> None:
        self.root = Tk()
        self.root.geometry('500x500')
        self.ap()
        self.lista = []
        self.var = ['a', 'b', 'c', 'd']
        self.root.mainloop()


    def insert_option(self, option, control_place, variable):
        try:
            variable = Checkbutton(self.root, text=option,
            highlightbackground='snow', activebackground='snow', activeforeground='blue4', relief=FLAT,
            anchor='w', background='snow')
            variable.place(relx=0.02, rely=control_place, relwidth=0.25, relheight=0.1)
        except Exception as e:
            print(e)

    def ap(self):
        i = 0
        c = 0.3
        input = Entry(self.root)
        input.grid(column=5, row=20)
        bt = Button(self.root, text= 'add', command=lambda:[self.lista.append(input.get()), input.delete(0, 'end'),
        le(input.get(), i, c)])
        bt.grid()
        def le(input, i , c):
            for x in self.lista:
                self.insert_option(x, c, self.var[i])
                i += 1
                c += 0.2

t = teste()
t