import pandas as pd
from pathlib import Path


# ============================================================
# CONFIGURAÇÃO
# ============================================================

arquivo = "reports/relatorio_clientes.csv"

df = pd.read_csv(arquivo)


# ============================================================
# INDICADORES
# ============================================================

total_clientes = len(df)

ativos = (df["status_cliente"] == "Ativo").sum()
risco = (df["status_cliente"] == "Risco de Churn").sum()
churn = (df["status_cliente"] == "Churn").sum()

percentual_ativos = ativos / total_clientes * 100
percentual_risco = risco / total_clientes * 100
percentual_churn = churn / total_clientes * 100

clientes_em_risco = risco + churn

percentual_em_risco = (
    clientes_em_risco / total_clientes * 100
)


# ============================================================
# CLIENTES DE ALTO VALOR EM RISCO
# ============================================================

alto_valor = df[
    (df["status_cliente"].isin(["Churn", "Risco de Churn"]))
].sort_values(
    "valor_total_comprado",
    ascending=False
)

top_10_risco = alto_valor.head(10)


# ============================================================
# VALOR ASSOCIADO AO CHURN
# ============================================================

valor_churn = df[
    df["status_cliente"] == "Churn"
]["valor_total_comprado"].sum()

valor_risco = df[
    df["status_cliente"] == "Risco de Churn"
]["valor_total_comprado"].sum()


# ============================================================
# GERAR RELATÓRIO
# ============================================================

Path("reports").mkdir(exist_ok=True)

arquivo_saida = "reports/analise_executiva.txt"


with open(
    arquivo_saida,
    "w",
    encoding="utf-8"
) as arquivo:

    arquivo.write(
        "RELATÓRIO EXECUTIVO - INTELIGÊNCIA DE CLIENTES\n"
    )

    arquivo.write("=" * 60 + "\n\n")

    arquivo.write("1. VISÃO GERAL\n")
    arquivo.write("-" * 60 + "\n")

    arquivo.write(
        f"Clientes analisados: {total_clientes:,}\n"
    )

    arquivo.write(
        f"Clientes ativos: {ativos:,} "
        f"({percentual_ativos:.2f}%)\n"
    )

    arquivo.write(
        f"Clientes em risco de churn: {risco:,} "
        f"({percentual_risco:.2f}%)\n"
    )

    arquivo.write(
        f"Clientes em churn: {churn:,} "
        f"({percentual_churn:.2f}%)\n"
    )

    arquivo.write(
        f"Clientes em situação de risco: "
        f"{clientes_em_risco:,} "
        f"({percentual_em_risco:.2f}%)\n\n"
    )


    arquivo.write("2. VALOR FINANCEIRO ASSOCIADO AO RISCO\n")
    arquivo.write("-" * 60 + "\n")

    arquivo.write(
        f"Valor histórico dos clientes em churn: "
        f"R$ {valor_churn:,.2f}\n"
    )

    arquivo.write(
        f"Valor histórico dos clientes em risco: "
        f"R$ {valor_risco:,.2f}\n\n"
    )


    arquivo.write("3. CLIENTES DE ALTO VALOR EM RISCO\n")
    arquivo.write("-" * 60 + "\n")

    for _, cliente in top_10_risco.iterrows():

        arquivo.write(
            f"Cliente {int(cliente['id_cliente'])} | "
            f"{int(cliente['dias_sem_comprar'])} dias sem comprar | "
            f"{int(cliente['total_pedidos'])} pedidos | "
            f"R$ {cliente['valor_total_comprado']:,.2f}\n"
        )

    arquivo.write("\n")


    arquivo.write("4. RECOMENDAÇÕES DE NEGÓCIO\n")
    arquivo.write("-" * 60 + "\n")

    arquivo.write(
        "1. Priorizar clientes de alto valor classificados "
        "como Churn ou Risco de Churn.\n"
    )

    arquivo.write(
        "2. Criar campanhas de reativação para clientes "
        "em risco.\n"
    )

    arquivo.write(
        "3. Criar ações de retenção para clientes ativos "
        "com alto valor histórico.\n"
    )

    arquivo.write(
        "4. Monitorar mensalmente a evolução das taxas "
        "de Churn e Risco de Churn.\n"
    )


print("=" * 60)
print("ANÁLISE EXECUTIVA GERADA")
print("=" * 60)

print(f"Clientes analisados: {total_clientes:,}")
print(f"Ativos: {ativos:,} ({percentual_ativos:.2f}%)")
print(f"Risco de Churn: {risco:,} ({percentual_risco:.2f}%)")
print(f"Churn: {churn:,} ({percentual_churn:.2f}%)")

print("\nRelatório salvo em:")
print(arquivo_saida)

print("=" * 60)