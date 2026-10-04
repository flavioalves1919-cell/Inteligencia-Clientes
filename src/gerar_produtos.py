from faker import Faker
import pandas as pd
import random
from pathlib import Path

fake = Faker("pt_BR")

QUANTIDADE_PRODUTOS = 500
CAMINHO_SAIDA = Path("data/products.csv")

categorias = [
    "Eletrônicos",
    "Informática",
    "Casa",
    "Cozinha",
    "Esportes",
    "Moda",
    "Beleza",
    "Livros",
    "Acessórios",
    "Games"
]

produtos = []

for id_produto in range(1, QUANTIDADE_PRODUTOS + 1):
    categoria = random.choice(categorias)

    produtos.append({
        "id_produto": id_produto,
        "nome_produto": fake.catch_phrase(),
        "categoria": categoria,
        "preco": round(random.uniform(20, 2500), 2),
        "custo": round(random.uniform(10, 1800), 2),
        "estoque_inicial": random.randint(10, 500)
    })

df_produtos = pd.DataFrame(produtos)

CAMINHO_SAIDA.parent.mkdir(parents=True, exist_ok=True)

df_produtos.to_csv(
    CAMINHO_SAIDA,
    index=False,
    encoding="utf-8-sig"
)

print(f"{len(df_produtos):,} produtos gerados com sucesso!")
print(f"Arquivo salvo em: {CAMINHO_SAIDA}")