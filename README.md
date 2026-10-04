# Inteligência de Clientes — Retenção e Churn

Projeto de análise e automação de dados desenvolvido com **Python, SQL e PostgreSQL** para identificar padrões de comportamento dos clientes, analisar retenção e churn e gerar relatórios executivos automaticamente.

## 🎯 Objetivo

Transformar dados de clientes e pedidos em informações que possam apoiar decisões de negócio.

O projeto simula um cenário de e-commerce e constrói uma solução capaz de:

- Processar dados de clientes, produtos e pedidos;
- Realizar tratamento e validação dos dados;
- Armazenar os dados em PostgreSQL;
- Executar análises utilizando SQL;
- Segmentar clientes utilizando RFM;
- Identificar clientes em risco de churn;
- Analisar retenção através de Cohort Analysis;
- Identificar clientes de alto valor em risco;
- Gerar análises executivas automaticamente;
- Gerar um relatório em PDF a partir dos dados atuais.

## 🧰 Tecnologias utilizadas

- **Python**
- **Pandas**
- **NumPy**
- **PostgreSQL**
- **SQL**
- **Psycopg2**
- **SQLAlchemy**
- **Faker**
- **python-dotenv**
- **ReportLab**
- **Git / GitHub**

## 🏗️ Arquitetura

```text
Dados
  ↓
Python / Faker
  ↓
CSV
  ↓
ETL com Pandas
  ↓
PostgreSQL
  ↓
SQL
  ↓
Análise de Clientes
  ↓
RFM + Segmentação
  ↓
Churn + Retenção
  ↓
Python
  ↓
Análise Executiva
  ↓
PDF
```

## 📊 Dados utilizados

O projeto trabalha com uma base simulada de e-commerce contendo:

- 50.000 clientes;
- 500 produtos;
- 200.000 pedidos;
- aproximadamente 24 meses de histórico;
- diferentes status de pedidos;
- métodos de pagamento;
- categorias de produtos;
- regiões.

Os dados foram gerados artificialmente para fins de estudo e portfólio.

## 🔎 Análises realizadas

### RFM

A análise RFM considera:

- **Recência:** quanto tempo desde a última compra;
- **Frequência:** quantidade de compras;
- **Valor Monetário:** quanto o cliente gastou.

Os clientes recebem scores de 1 a 5 e são posteriormente segmentados.

### Segmentação

Os clientes são classificados em grupos como:

- Champions;
- Clientes Fiéis;
- Clientes Novos;
- Clientes em Risco;
- Clientes Perdidos;
- Clientes Potenciais.

### Churn

Foi criada uma regra de classificação baseada no tempo desde a última compra:

| Situação | Regra |
|---|---|
| Ativo | Menos de 90 dias |
| Risco de Churn | 90 a 179 dias |
| Churn | 180 dias ou mais |

Essa regra foi definida para fins de análise do projeto.

### Cohort Analysis

A análise de Cohort acompanha os clientes a partir do mês da primeira compra e mede a quantidade de clientes que continuam comprando nos períodos seguintes.

## 📄 Relatório executivo

O projeto utiliza Python para gerar automaticamente:

```text
reports/
├── relatorio_clientes.csv
├── analise_executiva.txt
└── relatorio_executivo_clientes.pdf
```

O PDF apresenta:

- visão geral da base;
- clientes ativos;
- clientes em risco;
- clientes em churn;
- valor histórico associado aos grupos;
- clientes de alto valor em risco;
- recomendações de negócio.

## 🚀 Como executar

### 1. Clonar o projeto

```bash
git clone https://github.com/flavioalves1919-cell/Inteligencia-Clientes.git
```

### 2. Entrar na pasta

```bash
cd Inteligencia-Clientes
```

### 3. Criar o ambiente virtual

```bash
python -m venv .venv
```

### 4. Instalar as dependências

```bash
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 5. Configurar as credenciais

Criar um arquivo `.env`:

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=SUA_SENHA
```

O arquivo `.env` não deve ser enviado ao GitHub.

### 6. Executar o ETL

```bash
.venv\Scripts\python.exe src/etl.py
```

### 7. Carregar os dados no PostgreSQL

```bash
.venv\Scripts\python.exe src/carregar_postgres.py
```

### 8. Gerar o relatório de clientes

```bash
.venv\Scripts\python.exe src/gerar_relatorio.py
```

### 9. Gerar a análise executiva

```bash
.venv\Scripts\python.exe src/gerar_analise.py
```

### 10. Gerar o PDF

```bash
.venv\Scripts\python.exe src/gerar_pdf.py
```

O relatório será criado em:

```text
reports/relatorio_executivo_clientes.pdf
```

## 💡 Resultado do projeto

Na execução atual, a análise identificou:

- **48.631 clientes analisados**
- **17.765 clientes ativos — 36,53%**
- **11.544 clientes em risco de churn — 23,74%**
- **19.322 clientes em churn — 39,73%**

Esses números representam a execução atual da base simulada e podem mudar quando novos dados forem processados.

## 🎯 Aplicação de negócio

O projeto demonstra como utilizar tecnologia para transformar dados em ações de negócio.

A solução pode ser utilizada como base para processos como:

- identificação de clientes em risco;
- campanhas de reativação;
- priorização de clientes de alto valor;
- acompanhamento de retenção;
- geração automática de relatórios;
- apoio à tomada de decisão.

## 👨‍💻 Projeto

Desenvolvido como projeto de portfólio para demonstrar aplicação prática de **Python, SQL, PostgreSQL, análise de dados e automação de processos de negócio**.