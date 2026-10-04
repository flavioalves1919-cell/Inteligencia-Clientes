import pandas as pd
from pathlib import Path

# =========================
# CONFIGURAÇÃO
# =========================

PASTA_DATA = Path("data")

ARQUIVO_CLIENTES = PASTA_DATA / "clients.csv"
ARQUIVO_PRODUTOS = PASTA_DATA / "products.csv"
ARQUIVO_PEDIDOS = PASTA_DATA / "orders.csv"

# =========================
# LEITURA DOS DADOS
# =========================

print("Carregando dados...")

clientes = pd.read_csv(ARQUIVO_CLIENTES)
produtos = pd.read_csv(ARQUIVO_PRODUTOS)
pedidos = pd.read_csv(ARQUIVO_PEDIDOS)

print("Dados carregados com sucesso.")

# =========================
# TRATAMENTO DE DATAS
# =========================

clientes["data_cadastro"] = pd.to_datetime(
    clientes["data_cadastro"],
    errors="coerce"
)

pedidos["data_pedido"] = pd.to_datetime(
    pedidos["data_pedido"],
    errors="coerce"
)

# =========================
# TRATAMENTO DE DUPLICADOS
# =========================

clientes = clientes.drop_duplicates(
    subset="id_cliente"
)

produtos = produtos.drop_duplicates(
    subset="id_produto"
)

pedidos = pedidos.drop_duplicates(
    subset="id_pedido"
)

# =========================
# TRATAMENTO DE VALORES
# =========================

clientes["idade"] = pd.to_numeric(
    clientes["idade"],
    errors="coerce"
)

produtos["preco"] = pd.to_numeric(
    produtos["preco"],
    errors="coerce"
)

produtos["custo"] = pd.to_numeric(
    produtos["custo"],
    errors="coerce"
)

pedidos["quantidade"] = pd.to_numeric(
    pedidos["quantidade"],
    errors="coerce"
)

pedidos["preco_unitario"] = pd.to_numeric(
    pedidos["preco_unitario"],
    errors="coerce"
)

pedidos["valor_total"] = pd.to_numeric(
    pedidos["valor_total"],
    errors="coerce"
)

# =========================
# VALIDAÇÃO DE DADOS
# =========================

print("\n===== VALIDAÇÃO =====")

print("\nClientes:")
print(f"Registros: {len(clientes):,}")
print(f"Nulos: {clientes.isnull().sum().sum():,}")

print("\nProdutos:")
print(f"Registros: {len(produtos):,}")
print(f"Nulos: {produtos.isnull().sum().sum():,}")

print("\nPedidos:")
print(f"Registros: {len(pedidos):,}")
print(f"Nulos: {pedidos.isnull().sum().sum():,}")

# =========================
# VALIDAÇÃO DE RELACIONAMENTOS
# =========================

clientes_validos = set(clientes["id_cliente"])
produtos_validos = set(produtos["id_produto"])

pedidos_clientes_invalidos = ~pedidos["id_cliente"].isin(
    clientes_validos
)

pedidos_produtos_invalidos = ~pedidos["id_produto"].isin(
    produtos_validos
)

print("\n===== INTEGRIDADE =====")

print(
    "Pedidos com cliente inexistente:",
    pedidos_clientes_invalidos.sum()
)

print(
    "Pedidos com produto inexistente:",
    pedidos_produtos_invalidos.sum()
)

# =========================
# RECÁLCULO DO VALOR TOTAL
# =========================

pedidos["valor_total_calculado"] = (
    pedidos["quantidade"]
    * pedidos["preco_unitario"]
).round(2)

erros_valor = (
    pedidos["valor_total"]
    != pedidos["valor_total_calculado"]
)

print(
    "Pedidos com valor total inconsistente:",
    erros_valor.sum()
)

# =========================
# EXPORTAÇÃO DOS DADOS TRATADOS
# =========================

clientes.to_csv(
    PASTA_DATA / "clients_clean.csv",
    index=False,
    encoding="utf-8-sig"
)

produtos.to_csv(
    PASTA_DATA / "products_clean.csv",
    index=False,
    encoding="utf-8-sig"
)

pedidos.to_csv(
    PASTA_DATA / "orders_clean.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nETL concluído com sucesso!")