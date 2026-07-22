# Analisador de Vendas

Projeto para análise de dados de vendas com Python, PostgreSQL e ferramentas de ciência de dados.

## Requisitos

- Python 3.8+
- PostgreSQL 12+
- Pip

## Configuração

1. Clone o repositório
2. Crie ambiente virtual: `python -m venv venv`
3. Ative o ambiente: `source venv/bin/activate` (Linux/Mac) ou `venv\Scripts\activate` (Windows)
4. Instale dependências: `pip install -r requirements.txt`
5. Configure `.env` com seus dados do PostgreSQL
6. Execute: `python main.py`

## Estrutura

- `src/`: código fonte
  - `database.py`: conexão e operações PostgreSQL
  - `etl.py`: pipeline de extração, transformação e carga
  - `analytics.py`: análises estatísticas
  - `visualizations.py`: gráficos e visualizações
- `data/`: dados brutos e processados
- `notebooks/`: análises exploratórias
- `tests/`: testes unitários

## Funcionalidades

- Download de dados reais de vendas
- Limpeza e transformação de dados
- Armazenamento em PostgreSQL
- Análises estatísticas
- Visualizações interativas
- Previsões básicas

## Próximos Passos

- Análise exploratória detalhada
- Cálculo de métricas de negócio
- Previsões de vendas
- Dashboard interativo