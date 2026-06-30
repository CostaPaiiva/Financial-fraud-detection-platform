# Financial Fraud Detection Platform

## Plataforma de Detecção de Fraudes Financeiras

Projeto end-to-end de dados para detecção de transações financeiras suspeitas/fraudulentas, integrando Engenharia de Dados, Análise de Dados e Ciência de Dados.

---

## Objetivo

Este projeto simula uma plataforma completa de detecção de fraudes financeiras, contemplando:

- Pipeline ETL com Python
- Organização em camadas raw e processed
- Tratamento e padronização de dados
- Modelagem em PostgreSQL
- Consultas SQL analíticas
- Dashboard executivo em Streamlit
- Modelos de Machine Learning para classificação de fraude
- Geração de score de risco
- Documentação técnica para portfólio

---

## Tecnologias utilizadas

- Python
- Pandas
- NumPy
- PostgreSQL
- pgAdmin
- Docker
- Docker Compose
- SQLAlchemy
- Scikit-learn
- Matplotlib
- Plotly
- Streamlit
- SQL
- Git/GitHub

---

## Dataset

O projeto utiliza um dataset simulado de transações financeiras, criado para representar um cenário realista de detecção de fraudes.

Campos principais:

- `transaction_id`: identificador único da transação
- `customer_id`: identificador do cliente
- `transaction_date`: data e hora da transação
- `transaction_hour`: hora da transação
- `amount`: valor financeiro da transação
- `transaction_type`: tipo da transação
- `merchant_category`: categoria do estabelecimento
- `channel`: canal utilizado
- `device_type`: tipo de dispositivo
- `city`: cidade da transação
- `country`: país da transação
- `previous_transactions_count`: quantidade histórica de transações do cliente
- `average_customer_amount`: valor médio de transação do cliente
- `is_foreign_transaction`: indicador de transação internacional
- `is_high_risk_country`: indicador de país de maior risco
- `is_fraud`: variável alvo indicando fraude

---

## Arquitetura do projeto

```text
Dataset CSV
   ↓
Extração com Python
   ↓
Camada Raw
   ↓
Transformação e Feature Engineering
   ↓
Camada Processed
   ↓
Carga no PostgreSQL
   ↓
Modelagem Analítica
   ↓
SQL Analytics
   ↓
Machine Learning
   ↓
Score de Risco
   ↓
Dashboard Streamlit

Estrutura do projeto
financial-fraud-detection-platform/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
│
├── dashboard/
│   └── app.py
│
├── docs/
│   ├── arquitetura.md
│   ├── modelagem_dados.md
│   ├── relatorio_analitico.md
│   └── machine_learning.md
│
├── notebooks/
│   ├── 01_eda_fraudes.ipynb
│   └── 02_modelagem_fraude.ipynb
│
├── models/
│   └── fraud_model.pkl
│
├── sql/
│   ├── ddl/
│   │   └── create_tables.sql
│   ├── analytics/
│   └── views/
│
├── src/
│   ├── extraction/
│   ├── transformation/
│   ├── loading/
│   ├── analytics/
│   ├── ml/
│   └── utils/
│
├── tests/
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── README.md
└── Makefile
Como executar o projeto
1. Clonar o repositório
git clone https://github.com/seu-usuario/financial-fraud-detection-platform.git
cd financial-fraud-detection-platform
2. Criar o arquivo .env
cp .env.example .env
3. Subir PostgreSQL e pgAdmin
docker compose up -d
4. Verificar containers
docker compose ps
5. Acessar o pgAdmin

Acesse no navegador:

http://localhost:8081

Credenciais:

Email: admin@fraud.com
Senha: admin123
6. Dados do PostgreSQL
Host local: localhost
Porta local: 5433
Database: fraud_detection_db
Usuário: fraud_user
Senha: fraud_password

Dentro do pgAdmin, ao cadastrar o servidor, use:

Host name/address: fraud_postgres
Port: 5432
Maintenance database: fraud_detection_db
Username: fraud_user
Password: fraud_password
## Status do projeto

- [x] Estrutura inicial do projeto
- [x] Docker Compose com PostgreSQL e pgAdmin
- [x] Extração de dados
- [x] Geração de dataset simulado
- [x] Camada raw
- [x] Camada sample
- [ ] Transformação de dados
- [ ] Carga no PostgreSQL
- [ ] SQL analítico
- [ ] Machine Learning
- [ ] Dashboard Streamlit
- [ ] Documentação final
Autor

Projeto desenvolvido para fins de portfólio, com foco em Engenharia de Dados, Análise de Dados e Ciência de Dados.


---

# 11. Subir o Docker

Agora rode:

```bash
docker compose up -d

Depois verifique se os containers estão rodando:

docker compose ps

Você deve ver algo parecido com:

