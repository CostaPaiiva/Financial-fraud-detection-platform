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