from tkinter import *
root=Tk()

class novo:

        def __init__(self, janela):
            self.caixa=Frame(janela)
            self.caixa.grid()
            self.b=Button(janela, text='Abrir', command=self.new_jan)
            self.b.grid()
            self.l1=Label(janela, text='raiz!')
            self.l1.grid()

        def new_jan(self):
            self.jan=Toplevel()
            self.l=Label(self.jan, text='Feche esta para poder voltar a raiz!')
            self.l.grid()
            b=Button(self.jan, text='Fechar', command=self.fecha_jan)
            b.grid()
            self.jan.geometry('300x200')
            self.jan.transient(root)#
            self.jan.focus_force()#
            self.jan.grab_set()#

        def fecha_jan(self):
            self.jan.destroy()


novo(root)

root.geometry('300x200')

root.mainloop()