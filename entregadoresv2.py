import psycopg2


class Entregador:
    def __init__(self):
        self.conectar_func()
        self.standard()

    def conectar_func(self):
        conn = psycopg2.connect('dbname=restaurante user=Programador-mestre password=6cVMAj1B')
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS funcionarios(Id_bairro serial ,
                    Nome_func varchar(250) PRIMARY KEY, Entregas int, pagar int)""")
        conn.commit()
        return conn
    
    def standard(self):
        conn = self.conectar_func()
        c = conn.cursor()
        c.execute('''SELECT nome_func FROM funcionarios''')
        number = c.fetchall()
        default = 'Retirada'
        for x in number:
            registred = []
            registred.append(x[0])
        if default not in registred:
            c.execute('''INSERT INTO funcionarios(nome_func, Entregas, pagar)
                    VALUES(%s, %s, %s)''', ('Retirada', 0, 0))
            conn.commit()
        conn.close()

    def cadastrar(self, nome):
        conn = self.conectar_func()
        c = conn.cursor()
        c.execute("""INSERT INTO funcionarios(nome_func, Entregas, pagar)
                  VALUES(%s, %s, %s)""", (nome, 0, 0))
        conn.commit()
        conn.close()

    def apagar_func(self, nome):
        conn = self.conectar_func()
        c = conn.cursor()
        c.execute("""DELETE FROM funcionarios WHERE nome_func = %s""", (nome,))
        conn.commit()
        conn.close()

    def add_tele(self, nome, tele):
        conn = self.conectar_func()
        c = conn.cursor()
        c.execute('SELECT entregas, pagar FROM funcionarios WHERE nome_func = %s', (nome,))
        for x, y in c.fetchall():
            soma = x[0] + 1
            pagar = y[0] + tele
            c.execute("""UPDATE funcionarios SET Entregas = %s WHERE Nome_func = %s""", (soma, nome))
            c.execute("""UPDATE funcionarios SET pagar = %s WHERE Nome_func = %s""", (pagar, nome))

        conn.commit()
        conn.close()

    def consultar(self):
        conn = self.conectar_func()
        c = conn.cursor()
        c.execute("""SELECT * FROM funcionarios""")
        boy = c.fetchall()
        print(boy)

    def limpa(self, nome, endereco, boy):
            nome.delete(0, 'end')
            endereco.delete(0, 'end')
            boy.delete(0, 'end')

e = Entregador()
e