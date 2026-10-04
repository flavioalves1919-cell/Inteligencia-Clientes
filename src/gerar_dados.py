from faker import Faker
import pandas as pd
import random
from pathlib import Path

fake = Faker("pt_BR")

# Quantidade de clientes
QUANTIDADE_CLIENTES = 50_000

# Caminho para salvar os dados
CAMINHO_SAIDA = Path("data/clients.csv")

clientes = []

for id_cliente in range(1, QUANTIDADE_CLIENTES + 1):
    clientes.append({
        "id_cliente": id_cliente,
        "nome": fake.name(),
        "email": fake.email(),
        "cidade": fake.city(),
        "estado": fake.estado_sigla(),
        "data_cadastro": fake.date_between(
            start_date="-24m",
            end_date="today"
        ),
        "idade": random.randint(18, 70)
    })

df_clientes = pd.DataFrame(clientes)

# Criar a pasta caso não exista
CAMINHO_SAIDA.parent.mkdir(parents=True, exist_ok=True)

# Salvar arquivo CSV
df_clientes.to_csv(
    CAMINHO_SAIDA,
    index=False,
    encoding="utf-8-sig"
)

print(f"{len(df_clientes):,} clientes gerados com sucesso!")
print(f"Arquivo salvo em: {CAMINHO_SAIDA}")