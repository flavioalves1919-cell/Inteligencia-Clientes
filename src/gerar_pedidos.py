import pandas as pd
import numpy as np
from pathlib import Path

QUANTIDADE_PEDIDOS = 200_000

CAMINHO_CLIENTES = Path("data/clients.csv")
CAMINHO_PRODUTOS = Path("data/products.csv")
CAMINHO_SAIDA = Path("data/orders.csv")

# Carregar dados existentes
clientes = pd.read_csv(CAMINHO_CLIENTES)
produtos = pd.read_csv(CAMINHO_PRODUTOS)

# Gerador aleatório
rng = np.random.default_rng(42)

# IDs aleatórios de clientes e produtos
ids_clientes = rng.choice(
    clientes["id_cliente"].values,
    size=QUANTIDADE_PEDIDOS
)

ids_produtos = rng.choice(
    produtos["id_produto"].values,
    size=QUANTIDADE_PEDIDOS
)

# Buscar preços dos produtos
precos = produtos.set_index("id_produto")["preco"]

precos_unitarios = precos.loc[ids_produtos].to_numpy()

# Quantidades
quantidades = rng.integers(
    low=1,
    high=6,
    size=QUANTIDADE_PEDIDOS
)

# Datas aleatórias nos últimos 24 meses
data_fim = pd.Timestamp.today().normalize()
data_inicio = data_fim - pd.DateOffset(months=24)

dias = rng.integers(
    0,
    (data_fim - data_inicio).days + 1,
    size=QUANTIDADE_PEDIDOS
)

datas = data_inicio + pd.to_timedelta(dias, unit="D")

# Status dos pedidos
status = rng.choice(
    ["Concluído", "Cancelado"],
    size=QUANTIDADE_PEDIDOS,
    p=[0.90, 0.10]
)

# Formas de pagamento
formas_pagamento = rng.choice(
    [
        "Cartão de crédito",
        "Cartão de débito",
        "Pix",
        "Boleto"
    ],
    size=QUANTIDADE_PEDIDOS
)

# Criar DataFrame
df_pedidos = pd.DataFrame({
    "id_pedido": np.arange(1, QUANTIDADE_PEDIDOS + 1),
    "id_cliente": ids_clientes,
    "id_produto": ids_produtos,
    "data_pedido": datas,
    "quantidade": quantidades,
    "preco_unitario": np.round(precos_unitarios, 2),
    "status": status,
    "forma_pagamento": formas_pagamento
})

# Calcular valor total
df_pedidos["valor_total"] = (
    df_pedidos["quantidade"]
    * df_pedidos["preco_unitario"]
).round(2)

# Criar pasta caso não exista
CAMINHO_SAIDA.parent.mkdir(
    parents=True,
    exist_ok=True
)

# Salvar CSV
df_pedidos.to_csv(
    CAMINHO_SAIDA,
    index=False,
    encoding="utf-8-sig"
)

print(f"{len(df_pedidos):,} pedidos gerados com sucesso!")
print(f"Clientes utilizados: {df_pedidos['id_cliente'].nunique():,}")
print(f"Produtos utilizados: {df_pedidos['id_produto'].nunique():,}")
print(
    f"Valor total dos pedidos: "
    f"R$ {df_pedidos['valor_total'].sum():,.2f}"
)
print(f"Arquivo salvo em: {CAMINHO_SAIDA}")