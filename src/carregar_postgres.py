import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv

# ==========================================
# CONFIGURAÇÃO
# ==========================================

load_dotenv()

USUARIO = os.getenv("DB_USER")
SENHA = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORTA = os.getenv("DB_PORT")
BANCO = os.getenv("DB_NAME")

# ==========================================
# CONEXÃO DIRETA
# ==========================================

conexao = psycopg2.connect(
    host=HOST,
    port=PORTA,
    user=USUARIO,
    password=SENHA,
    dbname=BANCO
)

print("PostgreSQL conectado!")

# ==========================================
# SQLALCHEMY USANDO A CONEXÃO DIRETA
# ==========================================

engine = create_engine(
    "postgresql+psycopg2://",
    creator=lambda: conexao
)

# ==========================================
# CARREGAR CSVs
# ==========================================

print("Carregando arquivos...")

clientes = pd.read_csv("data/clients_clean.csv")
produtos = pd.read_csv("data/products_clean.csv")
pedidos = pd.read_csv("data/orders_clean.csv")

print("Arquivos carregados!")

# ==========================================
# ENVIAR PARA POSTGRESQL
# ==========================================

print("Enviando clientes...")
clientes.to_sql(
    "clientes",
    engine,
    if_exists="replace",
    index=False
)

print("Enviando produtos...")
produtos.to_sql(
    "produtos",
    engine,
    if_exists="replace",
    index=False
)

print("Enviando pedidos...")
pedidos.to_sql(
    "pedidos",
    engine,
    if_exists="replace",
    index=False
)

# ==========================================
# FINALIZAÇÃO
# ==========================================

conexao.close()

print()
print("=" * 45)
print("DADOS CARREGADOS COM SUCESSO!")
print("=" * 45)
print(f"Clientes: {len(clientes):,}")
print(f"Produtos: {len(produtos):,}")
print(f"Pedidos: {len(pedidos):,}")
print("=" * 45)