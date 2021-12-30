from tkinter import messagebox
import psycopg2

class Cliente:
    def __init__(self):
        self.conectar_cliente()

    def conectar_cliente(self):
        conn = psycopg2.connect('dbname=restaurante user=Programador-mestre password=6cVMAj1B')
        c = conn.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS Clientes(Id_cliente SERIAL,
                  nome_cliente varchar(250) PRIMARY KEY, Endereco varchar(250));""")
        conn.commit()
        return conn

    def mostrar(self):
        conn = self.conectar_cliente()
        c = conn.cursor()
        c.execute('SELECT * FROM clientes')
        for i in c.fetchall():
            print(i)

        conn.close()

    def salvar(self, nome, end):
        try:
            if nome == ' ':
                messagebox.showinfo('ERRO', 'Insira um nome válido')
            else:
                conn = self.conectar_cliente()
                c = conn.cursor()
                c.execute("""INSERT INTO Clientes(Nome_cliente, endereco)
                        VALUES(%s, %s)""", (nome, end))
                
                conn.commit()
                conn.close()
        except:
            messagebox.showwarning('ERRO', 'Cliente já cadastrado')

    def apagar(self, excluir):
        conn = self.conectar_cliente()
        c = conn.cursor()
        c.execute('DELETE FROM Clientes WHERE Id = %s', (excluir, ))

        conn.commit()
        conn.close()

    def atualizar(self, lista):
        conn = self.conectar_cliente()
        c = conn.cursor()
        c.execute("""SELECT cl.nome_cliente, cl.endereco, COUNT(pe.nome_cliente) 
                    FROM clientes as cl
                    JOIN pedidos as pe on cl.nome_cliente = pe.nome_cliente
                    GROUP BY cl.nome_cliente""")
        dados = c.fetchall()

        global contador
        contador = 0

        for dados[0], dados[1], dados[2] in c.fetchall():
            if contador % 2 == 0:
                lista.insert(parent='', index='end', text='',
                               values=(dados[0], dados[1], dados[2]),
                               tags=('evenrow',))

            else:
                lista.insert(parent='', index='end', text='',
                                 values=(dados[0], dados[1], dados[2]),
                                 tags=('oddrow',))
            contador += 1
            conn.close()
        conn.close()

    def limpa(self, nome, endereco):
        nome.delete(0, 'end')
        endereco.delete(0, 'end')
        







    





















