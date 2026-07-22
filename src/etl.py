import pandas as pd
import requests
import os
import numpy as np
from io import StringIO
from datetime import datetime, timedelta
from src.database import Database

class ETL:
    def __init__(self):
        self.db = Database()
        self.raw_data_path = "data/raw/"
        self.processed_data_path = "data/processed/"
        os.makedirs(self.raw_data_path, exist_ok=True)
        os.makedirs(self.processed_data_path, exist_ok=True)

    def download_and_process_states_data(self):
        url = "https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv"
        try:
            response = requests.get(url)
            response.raise_for_status()
            df_states = pd.read_csv(StringIO(response.text))
            print(f"Dados de estados baixados: {len(df_states)} registros")

            # Criar dados de vendas realistas a partir dos dados dos estados
            np.random.seed(42)
            produtos = ['Notebook', 'Mouse', 'Teclado', 'Monitor', 'Headphone', 
                       'Webcam', 'Impressora', 'Tablet', 'Smartphone', 'Carregador']
            
            datas = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
            
            vendas = []
            for estado in df_states.to_dict('records'):
                estado_nome = estado['State']
                populacao = estado['Population']
                # Número de vendas proporcional à população
                num_vendas = int(populacao / 10000) + np.random.randint(1, 50)
                
                for _ in range(min(num_vendas, 500)):  # Limite para não gerar dados enormes
                    produto = np.random.choice(produtos)
                    preco = np.random.uniform(50, 2000)
                    quantidade = np.random.randint(1, 5)
                    data_venda = np.random.choice(datas)
                    
                    vendas.append({
                        'data_venda': data_venda,
                        'produto': produto,
                        'cidade': estado_nome,
                        'estado': estado['Postal'],
                        'quantidade': quantidade,
                        'preco_unitario': preco,
                        'total_venda': preco * quantidade
                    })
            
            df_vendas = pd.DataFrame(vendas)
            df_vendas.to_csv(f"{self.raw_data_path}/vendas_estados_raw.csv", index=False)
            print(f"Dados de vendas gerados a partir dos estados: {len(df_vendas)} registros")
            return df_vendas

        except Exception as e:
            print(f"Erro ao processar dados dos estados: {e}")
            return None

    def clean_sales_data(self, df):
        if df is None:
            return None
        
        df_clean = df.copy()
        
        # Padronização de colunas
        colunas_renomear = {
            'data_venda': 'data_venda',
            'produto': 'produto',
            'cidade': 'cidade',
            'estado': 'estado',
            'quantidade': 'quantidade',
            'preco_unitario': 'preco_unitario',
            'total_venda': 'total_venda'
        }
        
        # Garantir tipos corretos
        if 'data_venda' in df_clean.columns:
            df_clean['data_venda'] = pd.to_datetime(df_clean['data_venda'], errors='coerce')
        
        if 'quantidade' in df_clean.columns:
            df_clean['quantidade'] = pd.to_numeric(df_clean['quantidade'], errors='coerce')
        
        if 'preco_unitario' in df_clean.columns:
            df_clean['preco_unitario'] = pd.to_numeric(df_clean['preco_unitario'], errors='coerce')
        
        if 'total_venda' in df_clean.columns:
            df_clean['total_venda'] = pd.to_numeric(df_clean['total_venda'], errors='coerce')
        
        # Remover registros com dados críticos faltantes
        df_clean = df_clean.dropna(subset=['data_venda', 'quantidade', 'preco_unitario'])
        
        # Remover registros com valores negativos ou zero
        df_clean = df_clean[df_clean['quantidade'] > 0]
        df_clean = df_clean[df_clean['preco_unitario'] > 0]
        
        # Salvar dados limpos
        df_clean.to_csv(f"{self.processed_data_path}/vendas_limpas.csv", index=False)
        print(f"Dados limpos: {len(df_clean)} registros")
        return df_clean

    def load_to_postgres(self, df, table_name):
        if df is None or df.empty:
            print(f"Sem dados para carregar na tabela {table_name}")
            return
        
        try:
            # Carregar para o PostgreSQL
            df.to_sql(table_name, self.db.engine, if_exists='replace', index=False)
            print(f"Dados carregados na tabela {table_name}: {len(df)} registros")
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")

    def run_full_etl(self):
        print("Iniciando ETL...")
        
        # Usar a única fonte de dados que funciona
        df_raw = self.download_and_process_states_data()
        
        if df_raw is not None:
            df_clean = self.clean_sales_data(df_raw)
            if df_clean is not None:
                self.load_to_postgres(df_clean, 'vendas')
                print("ETL concluido com sucesso")
                return df_clean
        else:
            print("Falha no ETL: nenhum dado disponivel")
            return None

if __name__ == "__main__":
    etl = ETL()
    df_resultado = etl.run_full_etl()
    if df_resultado is not None:
        print(f"Total de registros processados: {len(df_resultado)}")