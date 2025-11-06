
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# Esta classe representa a JANELA de cadastro de funcionários
# Ela será chamada a partir do menu principal
class JanelaFuncionarios:
    
    def __init__(self, root_pai):
        # Cria uma janela "filha" (Toplevel) sobre a janela "pai" (root_pai)
        self.top = tk.Toplevel(root_pai)
        self.top.title("Cadastro de Funcionários")
        self.top.geometry("600x450")
        
        # Conexão com o banco de dados
        self.conn = sqlite3.connect('loja.db')
        self.cursor = self.conn.cursor()

        # --- Widgets de Entrada (Formulário) ---
        form = ttk.Frame(self.top, padding="10")
        form.pack(fill=tk.X)

        # Matrícula
        ttk.Label(form, text="Matrícula (Chave):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_matricula = ttk.Entry(form, width=30)
        self.entry_matricula.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        # Nome
        ttk.Label(form, text="Nome:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_nome = ttk.Entry(form, width=50)
        self.entry_nome.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # Cargo
        ttk.Label(form, text="Cargo:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_cargo = ttk.Entry(form, width=30)
        self.entry_cargo.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        # --- Botões de Ação ---
        botoes = ttk.Frame(self.top, padding="10")
        botoes.pack(fill=tk.X)

        ttk.Button(botoes, text="Salvar Novo", command=self.salvar_funcionario).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes, text="Buscar por Matrícula", command=self.buscar_funcionario).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes, text="Atualizar", command=self.atualizar_funcionario).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes, text="Excluir", command=self.excluir_funcionario).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes, text="Limpar", command=self.limpar_campos).pack(side=tk.LEFT, padx=5)

        # --- Tabela (Treeview) para mostrar funcionários ---
        tabela = ttk.Frame(self.top, padding="10")
        tabela.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(tabela, columns=('Matrícula', 'Nome', 'Cargo'), show='headings')
        self.tree.heading('Matrícula', text='Matrícula')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('Cargo', text='Cargo')

        # Barras de rolagem
        scrollbar_y = ttk.Scrollbar(tabela, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(tabela, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Carregar os dados na inicialização
        self.carregar_dados()

    def limpar_campos(self):
        self.entry_matricula.delete(0, tk.END)
        self.entry_nome.delete(0, tk.END)
        self.entry_cargo.delete(0, tk.END)

    def carregar_dados(self):
        # Limpa a árvore antes de carregar
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        # Busca dados no DB e insere na árvore
        self.cursor.execute("SELECT matricula, nome, cargo FROM funcionarios")
        for row in self.cursor.fetchall():
            self.tree.insert('', tk.END, values=row)

    def salvar_funcionario(self):
        matricula = self.entry_matricula.get()
        nome = self.entry_nome.get()
        cargo = self.entry_cargo.get()

        if not matricula or not nome:
            messagebox.showerror("Erro", "Matrícula e Nome são obrigatórios.", parent=self.top)
            return

        try:
            # Tenta inserir o novo funcionário
            self.cursor.execute("INSERT INTO funcionarios (matricula, nome, cargo) VALUES (?, ?, ?)", 
                                (matricula, nome, cargo))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Funcionário salvo!", parent=self.top)
            self.limpar_campos()
            self.carregar_dados() # Atualiza a tabela
        except sqlite3.IntegrityError:
            # Isso acontece se a matrícula (CHAVE PRIMÁRIA) já existir
            messagebox.showerror("Erro", f"A matrícula '{matricula}' já existe!", parent=self.top)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}", parent=self.top)

    def buscar_funcionario(self):
        matricula = self.entry_matricula.get()
        if not matricula:
            messagebox.showerror("Erro", "Digite uma matrícula para buscar.", parent=self.top)
            return
        
        self.cursor.execute("SELECT nome, cargo FROM funcionarios WHERE matricula = ?", (matricula,))
        resultado = self.cursor.fetchone() # Pega o primeiro (e único) resultado

        if resultado:
            self.limpar_campos()
            self.entry_matricula.insert(0, matricula)
            self.entry_nome.insert(0, resultado[0]) # resultado[0] é o nome
            self.entry_cargo.insert(0, resultado[1]) # resultado[1] é o cargo
        else:
            messagebox.showinfo("Não encontrado", "Nenhum funcionário com essa matrícula.", parent=self.top)

    def atualizar_funcionario(self):
        matricula = self.entry_matricula.get()
        nome = self.entry_nome.get()
        cargo = self.entry_cargo.get()

        if not matricula:
            messagebox.showerror("Erro", "Use 'Buscar' para carregar um funcionário antes de atualizar.", parent=self.top)
            return

        try:
            self.cursor.execute("UPDATE funcionarios SET nome = ?, cargo = ? WHERE matricula = ?", 
                                (nome, cargo, matricula))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Dados do funcionário atualizados!", parent=self.top)
            self.limpar_campos()
            self.carregar_dados()
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}", parent=self.top)

    def excluir_funcionario(self):
        matricula = self.entry_matricula.get()
        if not matricula:
            messagebox.showerror("Erro", "Use 'Buscar' para carregar um funcionário antes de excluir.", parent=self.top)
            return

        # Pergunta de confirmação
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir {self.entry_nome.get()}?", parent=self.top):
            try:
                self.cursor.execute("DELETE FROM funcionarios WHERE matricula = ?", (matricula,))
                self.conn.commit()
                messagebox.showinfo("Sucesso", "Funcionário excluído.", parent=self.top)
                self.limpar_campos()
                self.carregar_dados()
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro: {e}", parent=self.top)
