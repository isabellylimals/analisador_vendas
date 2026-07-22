import pandas as pd
import requests
import os
from io import StringIO
from datetime import datetime
from sqlalchemy import text
from src.database import Database

class ETL:
    def __init__(self):
        self.db = Database()
        self.raw_data_path = "data/raw/"
        self.processed_data_path = "data/processed/"
        os.makedirs(self.raw_data_path, exist_ok=True)
        os.makedirs(self.processed_data_path, exist_ok=True)
    
    def download_supermarket_sales(self):
        url = "https://raw.githubusercontent.com/KeithGalli/Pandas-Data-Science-Tasks/master/SalesAnalysis/Sales_Data/Sales_Data.csv"
        try:
            response = requests.get(url)
            response.raise_for_status()
            df = pd.read_csv(StringIO(response.text))
            
            df.to_csv(f"{self.raw_data_path}/vendas_raw.csv", index=False)
            print(f"Dados baixados: {len(df)} registros")
            return df
        except Exception as e:
            print(f"Erro ao baixar dados: {e}")
            return None
    
    def download_online_retail(self):
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
        try:
            df = pd.read_excel(url)
            df.to_csv(f"{self.raw_data_path}/online_retail_raw.csv", index=False)
            print(f"Dados baixados: {len(df)} registros")
            return df
        except Exception as e:
            print(f"Erro ao baixar dados online retail: {e}")
            return None
    
    def clean_sales_data(self, df):
        if df is None:
            return None
        
        df_clean = df.copy()
        
        colunas_renomear = {
            'Order Date': 'data_venda',
            'Quantity Ordered': 'quantidade',
            'Price Each': 'preco_unitario',
            'Sales': 'total_venda'
        }
        
        for old, new in colunas_renomear.items():
            if old in df_clean.columns:
                df_clean.rename(columns={old: new}, inplace=True)
        
        if 'data_venda' in df_clean.columns:
            df_clean['data_venda'] = pd.to_datetime(df_clean['data_venda'], errors='coerce')
        
        if 'quantidade' in df_clean.columns:
            df_clean['quantidade'] = pd.to_numeric(df_clean['quantidade'], errors='coerce')
        
        if 'preco_unitario' in df_clean.columns:
            df_clean['preco_unitario'] = pd.to_numeric(df_clean['preco_unitario'], errors='coerce')
        
        df_clean = df_clean.dropna(subset=['data_venda', 'quantidade'])
        
        df_clean.to_csv(f"{self.processed_data_path}/vendas_limpas.csv", index=False)
        print(f"Dados limpos: {len(df_clean)} registros")
        return df_clean
    
    def load_to_postgres(self, df, table_name):
        if df is None or df.empty:
            print(f"Sem dados para carregar na tabela {table_name}")
            return
        
        try:
            df.to_sql(table_name, self.db.engine, if_exists='replace', index=False)
            print(f"Dados carregados na tabela {table_name}: {len(df)} registros")
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
    
    def run_full_etl(self):
        print("Iniciando ETL...")
        
        df_raw = self.download_supermarket_sales()
        if df_raw is None:
            df_raw = self.download_online_retail()
        
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