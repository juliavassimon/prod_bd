import tkinter as tk
from tkinter import ttk
import mysql.connector

class AppBd:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='35020349',
            database='produtos'
        )
        self.cursor = self.conn.cursor()

    def select_data(self):
        self.cursor.execute("SELECT * FROM produto")
        return self.cursor.fetchall()

    def insert_product(self, codigo, nome, preco):
        try:
            query = "INSERT INTO produto (codigo, nome, preco) VALUES (%s, %s, %s)"
            values = (codigo, nome, preco)
            self.cursor.execute(query, values)
            self.conn.commit()
            print('Produto cadastrado com sucesso!')
        except Exception as e:
            print(f'Não foi possível efetuar o cadastro: {e}')

    def update_data(self, codigo, nome, preco):
        try:
            query = "UPDATE produto SET nome = %s, preco = %s WHERE codigo = %s"
            values = (nome, preco, codigo)
            self.cursor.execute(query, values)
            self.conn.commit()
            print('Produto atualizado com sucesso!')
        except Exception as e:
            print(f'Não foi possível fazer a atualização: {e}')

    def delete_data(self, codigo):
        try:
            query = "DELETE FROM produto WHERE codigo = %s"
            values = (codigo,)
            self.cursor.execute(query, values)
            self.conn.commit()
            print('Produto excluído com sucesso!')
        except Exception as e:
            print(f'Não foi possível excluir o produto: {e}')