NAME              IMAGE                   STATUS          PORTS
fraud_postgres    postgres:16             Up              0.0.0.0:5433->5432/tcp
fraud_pgadmin     dpage/pgadmin4:latest   Up              0.0.0.0:8081->80/tcp
12. Acessar o pgAdmin

Abra no navegador:

http://localhost:8081

Login:

Email: admin@fraud.com
Senha: admin123
13. Conectar o PostgreSQL no pgAdmin

Dentro do pgAdmin:

Clique com botão direito em Servers
Clique em Register
Clique em Server
Em Name, coloque:
Fraud Detection DB

Na aba Connection, preencha:

Host name/address: fraud_postgres
Port: 5432
Maintenance database: fraud_detection_db
Username: fraud_user
Password: fraud_password

Depois clique em Save.

14. Testar conexão pelo terminal

Se quiser testar pelo Docker:

docker exec -it fraud_postgres psql -U fraud_user -d fraud_detection_db

Dentro do PostgreSQL, rode:

SELECT version();

Para sair:

\q
15. Criar ambiente virtual Python

Na raiz do projeto:

python -m venv venv

Ativar no Git Bash:

source venv/Scripts/activate

Instalar dependências:

pip install -r requirements.txt

Se estiver usando PowerShell:

venv\Scripts\activate
pip install -r requirements.txt
16. Criar documentação inicial da arquitetura

Abra o arquivo:

docs/arquitetura.md

Cole:

# Arquitetura do Projeto

## Visão geral

A Financial Fraud Detection Platform é uma solução end-to-end para detecção de transações financeiras suspeitas/fraudulentas.

O projeto foi estruturado para demonstrar competências em:

- Engenharia de Dados
- Análise de Dados
- Ciência de Dados
- Modelagem de banco de dados
- Machine Learning
- Visualização de dados
- Documentação técnica

---

## Fluxo de dados

```text
Dataset CSV
   ↓
Extração
   ↓
Camada Raw
   ↓
Transformação
   ↓
Camada Processed
   ↓
PostgreSQL
   ↓
SQL Analytics
   ↓
Machine Learning
   ↓
Dashboard
Camadas do projeto
1. Fonte de dados

Os dados representam transações financeiras simuladas, contendo informações como:

Identificador da transação
Cliente
Data e hora
Valor
Tipo de transação
Canal
Dispositivo
Localização
Histórico do cliente
Indicadores de risco
Flag de fraude
2. Camada Raw

A camada raw armazena os dados brutos, preservando o formato original da extração.

Local:

data/raw/

Objetivo:

Manter rastreabilidade
Preservar dados originais
Permitir reprocessamento
3. Camada Processed

A camada processed armazena os dados tratados, padronizados e enriquecidos.

Local:

data/processed/

Tratamentos aplicados:

Remoção ou preenchimento de valores nulos
Padronização de tipos
Padronização de categorias
Criação de features
Validação de qualidade dos dados
4. Banco de Dados

O banco PostgreSQL é utilizado para armazenar os dados processados e modelados.

Principais tabelas:

transactions_raw
transactions_processed
dim_customer
dim_time
dim_location
dim_transaction_type
fact_transactions
fraud_predictions
5. Análise de Dados

A análise de dados é feita com SQL e dashboard.

Exemplos de análises:

Total de transações
Valor total movimentado
Percentual de fraudes
Fraudes por hora
Fraudes por tipo de transação
Fraudes por canal
Ranking de transações suspeitas
6. Machine Learning

A etapa de Ciência de Dados treina modelos para classificação de transações fraudulentas.

Modelos previstos:

Logistic Regression
Random Forest
Decision Tree ou Isolation Forest

Métricas avaliadas:

Accuracy
Precision
Recall
F1-score
ROC-AUC
Matriz de confusão
7. Dashboard

O dashboard em Streamlit apresenta os principais indicadores do projeto.

Indicadores previstos:

Total de transações
Valor total movimentado
Total de fraudes
Percentual de fraudes
Valor perdido com fraudes
Fraudes por hora
Fraudes por tipo
Top transações com maior score de risco
Métricas do modelo

---

# 17. Conferir estrutura no terminal

Rode:

```bash
ls -la

E depois:

find . -maxdepth 3 -type d

No Windows, caso find dê problema, use:

tree

ou:

tree /F
18. Inicializar Git

Na raiz do projeto:

git init
git add .
git commit -m "chore: initial project structure with docker environment"
19. Checklist da Parte 1

Ao final desta parte, você deve ter:

Projeto criado
Estrutura de pastas criada
Docker Compose configurado
PostgreSQL rodando
pgAdmin rodando
.env.example criado
requirements.txt criado
.gitignore criado
Makefile criado
README inicial criado
Documentação inicial da arquitetura criada
Git inicializado