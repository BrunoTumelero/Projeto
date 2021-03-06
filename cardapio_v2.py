
import psycopg2
from PIL import Image, ImageTk


class Cardapio():
    def conectar_cardapio(self):
        conn = psycopg2.connect('dbname=restaurante user=Programador-mestre password=6cVMAj1B')
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS Menu(Id_prato SERIAL,
                  nome_prato varchar(250) PRIMARY KEY, valor_prato integer NOT NULL,
                  categoria varchar(255) NOT NULL)""")
        conn.commit()
        return conn
    
    def adicionar(self, prato, valor, categoria):
        conn = self.conectar_cardapio()
        c = conn.cursor()
        c.execute('INSERT INTO Menu(nome_Prato, Valor_prato, categoria) VALUES(%s, %s, %s)',
                        (prato, valor, categoria))

        conn.commit()
        conn.close()

    def apagar(self, prato):
        conn = self.conectar_cardapio()
        c = conn.cursor()
        c.execute('DELETE FROM Menu WHERE nome_prato = %s', (prato, ))
        conn.commit()
        conn.close()

    def atualizar(self, prato, valor, category):
        conn = self.conectar_cardapio()
        c = conn.cursor()
        c.execute("""UPDATE menu SET valor_prato = %s WHERE nome_prato = %s""", (valor, prato))
        c.execute("""UPDATE menu SET categoria = %s WHERE nome_prato = %s""", (category, prato))
        conn.commit()
        conn.close()

    def exibir_pratos(self):
        conn = self.conectar_cardapio()
        c = conn.cursor()
        c.execute('SELECT * FROM menu')
        for i in c.fetchall():
            print(i)
            
        conn.close()

    def limpa(self, nome, valor, cetegory):
        nome.delete(0, 'end')
        valor.delete(0, 'end')
        cetegory.delete(0, 'end')

class Modelo_prato():
    def __init__(self):
        self.prato = None
        self.quantidade = None

    def set_prato(self, prato):
        self.prato = prato

    def set_quantidade(sefl, quantidade):
        sefl.quantidade = quantidade

    def get_prato(self):
        return self.prato

    def get_quantidade(self):
        return self.quantidade