class Bd:
    def __init__(self, win):
        self.obj_bd = AppBd()
        self.lbCodigo = tk.Label(win, text="Código do Produto:")
        self.lbNome = tk.Label(win, text="Nome do Produto:")
        self.lbPreco = tk.Label(win, text="Preço do Produto:")
        self.txtCodigo = tk.Entry()
        self.txtNome = tk.Entry()
        self.txtPreco = tk.Entry()
        self.btCadastrar = tk.Button(win, text="Cadastrar", command=self.f_cadastrar_produto)
        self.btAtualizar = tk.Button(win, text="Atualizar", command=self.f_atualizar_produto)
        self.btExcluir = tk.Button(win, text="Excluir", command=self.f_excluir_produto)
        self.btLimpar = tk.Button(win, text="Limpar", command=self.f_limpar_tela)
        self.btCalcularAcrescimo = tk.Button(win, text="Calcular 10% de Acréscimo", fg="red", command=self.calcular_acrescimo)
        self.btCalcularAcrescimo.place(x=500, y=200)
        self.dadosColunas = ("Código", "Nome", "Preço")
        self.treeProdutos = ttk.Treeview(win, columns=self.dadosColunas, selectmode='browse')
        self.verscrolbar = ttk.Scrollbar(win, command=self.treeProdutos.yview, orient="vertical")
        self.verscrolbar.pack(side='right', fill='y')
        self.treeProdutos.configure(yscrollcommand=self.verscrolbar.set)
        self.treeProdutos.heading("Código", text="Código")
        self.treeProdutos.heading("Nome", text="Nome")
        self.treeProdutos.heading("Preço", text="Preço")
        self.treeProdutos.column("Código", minwidth=0, width=100)
        self.treeProdutos.column("Nome", minwidth=0, width=100)
        self.treeProdutos.column("Preço", minwidth=0, width=100)
        self.treeProdutos.pack(padx=10, pady=10)
        self.treeProdutos.bind("<<TreeviewSelect>>", self.apresentar_itens_selecionados)
        self.lbCodigo.place(x=100, y=50)
        self.txtCodigo.place(x=250, y=50)
        self.lbNome.place(x=100, y=100)
        self.txtNome.place(x=250, y=100)
        self.lbPreco.place(x=100, y=150)
        self.txtPreco.place(x=250, y=150)
        self.btCadastrar.place(x=100, y=200)
        self.btAtualizar.place(x=200, y=200)
        self.btExcluir.place(x=300, y=200)
        self.btLimpar.place(x=400, y=200)
        self.treeProdutos.place(x=100, y=300)
        self.verscrolbar.place(x=605, y=300, height=225)
        self.carregar_dados_iniciais()
        self.btCalcularAcrescimo = tk.Button(win, text="Calcular 10% de Acréscimo", fg="red", command=self.calcular_acrescimo)
        self.btCalcularAcrescimo.place(x=500, y=200)

    def apresentar_itens_selecionados(self, event):
        self.f_limpar_tela()
        for selection in self.treeProdutos.selection():
            item = self.treeProdutos.item(selection)
            codigo, nome, preco = item["values"]
            self.txtCodigo.insert(0, codigo)
            self.txtNome.insert(0, nome)
            self.txtPreco.insert(0, preco)

    def carregar_dados_iniciais(self):
        try:
            self.id = 0
            self.iid = 0
            registros = self.obj_bd.select_data()
            if registros:
                for item in registros:
                    codigo, nome, preco = item
                    print("Código = ", codigo)
                    print("Nome   = ", nome)
                    print("Preço  = ", preco, '\n')
                    self.treeProdutos.insert('', 'end', iid=self.iid, values=(codigo, nome, preco))
                    self.iid = self.iid + 1
                    self.id = self.id + 1
                print('Dados da Base')
            else:
                print('Nenhum registro encontrado.')
        except Exception as e:
            print(f'Erro ao carregar dados: {e}')

    def f_ler_campos(self):
        codigo = None
        nome = None
        preco = None

        try:
            codigo = int(self.txtCodigo.get())
            nome = self.txtNome.get()
            preco = float(self.txtPreco.get())
            print("Leitura dos dados com sucesso!")
        except Exception as e:
            print(f"Não foi possível carregar os dados: {e}")

        return codigo, nome, preco

    def f_cadastrar_produto(self):
        try:
            codigo, nome, preco = self.f_ler_campos()
            self.obj_bd.insert_product(codigo, nome, preco)
            self.treeProdutos.insert('', 'end', iid=self.iid, values=(codigo, nome, preco))
            self.iid = self.iid + 1
            self.id = self.id + 1
            self.f_limpar_tela()
            print('Produto cadastrado com sucesso!')
        except Exception as e:
            print(f'Não foi possível efetuar o cadastro: {e}')

    def f_atualizar_produto(self):
        try:
            codigo, nome, preco = self.f_ler_campos()
            self.obj_bd.update_data(codigo, nome, preco)
            self.treeProdutos.delete(*self.treeProdutos.get_children())
            self.carregar_dados_iniciais()
            self.f_limpar_tela()
            print('Produto atualizado com sucesso!')
        except Exception as e:
            print(f'Não foi possível fazer a atualização: {e}')

    def f_excluir_produto(self):
        try:
            codigo, _, _ = self.f_ler_campos()
            self.obj_bd.delete_data(codigo)
            self.treeProdutos.delete(*self.treeProdutos.get_children())
            self.carregar_dados_iniciais()
            self.f_limpar_tela()
            print('Produto excluído com sucesso!')
        except Exception as e:
            print(f'Não foi possível excluir o produto: {e}')

    def f_limpar_tela(self):
        self.txtCodigo.delete(0, 'end')
        self.txtNome.delete(0, 'end')
        self.txtPreco.delete(0, 'end')

    def calcular_acrescimo(self):
        try:
            preco_atual = float(self.txtPreco.get())
            novo_preco = preco_atual * 1.10  # Acréscimo de 10%

            selection = self.treeProdutos.selection()
            if selection:
                item = self.treeProdutos.item(selection[0])
                item_values = item["values"]

                item_values[2] = novo_preco
                self.treeProdutos.item(selection[0], values=item_values)

                self.txtPreco.delete(0, 'end')
            else:
                print("Selecione um produto na lista antes de calcular o acréscimo.")

        except Exception as e:
            print(f'Erro ao calcular acréscimo: {e}')

if __name__ == "__main__":
    root = tk.Tk()
    app = Bd(root)
    root.title("Estoque de produtos")
    root.geometry("700x550")
    root.mainloop()
