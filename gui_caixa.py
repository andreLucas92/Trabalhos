
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Esta classe representa a JANELA do Ponto de Venda (Caixa)
class JanelaCaixa:
    
    def __init__(self, root_pai):
        self.top = tk.Toplevel(root_pai)
        self.top.title("Caixa")
        self.top.geometry("900x600")
        
        self.conn = sqlite3.connect('loja.db')
        self.cursor = self.conn.cursor()

        # --- Variáveis de Estado da Venda ---
        self.carrinho = [] # Lista para guardar os itens da venda atual
        self.total_venda = 0.0

        # --- Layout da Janela ---
        # A janela será dividida em 3 partes:
        # 1. Topo: Adicionar Produtos
        # 2. Meio: Carrinho (Tabela)
        # 3. Baixo: Finalização e Total

        self.adicionar()
        self.carrinho_()
        self.finalizar()

    # --- Parte 1: Frame de Adicionar Itens ---
    def adicionar(self):
        adicionar = ttk.Frame(self.top, padding="10")
        adicionar.pack(fill=tk.X)

        ttk.Label(adicionar, text="ID do Produto:", font=('Arial', 12)).grid(row=0, column=0, padx=5, pady=5)
        self.entry_produto_id = ttk.Entry(adicionar, width=10, font=('Arial', 12))
        self.entry_produto_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(adicionar, text="Qtd:", font=('Arial', 12)).grid(row=0, column=2, padx=5, pady=5)
        self.entry_produto_qtd = ttk.Entry(adicionar, width=5, font=('Arial', 12))
        self.entry_produto_qtd.grid(row=0, column=3, padx=5, pady=5)
        self.entry_produto_qtd.insert(0, "1") # Quantidade padrão é 1

        ttk.Button(adicionar, text="Adicionar Item", command=self.adicionar_item).grid(row=0, column=4, padx=10, pady=5)
        
        # Labels para mostrar o produto encontrado
        self.label_produto_nome = ttk.Label(adicionar, text="Produto:", font=('Arial', 10, 'italic'))
        self.label_produto_nome.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=5)
        self.label_produto_preco = ttk.Label(adicionar, text="Preço: R$", font=('Arial', 10, 'italic'))
        self.label_produto_preco.grid(row=1, column=2, columnspan=2, sticky=tk.W, padx=5)

    # --- Parte 2: Frame do Carrinho (Tabela) ---
    def carrinho_(self):
        carrinho_ = ttk.Frame(self.top, padding="10")
        carrinho_.pack(fill=tk.BOTH, expand=True)

        ttk.Label(carrinho_, text="Carrinho de Compras", font=('Arial', 14, 'bold')).pack(pady=5)
        
        self.tree = ttk.Treeview(carrinho_, columns=('ID', 'Produto', 'Qtd', 'Preço Unit.', 'Total Item'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Produto', text='Produto')
        self.tree.heading('Qtd', text='Qtd')
        self.tree.heading('Preço Unit.', text='Preço Unit.')
        self.tree.heading('Total Item', text='Total Item')

        self.tree.column('ID', width=50)
        self.tree.column('Produto', width=300)
        self.tree.column('Qtd', width=50, anchor=tk.CENTER)
        self.tree.column('Preço Unit.', width=100, anchor=tk.E)
        self.tree.column('Total Item', width=100, anchor=tk.E)

        scrollbar_y = ttk.Scrollbar(carrinho_, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

    # --- Parte 3: Frame de Finalização ---
    def finalizar(self):
        finalizar = ttk.Frame(self.top, padding="10")
        finalizar.pack(fill=tk.X)

        # Lado Esquerdo: Cliente
        frame_cliente = ttk.Frame(finalizar)
        frame_cliente.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        ttk.Label(frame_cliente, text="Cliente (Email/Telefone, opcional):").pack(anchor=tk.W)
        self.entry_cliente_id = ttk.Entry(frame_cliente, width=30)
        self.entry_cliente_id.pack(anchor=tk.W)

        # Lado Direito: Total e Botões
        frame_total = ttk.Frame(finalizar)
        frame_total.pack(side=tk.RIGHT, padx=10)

        self.label_total_venda = ttk.Label(frame_total, text="Total: R$ 0.00", font=('Arial', 18, 'bold'))
        self.label_total_venda.pack(pady=10, anchor=tk.E)
        
        btn_finalizar = ttk.Button(frame_total, text="Finalizar Venda", command=self.finalizar_venda, style='Accent.TButton')
        btn_finalizar.pack(side=tk.LEFT, padx=10)
        
        btn_cancelar = ttk.Button(frame_total, text="Cancelar Venda", command=self.limpar_venda)
        btn_cancelar.pack(side=tk.LEFT)
        
        # Estilo para o botão de finalizar
        s = ttk.Style()
        s.configure('Accent.TButton', font=('Arial', 12, 'bold'), padding=10)

    # --- Lógica do PDV ---

    def adicionar_item(self):
        try:
            id_produto = int(self.entry_produto_id.get())
            quantidade_pedida = int(self.entry_produto_qtd.get())
        except ValueError:
            messagebox.showerror("Erro", "ID do Produto e Quantidade devem ser números.", parent=self.top)
            return

        if quantidade_pedida <= 0:
            messagebox.showerror("Erro", "Quantidade deve ser maior que zero.", parent=self.top)
            return

        # Busca o produto no banco de dados (estoque)
        self.cursor.execute("SELECT nome_produto, preco_venda, quantidade FROM estoque WHERE id_produto = ?", (id_produto,))
        produto = self.cursor.fetchone()

        if not produto:
            messagebox.showerror("Erro", "Produto não encontrado.", parent=self.top)
            self.label_produto_nome.config(text="Produto:")
            self.label_produto_preco.config(text="Preço: R$")
            return
            
        nome_produto, preco_venda, qtd_estoque = produto
        
        # Atualiza os labels para o usuário ver
        self.label_produto_nome.config(text=f"Produto: {nome_produto}")
        self.label_produto_preco.config(text=f"Preço: R$ {preco_venda:.2f}")

        # Verifica se há estoque suficiente
        if qtd_estoque < quantidade_pedida:
            messagebox.showerror("Estoque Insuficiente", f"Estoque disponível para '{nome_produto}': {qtd_estoque} unidades.", parent=self.top)
            return

        # Adiciona o item ao carrinho (lista interna)
        total_item = preco_venda * quantidade_pedida
        item_carrinho = {
            "id": id_produto,
            "nome": nome_produto,
            "qtd": quantidade_pedida,
            "preco_unit": preco_venda,
            "total_item": total_item
        }
        self.carrinho.append(item_carrinho)
        
        # Atualiza a tela (tabela e total)
        self._atualizar_carrinho_treeview()
        self._atualizar_total_venda()
        
        # Limpa os campos de entrada do produto
        self.entry_produto_id.delete(0, tk.END)
        self.entry_produto_qtd.delete(0, tk.END)
        self.entry_produto_qtd.insert(0, "1")
        self.entry_produto_id.focus() # Move o cursor de volta para o ID

    def _atualizar_carrinho_treeview(self):
        # Limpa a tabela
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        # Preenche a tabela com os itens do self.carrinho
        for item in self.carrinho:
            self.tree.insert('', tk.END, values=(
                item['id'], 
                item['nome'], 
                item['qtd'], 
                f"{item['preco_unit']:.2f}",
                f"{item['total_item']:.2f}"
            ))

    def _atualizar_total_venda(self):
        self.total_venda = sum(item['total_item'] for item in self.carrinho)
        self.label_total_venda.config(text=f"Total: R$ {self.total_venda:.2f}")

    def limpar_venda(self):
        # Limpa o estado interno
        self.carrinho = []
        self.total_venda = 0.0
        
        # Limpa a interface
        self._atualizar_carrinho_treeview()
        self._atualizar_total_venda()
        
        self.entry_cliente_id.delete(0, tk.END)
        self.entry_produto_id.delete(0, tk.END)
        self.entry_produto_qtd.delete(0, tk.END)
        self.entry_produto_qtd.insert(0, "1")
        self.label_produto_nome.config(text="Produto:")
        self.label_produto_preco.config(text="Preço: R$")

    def finalizar_venda(self):
        if not self.carrinho:
            messagebox.showerror("Erro", "Carrinho vazio. Adicione pelo menos um item.", parent=self.top)
            return

        id_cliente = self.entry_cliente_id.get()
        id_cliente_db = None # Começa como Nulo (None)

        # 1. Valida o cliente (se foi digitado)
        if id_cliente:
            self.cursor.execute("SELECT nome FROM clientes WHERE identificador = ?", (id_cliente,))
            cliente = self.cursor.fetchone()
            if not cliente:
                messagebox.showerror("Cliente não encontrado", 
                                     "O Cliente (Email/Telefone) não foi encontrado. \n"
                                     "Cadastre o cliente primeiro ou deixe o campo em branco.",
                                     parent=self.top)
                return
            id_cliente_db = id_cliente # Cliente é válido
            
        data_agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            # --- Início da Transação ---
            
            # 2. Grava na tabela 'vendas'
            self.cursor.execute("""
                INSERT INTO vendas (data_venda, id_cliente, total) 
                VALUES (?, ?, ?)
            """, (data_agora, id_cliente_db, self.total_venda))
            
            # Pega o ID da venda que acabamos de criar
            id_venda_criada = self.cursor.lastrowid

            # 3. Grava na tabela 'itens_venda' (um por um)
            # 4. Atualiza (baixa) o 'estoque' (um por um)
            for item in self.carrinho:
                # 3. Grava o item
                self.cursor.execute("""
                    INSERT INTO itens_venda (id_venda, id_produto, quantidade, preco_unitario)
                    VALUES (?, ?, ?, ?)
                """, (id_venda_criada, item['id'], item['qtd'], item['preco_unit']))
                
                # 4. Atualiza o estoque
                self.cursor.execute("""
                    UPDATE estoque 
                    SET quantidade = quantidade - ? 
                    WHERE id_produto = ?
                """, (item['qtd'], item['id']))

            # 5. Confirma a Transação (Commita tudo)
            self.conn.commit()
            
            # --- Fim da Transação ---

            messagebox.showinfo("Sucesso", f"Venda (ID: {id_venda_criada}) finalizada com sucesso!", parent=self.top)
            self.limpar_venda() # Limpa tudo para a próxima venda

        except sqlite3.Error as e:
            # Se algo der errado (ex: o estoque ficou negativo no meio),
            # o banco de dados desfaz tudo (rollback)
            self.conn.rollback() # Desfaz as mudanças
            messagebox.showerror("Erro na Transação", f"Ocorreu um erro ao salvar a venda: {e}", parent=self.top)
