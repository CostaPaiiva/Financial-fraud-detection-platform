---

## Geração dos dados

A primeira etapa do projeto consiste na geração de um dataset simulado de transações financeiras.

O script responsável é:

```text
src/extraction/extract_transactions.py
```

Esse script cria dados sintéticos com características próximas de um ambiente financeiro real, incluindo:

- Transações nacionais e internacionais
- Diferentes canais de transação
- Diferentes tipos de dispositivo
- Categorias de estabelecimento
- Histórico transacional do cliente
- Indicadores de risco
- Variável alvo de fraude

Os dados são salvos em duas camadas:

- `data/raw/transactions_raw.csv`
- `data/sample/sample_transactions.csv`

A camada `raw` preserva os dados brutos simulados.
A camada `sample` contém uma amostra menor para inspeção rápida e demonstração no GitHub.

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
```

---

## Transformação dos dados

A transformação dos dados é realizada pelo script:

```text
src/transformation/transform_transactions.py
```

Essa etapa recebe os dados da camada raw e gera uma versão limpa e enriquecida na camada processed.

**Entrada:**
- `data/raw/transactions_raw.csv`

**Saída:**
- `data/processed/transactions_processed.csv`

### Tratamentos realizados
- Padronização de campos textuais
- Conversão de datas
- Conversão de campos numéricos
- Tratamento de valores nulos
- Validação de identificadores únicos
- Validação de valores financeiros
- Validação da variável alvo `is_fraud`

### Features criadas
| Feature | Descrição |
|---|---|
| `transaction_date_only` | Data da transação sem horário |
| `transaction_year` | Ano da transação |
| `transaction_month` | Mês da transação |
| `transaction_day` | Dia da transação |
| `transaction_day_of_week` | Dia da semana em formato numérico |
| `transaction_day_name` | Nome do dia da semana |
| `is_weekend` | Indica se a transação ocorreu no fim de semana |
| `is_night_transaction` | Indica se a transação ocorreu entre 00h e 05h |
| `is_business_hours` | Indica se ocorreu em horário comercial |
| `amount_above_customer_avg` | Razão entre valor da transação e média do cliente |
| `amount_difference_from_avg` | Diferença entre valor da transação e média do cliente |
| `amount_risk_level` | Faixa de risco baseada no valor |
| `transaction_amount_category` | Categoria de valor da transação |
| `customer_activity_level` | Nível de atividade histórica do cliente |
| `rule_based_risk_score` | Score de risco baseado em regras |
| `risk_level` | Classificação do risco: baixo, médio, alto ou crítico |

### Importância da transformação

Essa etapa demonstra a aplicação de práticas fundamentais de Engenharia de Dados, como limpeza, padronização, enriquecimento, rastreabilidade e validação de qualidade dos dados antes da carga no banco.
