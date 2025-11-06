
import tkinter as tk
from tkinter import ttk

import gui_funcionarios
import gui_clientes
import gui_estoque
import gui_caixa
import gui_relatorio

# Vamos precisar importar os outros arquivos (que ainda vamos criar)
# import gui_clientes 
# import gui_funcionarios
# ... etc

class AppPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Loja de Roupas")
        self.root.geometry("900x600")

        # Container principal
        frame_principal = ttk.Frame(self.root, padding="20")
        frame_principal.pack(expand=True, fill=tk.BOTH)

        label_titulo = ttk.Label(frame_principal, text="Menu Principal", 
                                 font=("Arial", 24, "bold"))
        label_titulo.pack(pady=20)

        # --- Botões do Menu ---
        
        # Estilo dos botões
        s = ttk.Style()
        s.configure('Menu.TButton', font=('Arial', 14), padding=15)

        # Frame para os botões
        botao = ttk.Frame(frame_principal)
        botao.pack(expand=True)

        # Botão Caixa (Vendas)
        botao_caixa = ttk.Button(botao, text="Caixa", 
                               style='Menu.TButton', command=self.abrir_caixa)
        botao_caixa.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Botão Estoque
        botao_estoque = ttk.Button(botao, text="Estoque", 
                                 style='Menu.TButton', command=self.abrir_estoque)
        botao_estoque.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Botão Clientes
        botao_clientes = ttk.Button(botao, text="Cadastro de Clientes", 
                                  style='Menu.TButton', command=self.abrir_clientes)
        botao_clientes.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Botão Funcionários
        botao_funcionarios = ttk.Button(botao, text="Cadastro de Funcionários", 
                                      style='Menu.TButton', command=self.abrir_funcionarios)
        botao_funcionarios.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        # Botão Relatórios
        botao_relatorios = ttk.Button(botao, text="Relatórios", 
                                    style='Menu.TButton', command=self.abrir_relatorios)
        botao_relatorios.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    # --- Funções para abrir as janelas (módulos) ---
    # (Por enquanto, elas só vão imprimir no console)
    
    def abrir_caixa(self):
        print("Abrindo o Caixa")
        # Aqui chamaremos a janela do Caixa
        # Toplevel(self.root) ... etc.
        janela_caixa = gui_caixa.JanelaCaixa(self.root)
        
    def abrir_estoque(self):
        print("Abrindo o Estoque")
        # Aqui chamaremos a janela do Estoque
        janela_estoque = gui_estoque.JanelaEstoque(self.root)        

    def abrir_clientes(self):
        print("Abrindo o Cadastro de Cliente")
    # Cria uma instância da nossa janela de clientes
        janela_cliente = gui_clientes.JanelaClientes(self.root)

    def abrir_funcionarios(self):
        print("Abrindo o Cadastro de Funcionários")
    # Cria uma instância da nossa janela de funcionários
    # Passando 'self.root' como o "pai"
        janela_funcionario = gui_funcionarios.JanelaFuncionarios(self.root)

    def abrir_relatorios(self):
        print("Abrindo Relatórios") 
    # Cria uma instância da nossa janela de relatórios
        janela_relatorio = gui_relatorio.JanelaRelatorios(self.root)


if __name__ == "__main__":
    root = tk.Tk()
    app = AppPrincipal(root)
    root.mainloop()