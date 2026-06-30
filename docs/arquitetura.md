---

## Geração dos dados

A primeira etapa do projeto consiste na geração de um dataset simulado de transações financeiras.

O script responsável é:

```text
src/extraction/extract_transactions.py

Esse script cria dados sintéticos com características próximas de um ambiente financeiro real, incluindo:

Transações nacionais e internacionais
Diferentes canais de transação
Diferentes tipos de dispositivo
Categorias de estabelecimento
Histórico transacional do cliente
Indicadores de risco
Variável alvo de fraude

Os dados são salvos em duas camadas:

data/raw/transactions_raw.csv
data/sample/sample_transactions.csv

A camada raw preserva os dados brutos simulados.
A camada sample contém uma amostra menor para inspeção rápida e demonstração no GitHub.


---

# 10. O que essa Parte 2 prova para recrutadores

Essa etapa já demonstra:

```text
Capacidade de criar uma fonte de dados controlada e realista
Organização de dados em camada raw
Criação de dataset com lógica de negócio
Simulação de variável alvo para machine learning
Uso de Python, Pandas e NumPy
Uso de logs
Separação de responsabilidade por módulo
Criação de testes básicos de qualidade