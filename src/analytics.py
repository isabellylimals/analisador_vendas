import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.database import Database

class SalesAnalytics:
    def __init__(self):
        self.db = Database()
        self.df = None
        self.load_data()
    
    def load_data(self):
        query = "SELECT data_venda, produto, cidade, estado, quantidade, preco_unitario, total_venda FROM vendas"
        try:
            result = self.db.execute_read_query(query)
            
            if result and len(result) > 0:
                colunas = ['data_venda', 'produto', 'cidade', 'estado', 
                          'quantidade', 'preco_unitario', 'total_venda']
                
                self.df = pd.DataFrame(result, columns=colunas)
                self.df['data_venda'] = pd.to_datetime(self.df['data_venda'])
                
                print(f"Dados carregados: {len(self.df)} registros")
                print(f"Colunas disponiveis: {list(self.df.columns)}")
            else:
                print("Nenhum dado encontrado na tabela vendas")
                self.df = pd.DataFrame()
                
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            self.df = pd.DataFrame()
    
    def get_basic_statistics(self):
        if self.df is None or self.df.empty:
            return {}
        
        stats = {
            'total_vendas': len(self.df),
            'periodo_inicio': self.df['data_venda'].min(),
            'periodo_fim': self.df['data_venda'].max(),
            'total_faturado': self.df['total_venda'].sum(),
            'media_venda': self.df['total_venda'].mean(),
            'mediana_venda': self.df['total_venda'].median(),
            'total_itens_vendidos': self.df['quantidade'].sum(),
            'media_preco_unitario': self.df['preco_unitario'].mean(),
            'produtos_unicos': self.df['produto'].nunique(),
            'cidades_unicas': self.df['cidade'].nunique(),
            'estados_unicos': self.df['estado'].nunique()
        }
        return stats
    
    def get_top_products(self, n=10):
        if self.df is None or self.df.empty:
            return pd.DataFrame()
        
        top_produtos = self.df.groupby('produto').agg({
            'quantidade': 'sum',
            'total_venda': 'sum',
            'preco_unitario': 'mean'
        }).sort_values('total_venda', ascending=False).head(n)
        
        return top_produtos
    
    def get_sales_by_state(self):
        if self.df is None or self.df.empty:
            return pd.DataFrame()
        
        vendas_estado = self.df.groupby('estado').agg({
            'total_venda': 'sum',
            'quantidade': 'sum',
            'preco_unitario': 'mean'
        }).sort_values('total_venda', ascending=False)
        
        return vendas_estado
    
    def get_monthly_sales(self):
        if self.df is None or self.df.empty:
            return pd.DataFrame()
        
        self.df['mes'] = self.df['data_venda'].dt.to_period('M')
        
        vendas_mensais = self.df.groupby('mes').agg({
            'total_venda': 'sum',
            'quantidade': 'sum'
        }).reset_index()
        
        vendas_mensais['mes'] = vendas_mensais['mes'].astype(str)
        return vendas_mensais
    
    def get_daily_sales(self):
        if self.df is None or self.df.empty:
            return pd.DataFrame()
        
        vendas_diarias = self.df.groupby('data_venda').agg({
            'total_venda': 'sum',
            'quantidade': 'sum'
        }).reset_index()
        
        return vendas_diarias
    
    def get_product_performance(self):
        if self.df is None or self.df.empty:
            return pd.DataFrame()
        
        performance = self.df.groupby('produto').agg({
            'total_venda': ['sum', 'mean', 'count'],
            'quantidade': 'sum',
            'preco_unitario': 'mean'
        }).round(2)
        
        performance.columns = ['faturamento_total', 'ticket_medio', 'numero_vendas', 
                              'quantidade_total', 'preco_medio']
        
        performance = performance.sort_values('faturamento_total', ascending=False)
        return performance
    
    def get_customer_segments(self):
        if self.df is None or self.df.empty:
            return pd.DataFrame()
        
        segmentos = self.df.groupby('cidade').agg({
            'total_venda': ['sum', 'mean', 'count'],
            'quantidade': 'sum'
        }).round(2)
        
        segmentos.columns = ['faturamento_total', 'ticket_medio', 'num_transacoes', 'itens_vendidos']
        
        segmentos['valor_por_transacao'] = segmentos['faturamento_total'] / segmentos['num_transacoes']
        segmentos = segmentos.sort_values('faturamento_total', ascending=False)
        
        return segmentos
    
    def get_sales_trends(self):
        if self.df is None or self.df.empty:
            return {}
        
        self.df['mes'] = self.df['data_venda'].dt.to_period('M')
        self.df['trimestre'] = self.df['data_venda'].dt.to_period('Q')
        self.df['semana'] = self.df['data_venda'].dt.isocalendar().week
        
        tendencias = {
            'vendas_por_mes': self.df.groupby('mes')['total_venda'].sum().to_dict(),
            'vendas_por_trimestre': self.df.groupby('trimestre')['total_venda'].sum().to_dict(),
            'media_diaria': self.df.groupby('data_venda')['total_venda'].sum().mean(),
            'dia_maior_venda': self.df.groupby('data_venda')['total_venda'].sum().idxmax(),
            'valor_dia_maior_venda': self.df.groupby('data_venda')['total_venda'].sum().max()
        }
        
        return tendencias
    
    def get_correlation_analysis(self):
        if self.df is None or self.df.empty:
            return {}
        
        correlacoes = {
            'quantidade_vs_total': self.df['quantidade'].corr(self.df['total_venda']),
            'preco_vs_total': self.df['preco_unitario'].corr(self.df['total_venda']),
            'quantidade_vs_preco': self.df['quantidade'].corr(self.df['preco_unitario'])
        }
        
        return correlacoes
    
    def generate_full_report(self):
        print("Gerando relatorio completo de vendas...")
        
        if self.df is None or self.df.empty:
            print("Sem dados para gerar relatorio")
            return {}
        
        relatorio = {
            'estatisticas_basicas': self.get_basic_statistics(),
            'top_produtos': self.get_top_products(),
            'vendas_por_estado': self.get_sales_by_state(),
            'vendas_mensais': self.get_monthly_sales(),
            'performance_produtos': self.get_product_performance(),
            'segmentos_clientes': self.get_customer_segments(),
            'tendencias': self.get_sales_trends(),
            'correlacoes': self.get_correlation_analysis()
        }
        
        print("Relatorio gerado com sucesso!")
        return relatorio

if __name__ == "__main__":
    analytics = SalesAnalytics()
    report = analytics.generate_full_report()
    
    if report and report.get('estatisticas_basicas'):
        print("\n=== ESTATISTICAS BASICAS ===")
        for key, value in report['estatisticas_basicas'].items():
            if isinstance(value, float):
                print(f"{key}: R$ {value:,.2f}")
            else:
                print(f"{key}: {value}")
        
        print("\n=== TOP 5 PRODUTOS ===")
        if not report['top_produtos'].empty:
            print(report['top_produtos'].head())
        else:
            print("Sem dados de produtos")
        
        print("\n=== CORRELACOES ===")
        for key, value in report['correlacoes'].items():
            print(f"{key}: {value:.3f}")