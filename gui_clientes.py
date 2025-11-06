
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# Esta classe representa a JANELA de cadastro de clientes
class JanelaClientes:
    
    def __init__(self, root_pai):
        self.top = tk.Toplevel(root_pai)
        self.top.title("Cadastro de Clientes")
        self.top.geometry("900x600") # Um pouco mais largo para o identificador
        
        # Conexão com o banco de dados
        self.conn = sqlite3.connect('loja.db')
        self.cursor = self.conn.cursor()

        # --- Widgets de Entrada (Formulário) ---
        form = ttk.Frame(self.top, padding="10")
        form.pack(fill=tk.X)

        # Identificador (Email ou Telefone) - Chave Primária
        ttk.Label(form, text="Email/Telefone (Chave):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_identificador = ttk.Entry(form, width=40)
        self.entry_identificador.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        # Nome
        ttk.Label(form, text="Nome:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_nome = ttk.Entry(form, width=50)
        self.entry_nome.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # --- Botões de Ação ---
        botoes = ttk.Frame(self.top, padding="10")
        botoes.pack(fill=tk.X)

        ttk.Button(botoes, text="Salvar Novo", command=self.salvar_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes, text="Buscar por Email/Telefone", command=self.buscar_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes, text="Atualizar", command=self.atualizar_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes, text="Excluir", command=self.excluir_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes, text="Limpar", command=self.limpar_campos).pack(side=tk.LEFT, padx=5)

        # --- Tabela (Treeview) para mostrar clientes ---
        tabela = ttk.Frame(self.top, padding="10")
        tabela.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(tabela, columns=('Identificador', 'Nome'), show='headings')
        self.tree.heading('Identificador', text='Email ou Telefone')
        self.tree.heading('Nome', text='Nome')

        # Ajuste de largura das colunas
        self.tree.column('Identificador', width=200)
        self.tree.column('Nome', width=300)

        # Barras de rolagem
        scrollbar_y = ttk.Scrollbar(tabela, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Carregar os dados na inicialização
        self.carregar_dados()

    def limpar_campos(self):
        self.entry_identificador.delete(0, tk.END)
        self.entry_nome.delete(0, tk.END)

    def carregar_dados(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        self.cursor.execute("SELECT identificador, nome FROM clientes")
        for row in self.cursor.fetchall():
            self.tree.insert('', tk.END, values=row)

    def salvar_cliente(self):
        identificador = self.entry_identificador.get()
        nome = self.entry_nome.get()

        if not identificador or not nome:
            messagebox.showerror("Erro", "Identificador (Email/Telefone) e Nome são obrigatórios.", parent=self.top)
            return

        try:
            self.cursor.execute("INSERT INTO clientes (identificador, nome) VALUES (?, ?)", 
                                (identificador, nome))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Cliente salvo!", parent=self.top)
            self.limpar_campos()
            self.carregar_dados()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", f"O identificador '{identificador}' já está cadastrado!", parent=self.top)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}", parent=self.top)

    def buscar_cliente(self):
        identificador = self.entry_identificador.get()
        if not identificador:
            messagebox.showerror("Erro", "Digite um Email ou Telefone para buscar.", parent=self.top)
            return
        
        self.cursor.execute("SELECT nome FROM clientes WHERE identificador = ?", (identificador,))
        resultado = self.cursor.fetchone()

        if resultado:
            self.limpar_campos()
            self.entry_identificador.insert(0, identificador)
            self.entry_nome.insert(0, resultado[0]) # resultado[0] é o nome
        else:
            messagebox.showinfo("Não encontrado", "Nenhum cliente com esse identificador.", parent=self.top)

    def atualizar_cliente(self):
        identificador = self.entry_identificador.get()
        nome = self.entry_nome.get()

        if not identificador:
            messagebox.showerror("Erro", "Use 'Buscar' para carregar um cliente antes de atualizar.", parent=self.top)
            return

        try:
            self.cursor.execute("UPDATE clientes SET nome = ? WHERE identificador = ?", 
                                (nome, identificador))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Dados do cliente atualizados!", parent=self.top)
            self.limpar_campos()
            self.carregar_dados()
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}", parent=self.top)

    def excluir_cliente(self):
        identificador = self.entry_identificador.get()
        if not identificador:
            messagebox.showerror("Erro", "Use 'Buscar' para carregar um cliente antes de excluir.", parent=self.top)
            return

        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir {self.entry_nome.get()}?", parent=self.top):
            try:
                self.cursor.execute("DELETE FROM clientes WHERE identificador = ?", (identificador,))
                self.conn.commit()
                messagebox.showinfo("Sucesso", "Cliente excluído.", parent=self.top)
                self.limpar_campos()
                self.carregar_dados()
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro: {e}", parent=self.top)
