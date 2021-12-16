import psycopg2
from tkinter import messagebox

class Pedido:
    def __init__(self):
        self.conectar()
    #conecta ao banco de dados e cria a tabela se não esxistir
    def conectar(self):
        conn = psycopg2.connect('dbname=restaurante user=Programador-mestre password=6cVMAj1B')
        c = conn.cursor()

        c.execute("""create table if not exists pedidos(id_pedido serial,
					nome_cliente varchar(255) references clientes(nome_cliente),
					nome_prato varchar(255) references menu(nome_prato),
					nome_func varchar(255) references funcionarios(nome_func),
                    valor_total integer,
                    tipo_tele integer,
					dia date not null)""")
        conn.commit()
        return conn
    #salva o nome do cliente, endereço e o funcionario que fez a entrega
    def salvar(self, nome, end, func):
        conn = self.conectar()
        c = conn.cursor()
        c.execute("""INSERT INTO Clientes(Id_cliente, Nome_cliente, endereco)
                  VALUES (DEFAULT, %s,%s)""", (nome, end))
        c.execute("""INSERT INTO funcionarios(Nome_func)
                  VALUES (%s)""", (func,))
        
        conn.commit()
        conn.close()
    #Função para fazer novo pedido
    def novo_pedido(self, nome_c, prato, func, tele, tipo, data):
        try:
            conn = self.conectar()
            c = conn.cursor()
            #cria a tabela dos items pedidos
            c.execute("""CREATE TABLE IF NOT EXISTS itens_pedidos(id_pedido integer,
            prato varchar(255), valor integer)""")

            #seleciona o valor do prato pelo id do pedido
            lista_pratos = []
            for i in prato.keys():
                c.execute("""SELECT valor_prato FROM menu 
                    WHERE nome_prato = %s """, (i,))
                valor1 = c.fetchall()
                lista_pratos.append(valor1[0][0])
                self.total_pratos = sum(lista_pratos)
            
            #adiciona a tele para o funcionario
            c.execute('SELECT entregas, pagar FROM funcionarios WHERE nome_func = %s', (func,))
            for x, y in c.fetchall():
                soma = x + 1
                pagar = y + tele
                c.execute("""UPDATE funcionarios SET Entregas = %s WHERE Nome_func = %s""", (soma, func))
                c.execute("""UPDATE funcionarios SET pagar = %s WHERE Nome_func = %s""", (pagar, func))

            conn.commit()
            #soma o valor do prato e da tele
            total = self.total_pratos + tele
        
            c.execute("""INSERT INTO pedidos(nome_cliente, nome_func, valor_total, tipo_tele, dia) 
            VALUES(%s, %s, %s, %s, %s)""", (nome_c, func, total, tipo, data))
            conn.commit()

            #seleciona o id do cliente
            c.execute("""SELECT id_pedido FROM pedidos
                WHERE nome_cliente = %s""", (nome_c,))
            id_p = c.fetchall()
            num_id = id_p[0][0]
            
            contador = 0
            if contador <= len(prato.keys()):
                for p in prato.keys():
                    c.execute("""INSERT INTO itens_pedidos(id_pedido, prato, valor) VALUES(%s, %s, %s)""",
                                (num_id, p, valor1[0][0]))
                    contador += 1
            conn.commit()

            conn.close()
        except AttributeError:
            messagebox.showerror('Pedido', 'Selecione o tipo de entrega')
        except Exception:
            messagebox.showinfo('Info', 'Algo deu errado')

    #selec com as informações de cada pedido
    def seleciona(self):
        conn = self.conectar()
        c = conn.cursor()
        c.execute("""SELECT Id_pedido, pe.nome_cliente, pe.valor_total,
                cl.endereco, 
                f.nome_func, pe.dia
                FROM pedidos as pe
                join clientes as cl on cl.nome_cliente = pe.nome_cliente
                join funcionarios as f on f.nome_func = pe.nome_func
                """)
        
        for i, n, v, b, f, d in c.fetchall():
            print(i, n, v, b, f, d)

        conn.close()
    #limpa as entrys
    def limpa(self, nome, endereco):
        nome.delete(0, 'end')
        endereco.delete(0, 'end')

    def apagar(self, id_pedido):
        conn = self.conectar()
        c = conn.cursor()
        c.execute("""DELETE FROM pedidos WHERE id_pedido = %s""", (id_pedido,))
        conn.commit()
        conn.close()

#p1 = Pedido()
#p1.somar('Dadinhos', 'ucs')
#p1.novo_pedido('Ana paula', 'Poke Bowl', 'Bruno')
#p1.salvar('raquel', 'ucs', 'Amalia')
#p1.somar('Henrique ruaro')
#p1.seleciona()













        
