
import tkinter as tk
from tkinter import ttk
import sqlite3

# Esta classe representa a JANELA de Relatórios
class JanelaRelatorios:
    
    def __init__(self, root_pai):
        self.top = tk.Toplevel(root_pai)
        self.top.title("Relatórios do Sistema")
        self.top.geometry("900x600")
        
        self.conn = sqlite3.connect('loja.db')
        self.cursor = self.conn.cursor()

        # --- Layout da Janela ---
        # 1. Topo: Botões de seleção de relatório
        # 2. Baixo: Tabela (Treeview) para mostrar os dados

        self.controles()
        self.display()

    # --- Parte 1: Botões de Controle ---
    def controles(self):
        controles = ttk.Frame(self.top, padding="10")
        controles.pack(fill=tk.X)

        ttk.Label(controles, text="Selecione o Relatório:", font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=10)

        # Botão Relatório 1
        btn_vendas_dia = ttk.Button(controles, text="Vendas do Dia", command=self.gerar_relatorio_vendas_dia)
        btn_vendas_dia.pack(side=tk.LEFT, padx=5)

        # Botão Relatório 2
        btn_estoque_baixo = ttk.Button(controles, text="Estoque Baixo (<= 10)", command=self.gerar_relatorio_estoque_baixo)
        btn_estoque_baixo.pack(side=tk.LEFT, padx=5)

        # Botão Relatório 3
        btn_itens_vendidos = ttk.Button(controles, text="Itens Vendidos (Detalhado)", command=self.gerar_relatorio_itens_vendidos)
        btn_itens_vendidos.pack(side=tk.LEFT, padx=5)

    # --- Parte 2: Display (Tabela) ---
    def display(self):
        display = ttk.Frame(self.top, padding="10")
        display.pack(fill=tk.BOTH, expand=True)

        # Título do Relatório (será atualizado)
        self.label_titulo_relatorio = ttk.Label(display, text="Nenhum relatório selecionado", font=('Arial', 14))
        self.label_titulo_relatorio.pack(pady=5)

        # A Treeview será configurada dinamicamente
        self.tree = ttk.Treeview(display, columns=(), show='headings')
        
        scrollbar_y = ttk.Scrollbar(display, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(display, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)

    # --- Funções Auxiliares ---

    def _configurar_treeview(self, colunas_dict):
        """
        Limpa e reconfigura a Treeview (tabela) com novas colunas.
        colunas_dict: Um dicionário como {'id_coluna': 'Título da Coluna'}
        """
        # Limpa dados antigos
        self.tree.delete(*self.tree.get_children())
        
        # Define as novas colunas
        self.tree['columns'] = tuple(colunas_dict.keys())
        
        # Configura os cabeçalhos (headings) e larguras
        for col_id, col_titulo in colunas_dict.items():
            self.tree.heading(col_id, text=col_titulo)
            # Define larguras (pode ser ajustado)
            if col_id in ('nome', 'produto', 'cliente'):
                self.tree.column(col_id, width=250)
            elif col_id in ('id', 'qtd'):
                self.tree.column(col_id, width=80, anchor=tk.CENTER)
            else:
                self.tree.column(col_id, width=120)

    # --- Lógica dos Relatórios (SQL) ---

    def gerar_relatorio_vendas_dia(self):
        self.label_titulo_relatorio.config(text="Relatório: Vendas de Hoje")
        
        # 1. Configura a tabela para este relatório
        colunas = {
            'id_venda': 'ID Venda',
            'data': 'Data',
            'hora': 'Hora',
            'cliente': 'Cliente',
            'total': 'Total (R$)'
        }
        self._configurar_treeview(colunas)

        # 2. Busca os dados no DB
        # 'localtime' ajusta para o fuso horário local
        query = """
        SELECT 
            v.id_venda,
            DATE(v.data_venda, 'localtime'),
            TIME(v.data_venda, 'localtime'),
            COALESCE(c.nome, 'Cliente Não Informado'),
            v.total
        FROM vendas AS v
        LEFT JOIN clientes AS c ON v.id_cliente = c.identificador
        WHERE DATE(v.data_venda, 'localtime') = DATE('now', 'localtime')
        ORDER BY v.data_venda DESC
        """
        self.cursor.execute(query)
        
        # 3. Insere os dados na tabela
        for row in self.cursor.fetchall():
            # Formata o total para R$
            valores = list(row)
            valores[4] = f"{row[4]:.2f}"
            self.tree.insert('', tk.END, values=valores)

    def gerar_relatorio_estoque_baixo(self):
        self.label_titulo_relatorio.config(text="Relatório: Produtos com Estoque Baixo (10 ou menos)")
        
        colunas = {
            'id': 'ID Produto',
            'nome': 'Nome do Produto',
            'qtd': 'Quantidade Restante'
        }
        self._configurar_treeview(colunas)

        # Vamos definir "estoque baixo" como <= 10 unidades
        query = "SELECT id_produto, nome_produto, quantidade FROM estoque WHERE quantidade <= 10 ORDER BY quantidade ASC"
        
        self.cursor.execute(query)
        
        for row in self.cursor.fetchall():
            self.tree.insert('', tk.END, values=row)

    def gerar_relatorio_itens_vendidos(self):
        self.label_titulo_relatorio.config(text="Relatório: Itens Vendidos (Geral)")
        
        colunas = {
            'venda': 'ID Venda',
            'produto': 'Produto Vendido',
            'qtd': 'Qtd',
            'preco_unit': 'Preço Unit. (R$)',
            'total_item': 'Total Item (R$)'
        }
        self._configurar_treeview(colunas)

        query = """
        SELECT 
            iv.id_venda,
            e.nome_produto,
            iv.quantidade,
            iv.preco_unitario,
            (iv.quantidade * iv.preco_unitario) AS total_item
        FROM itens_venda AS iv
        JOIN estoque AS e ON iv.id_produto = e.id_produto
        ORDER BY iv.id_venda DESC
        """
        self.cursor.execute(query)
        
        for row in self.cursor.fetchall():
            # Formata os preços
            valores = list(row)
            valores[3] = f"{row[3]:.2f}" # Preço Unit.
            valores[4] = f"{row[4]:.2f}" # Total Item
            self.tree.insert('', tk.END, values=valores)
