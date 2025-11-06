
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# Esta classe representa a JANELA de Controle de Estoque
class JanelaEstoque:
    
    def __init__(self, root_pai):
        self.top = tk.Toplevel(root_pai)
        self.top.title("Controle de Estoque de Produtos")
        self.top.geometry("800x500") # Janela um pouco maior
        
        self.conn = sqlite3.connect('loja.db')
        self.cursor = self.conn.cursor()

        # --- Widgets de Entrada (Formulário) ---
        frame_form = ttk.Frame(self.top, padding="10")
        frame_form.pack(fill=tk.X)

        # ID do Produto (Usado para buscar/atualizar/excluir)
        # Este campo será preenchido automaticamente ao buscar ou salvar
        ttk.Label(frame_form, text="ID do Produto:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_id = ttk.Entry(frame_form, width=10, state="readonly") # Bloqueado para edição
        self.entry_id.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        # Nome do Produto
        ttk.Label(frame_form, text="Nome do Produto:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_nome = ttk.Entry(frame_form, width=50)
        self.entry_nome.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # Quantidade
        ttk.Label(frame_form, text="Quantidade em Estoque:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_quantidade = ttk.Entry(frame_form, width=15)
        self.entry_quantidade.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        # Preço de Venda
        ttk.Label(frame_form, text="Preço de Venda (R$):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_preco = ttk.Entry(frame_form, width=15)
        self.entry_preco.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

        # --- Botões de Ação ---
        botoes = ttk.Frame(self.top, padding="10")
        botoes.pack(fill=tk.X)

        ttk.Button(botoes, text="Salvar Novo Produto", command=self.salvar_produto).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes, text="Buscar por ID", command=self.buscar_produto).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes, text="Atualizar Produto", command=self.atualizar_produto).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes, text="Excluir Produto", command=self.excluir_produto).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes, text="Limpar Campos", command=self.limpar_campos).pack(side=tk.LEFT, padx=5)
        
        # --- Tabela (Treeview) para mostrar o estoque ---
        tabela = ttk.Frame(self.top, padding="10")
        tabela.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(tabela, columns=('ID', 'Nome', 'Qtd', 'Preço'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nome', text='Nome do Produto')
        self.tree.heading('Qtd', text='Quantidade')
        self.tree.heading('Preço', text='Preço (R$)')

        # Largura das colunas
        self.tree.column('ID', width=50)
        self.tree.column('Nome', width=300)
        self.tree.column('Qtd', width=80)
        self.tree.column('Preço', width=100)

        # Barras de rolagem
        scrollbar_y = ttk.Scrollbar(tabela, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(tabela, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Carregar os dados na inicialização
        self.carregar_dados()

    def _validar_campos(self):
        """Função interna para validar os campos de quantidade e preço."""
        nome = self.entry_nome.get()
        if not nome:
            messagebox.showerror("Erro", "O Nome do Produto é obrigatório.", parent=self.top)
            return False
            
        try:
            # Tenta converter para número
            int(self.entry_quantidade.get())
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro.", parent=self.top)
            return False

        try:
            # Tenta converter para número (float). Substitui vírgula por ponto.
            preco_str = self.entry_preco.get().replace(',', '.')
            float(preco_str)
        except ValueError:
            messagebox.showerror("Erro", "Preço de Venda deve ser um número (ex: 19.90).", parent=self.top)
            return False
            
        return True

    def limpar_campos(self):
        # Habilita o campo ID para limpá-lo, depois desabilita
        self.entry_id.config(state="normal")
        self.entry_id.delete(0, tk.END)
        self.entry_id.config(state="readonly")
        
        self.entry_nome.delete(0, tk.END)
        self.entry_quantidade.delete(0, tk.END)
        self.entry_preco.delete(0, tk.END)

    def carregar_dados(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        self.cursor.execute("SELECT id_produto, nome_produto, quantidade, preco_venda FROM estoque")
        for row in self.cursor.fetchall():
            # Formata o preço para exibição
            preco_formatado = f"{row[3]:.2f}"
            self.tree.insert('', tk.END, values=(row[0], row[1], row[2], preco_formatado))

    def salvar_produto(self):
        # Valida os campos antes de continuar
        if not self._validar_campos():
            return

        nome = self.entry_nome.get()
        quantidade = int(self.entry_quantidade.get())
        preco = float(self.entry_preco.get().replace(',', '.'))

        try:
            self.cursor.execute("INSERT INTO estoque (nome_produto, quantidade, preco_venda) VALUES (?, ?, ?)", 
                                (nome, quantidade, preco))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Produto salvo!", parent=self.top)
            self.limpar_campos()
            self.carregar_dados()
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}", parent=self.top)

    def buscar_produto(self):
        # Para buscar, vamos temporariamente habilitar o campo ID para o usuário digitar
        id_str = self.entry_id.get()
        if not id_str:
            # Se o campo ID estiver vazio, pedimos para o usuário
            # Usamos um SimpleDialog para isso (um pop-up que pede um valor)
            id_produto = tk.simpledialog.askstring("Buscar por ID", 
                                                   "Digite o ID do produto:", 
                                                   parent=self.top)
            if not id_produto:
                return # Usuário cancelou
        else:
            id_produto = id_str

        try:
            self.cursor.execute("SELECT nome_produto, quantidade, preco_venda FROM estoque WHERE id_produto = ?", (int(id_produto),))
            resultado = self.cursor.fetchone()

            if resultado:
                self.limpar_campos()
                # Re-habilita o campo ID para inserir o valor encontrado
                self.entry_id.config(state="normal")
                self.entry_id.insert(0, id_produto)
                self.entry_id.config(state="readonly")
                
                self.entry_nome.insert(0, resultado[0]) # nome
                self.entry_quantidade.insert(0, resultado[1]) # quantidade
                self.entry_preco.insert(0, f"{resultado[2]:.2f}") # preco
            else:
                messagebox.showinfo("Não encontrado", "Nenhum produto com esse ID.", parent=self.top)
        except ValueError:
            messagebox.showerror("Erro", "ID deve ser um número.", parent=self.top)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}", parent=self.top)

    def atualizar_produto(self):
        id_produto = self.entry_id.get()
        if not id_produto:
            messagebox.showerror("Erro", "Use 'Buscar' para carregar um produto antes de atualizar.", parent=self.top)
            return

        # Valida os outros campos
        if not self._validar_campos():
            return

        nome = self.entry_nome.get()
        quantidade = int(self.entry_quantidade.get())
        preco = float(self.entry_preco.get().replace(',', '.'))

        try:
            self.cursor.execute("""
                UPDATE estoque 
                SET nome_produto = ?, quantidade = ?, preco_venda = ? 
                WHERE id_produto = ?
            """, (nome, quantidade, preco, int(id_produto)))
            
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Dados do produto atualizados!", parent=self.top)
            self.limpar_campos()
            self.carregar_dados()
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}", parent=self.top)

    def excluir_produto(self):
        id_produto = self.entry_id.get()
        if not id_produto:
            messagebox.showerror("Erro", "Use 'Buscar' para carregar um produto antes de excluir.", parent=self.top)
            return

        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir o produto '{self.entry_nome.get()}'?", parent=self.top):
            try:
                self.cursor.execute("DELETE FROM estoque WHERE id_produto = ?", (int(id_produto),))
                self.conn.commit()
                messagebox.showinfo("Sucesso", "Produto excluído.", parent=self.top)
                self.limpar_campos()
                self.carregar_dados()
            except Exception as e:
                # NOTA: Se o produto já foi usado em uma venda, o ideal seria
                # apenas "desativar" o produto, e não excluí-lo (por causa
                # das chaves estrangeiras nos relatórios). Mas para este sistema,
                # a exclusão direta funcionará.
                messagebox.showerror("Erro", f"Ocorreu um erro: {e}", parent=self.top)
