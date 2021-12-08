import psycopg2

class Local:
    def __init__(self):
        self.conectar()
    def conectar(self):
        conn = psycopg2.connect('dbname=restaurante user=Programador-mestre password=6cVMAj1B')
        c = conn.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS Bairros(Id_bairro SERIAL,
                  nome_bairro varchar PRIMARY KEY, preco integer);""")
        conn.commit()
        return conn

    def salvar(self, bairro, valor):
        conn = self.conectar()
        c = conn.cursor()
        c.execute("""INSERT INTO bairros(nome_bairro, preco)
                  VALUES (%s,%s)""", (bairro, valor))
        
        conn.commit()
        conn.close()

    def mostrar(self):
        conn = self.conectar()
        c = conn.cursor()
        c.execute('SELECT * FROM bairros')
        for i in c.fetchall():
            print(i)

    def apagar(self, excluir):
        conn = self.conectar()
        c = conn.cursor()
        c.execute('DELETE FROM Bairros WHERE nome_bairro = %s', (excluir, ))

        conn.commit()
        conn.close()

    def valor_ifood(self):
        return 10

    def retirada(self):
        return 0

    def valor_tele(self, bairro):
        conn = self.conectar()
        c = conn.cursor()
        c.execute("""SELECT preco FROM bairros WHERE nome_bairro = %s""", (bairro,))
        valor = c.fetchall()
        return valor[0][0]

    def limpa(self, nome, valor):
        nome.delete(0, 'end')
        valor.delete(0, 'end')

    def atualiza_valor(self, valor, bairro):
        conn = self.conectar()
        c = conn.cursor()
        c.execute("""UPDATE  bairros SET preco = %s WHERE nome_bairro =  %s""", (valor, bairro))
        conn.commit()
        conn.close()

#l1 = Local()
#l1.conectar()
#l1.salvar('Exposição', 10)
#l1.mostrar()

#l1.apagar()
