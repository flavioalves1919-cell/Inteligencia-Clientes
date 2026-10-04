import pandas as pd
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


# ============================================================
# CONFIGURAÇÃO
# ============================================================

arquivo_dados = "reports/relatorio_clientes.csv"
arquivo_saida = "reports/relatorio_executivo_clientes.pdf"


# ============================================================
# LER DADOS ATUAIS
# ============================================================

df = pd.read_csv(arquivo_dados)

total_clientes = len(df)

ativos = (df["status_cliente"] == "Ativo").sum()
risco = (df["status_cliente"] == "Risco de Churn").sum()
churn = (df["status_cliente"] == "Churn").sum()

percentual_ativos = ativos / total_clientes * 100
percentual_risco = risco / total_clientes * 100
percentual_churn = churn / total_clientes * 100

valor_churn = df.loc[
    df["status_cliente"] == "Churn",
    "valor_total_comprado"
].sum()

valor_risco = df.loc[
    df["status_cliente"] == "Risco de Churn",
    "valor_total_comprado"
].sum()


# ============================================================
# CLIENTES DE ALTO VALOR EM RISCO
# ============================================================

top_risco = (
    df[
        df["status_cliente"].isin(
            ["Churn", "Risco de Churn"]
        )
    ]
    .sort_values(
        "valor_total_comprado",
        ascending=False
    )
    .head(10)
)


# ============================================================
# CRIAR PASTA
# ============================================================

Path("reports").mkdir(exist_ok=True)


# ============================================================
# ESTILOS
# ============================================================

styles = getSampleStyleSheet()

titulo = styles["Title"]
subtitulo = styles["Heading2"]
texto = styles["BodyText"]


# ============================================================
# DOCUMENTO
# ============================================================

documento = SimpleDocTemplate(
    arquivo_saida,
    pagesize=A4,
    rightMargin=40,
    leftMargin=40,
    topMargin=40,
    bottomMargin=40
)

conteudo = []


# ============================================================
# TÍTULO
# ============================================================

conteudo.append(
    Paragraph(
        "INTELIGÊNCIA DE CLIENTES",
        titulo
    )
)

conteudo.append(
    Paragraph(
        "Relatório Executivo",
        subtitulo
    )
)

conteudo.append(Spacer(1, 20))


# ============================================================
# VISÃO GERAL
# ============================================================

conteudo.append(
    Paragraph(
        "1. Visão Geral",
        subtitulo
    )
)

dados_resumo = [
    ["Indicador", "Resultado"],

    [
        "Clientes analisados",
        f"{total_clientes:,}".replace(",", ".")
    ],

    [
        "Clientes ativos",
        f"{ativos:,}".replace(",", ".")
        + f" ({percentual_ativos:.2f}%)"
    ],

    [
        "Risco de Churn",
        f"{risco:,}".replace(",", ".")
        + f" ({percentual_risco:.2f}%)"
    ],

    [
        "Churn",
        f"{churn:,}".replace(",", ".")
        + f" ({percentual_churn:.2f}%)"
    ],

    [
        "Valor histórico - Churn",
        f"R$ {valor_churn:,.2f}"
    ],

    [
        "Valor histórico - Risco",
        f"R$ {valor_risco:,.2f}"
    ]
]

tabela = Table(
    dados_resumo,
    colWidths=[250, 220]
)

tabela.setStyle(
    TableStyle([
        (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            colors.darkblue
        ),
        (
            "TEXTCOLOR",
            (0, 0),
            (-1, 0),
            colors.white
        ),
        (
            "FONTNAME",
            (0, 0),
            (-1, 0),
            "Helvetica-Bold"
        ),
        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.5,
            colors.grey
        ),
        (
            "PADDING",
            (0, 0),
            (-1, -1),
            7
        )
    ])
)

conteudo.append(tabela)
conteudo.append(Spacer(1, 20))


# ============================================================
# CLIENTES DE ALTO VALOR EM RISCO
# ============================================================

conteudo.append(
    Paragraph(
        "2. Clientes de Alto Valor em Risco",
        subtitulo
    )
)

conteudo.append(
    Paragraph(
        "Clientes classificados como Churn ou Risco de Churn, "
        "ordenados pelo valor histórico comprado.",
        texto
    )
)

conteudo.append(Spacer(1, 10))


dados_risco = [
    [
        "Cliente",
        "Dias sem comprar",
        "Pedidos",
        "Valor histórico"
    ]
]

for _, cliente in top_risco.iterrows():

    dados_risco.append([
        str(int(cliente["id_cliente"])),

        str(
            int(cliente["dias_sem_comprar"])
        ),

        str(
            int(cliente["total_pedidos"])
        ),

        f"R$ {cliente['valor_total_comprado']:,.2f}"
    ])


tabela_risco = Table(
    dados_risco,
    colWidths=[80, 110, 70, 150]
)

tabela_risco.setStyle(
    TableStyle([
        (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            colors.darkblue
        ),
        (
            "TEXTCOLOR",
            (0, 0),
            (-1, 0),
            colors.white
        ),
        (
            "FONTNAME",
            (0, 0),
            (-1, 0),
            "Helvetica-Bold"
        ),
        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.5,
            colors.grey
        ),
        (
            "PADDING",
            (0, 0),
            (-1, -1),
            6
        )
    ])
)

conteudo.append(tabela_risco)
conteudo.append(Spacer(1, 20))


# ============================================================
# RECOMENDAÇÕES
# ============================================================

conteudo.append(
    Paragraph(
        "3. Recomendações de Negócio",
        subtitulo
    )
)

recomendacoes = [
    "Priorizar clientes de alto valor classificados como Churn ou Risco de Churn.",

    "Criar campanhas de reativação para clientes em risco.",

    "Criar ações de retenção para clientes ativos com alto valor histórico.",

    "Monitorar mensalmente a evolução das taxas de Churn e Risco de Churn."
]

for recomendacao in recomendacoes:

    conteudo.append(
        Paragraph(
            "• " + recomendacao,
            texto
        )
    )

    conteudo.append(Spacer(1, 6))


# ============================================================
# GERAR PDF
# ============================================================

documento.build(conteudo)


print("=" * 60)
print("PDF GERADO COM SUCESSO!")
print("=" * 60)
print()
print("Arquivo:")
print(arquivo_saida)
print()
print("O PDF utiliza os dados atuais do relatório.")
print("=" * 60)