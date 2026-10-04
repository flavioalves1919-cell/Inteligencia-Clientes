import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()


CONEXAO = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT")
}

# ============================================================
# CONEXÃO COM POSTGRESQL
# ============================================================

conexao = psycopg2.connect(**CONEXAO)


# ============================================================
# CONSULTA PRINCIPAL
# ============================================================

query = """
WITH clientes AS (

    SELECT

        id_cliente,

        MAX(data_pedido::date) AS ultima_compra,

        CURRENT_DATE - MAX(data_pedido::date)
            AS dias_sem_comprar,

        COUNT(DISTINCT id_pedido)
            AS total_pedidos,

        SUM(valor_total)
            AS valor_total_comprado

    FROM pedidos

    WHERE status = 'Concluído'

    GROUP BY id_cliente
)

SELECT

    id_cliente,

    ultima_compra,

    dias_sem_comprar,

    total_pedidos,

    ROUND(valor_total_comprado::numeric, 2)
        AS valor_total_comprado,

    CASE

        WHEN dias_sem_comprar >= 180
            THEN 'Churn'

        WHEN dias_sem_comprar >= 90
            THEN 'Risco de Churn'

        ELSE 'Ativo'

    END AS status_cliente

FROM clientes

ORDER BY valor_total_comprado DESC;
"""


# ============================================================
# EXECUTAR CONSULTA
# ============================================================

df = pd.read_sql_query(query, conexao)


# ============================================================
# CRIAR PASTA DE RELATÓRIOS
# ============================================================

Path("reports").mkdir(exist_ok=True)


# ============================================================
# SALVAR RELATÓRIO
# ============================================================

arquivo = "reports/relatorio_clientes.csv"

df.to_csv(
    arquivo,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# RESUMO
# ============================================================

print("=" * 60)
print("RELATÓRIO DE INTELIGÊNCIA DE CLIENTES")
print("=" * 60)

print(f"Clientes analisados: {len(df):,}")

print("\nStatus dos clientes:")

print(
    df["status_cliente"]
    .value_counts()
)

print("\nRelatório salvo em:")
print(arquivo)

print("=" * 60)


conexao.close()