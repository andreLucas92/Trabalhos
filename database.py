
import sqlite3

def criar_banco():
    # Conecta ao banco de dados (cria o arquivo loja.db se não existir)
    conn = sqlite3.connect('loja.db')
    cursor = conn.cursor()

    # --- Criar Tabela de Funcionários ---
    # matricula é a CHAVE PRIMÁRIA (PRIMARY KEY)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS funcionarios (
        matricula TEXT PRIMARY KEY,
        nome TEXT NOT NULL,
        cargo TEXT
    )
    ''')

    # --- Criar Tabela de Clientes ---
    # 'identificador' será o email ou telefone (CHAVE PRIMÁRIA)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        identificador TEXT PRIMARY KEY,
        nome TEXT NOT NULL
    )
    ''')

    # --- Criar Tabela de Estoque (Produtos) ---
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS estoque (
        id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_produto TEXT NOT NULL,
        quantidade INTEGER,
        preco_venda REAL
    )
    ''')

    # --- Criar Tabela de Vendas (para o Caixa) ---
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vendas (
        id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
        data_venda TEXT NOT NULL,
        id_cliente TEXT,
        total REAL,
        FOREIGN KEY (id_cliente) REFERENCES clientes (identificador)
    )
    ''')

    # --- Criar Tabela de Itens da Venda (para os Relatórios) ---
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS itens_venda (
        id_item INTEGER PRIMARY KEY AUTOINCREMENT,
        id_venda INTEGER,
        id_produto INTEGER,
        quantidade INTEGER,
        preco_unitario REAL,
        FOREIGN KEY (id_venda) REFERENCES vendas (id_venda),
        FOREIGN KEY (id_produto) REFERENCES estoque (id_produto)
    )
    ''')

    print("Tabelas criadas com sucesso!")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_banco()
