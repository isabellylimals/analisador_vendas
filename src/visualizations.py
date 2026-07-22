import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from src.analytics import SalesAnalytics

class SalesVisualizer:
    def __init__(self):
        self.analytics = SalesAnalytics()
        self.output_path = "data/processed/visualizations/"
        os.makedirs(self.output_path, exist_ok=True)
        
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
    
    def plot_top_products(self, n=10):
        if self.analytics.df is None or self.analytics.df.empty:
            print("Sem dados para visualizar")
            return
        
        top = self.analytics.get_top_products(n)
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        axes[0].bar(top.index, top['total_venda'])
        axes[0].set_title(f'Top {n} Produtos por Faturamento')
        axes[0].set_xlabel('Produto')
        axes[0].set_ylabel('Faturamento Total (R$)')
        axes[0].tick_params(axis='x', rotation=45)
        
        axes[1].bar(top.index, top['quantidade'])
        axes[1].set_title(f'Top {n} Produtos por Quantidade Vendida')
        axes[1].set_xlabel('Produto')
        axes[1].set_ylabel('Quantidade Vendida')
        axes[1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(f"{self.output_path}top_produtos.png", dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Grafico salvo em: {self.output_path}top_produtos.png")
    
    def plot_sales_by_state(self):
        if self.analytics.df is None or self.analytics.df.empty:
            print("Sem dados para visualizar")
            return
        
        vendas_estado = self.analytics.get_sales_by_state().head(10)
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        axes[0].bar(vendas_estado.index, vendas_estado['total_venda'])
        axes[0].set_title('Top 10 Estados por Faturamento')
        axes[0].set_xlabel('Estado')
        axes[0].set_ylabel('Faturamento Total (R$)')
        
        axes[1].bar(vendas_estado.index, vendas_estado['quantidade'])
        axes[1].set_title('Top 10 Estados por Quantidade Vendida')
        axes[1].set_xlabel('Estado')
        axes[1].set_ylabel('Quantidade Vendida')
        
        plt.tight_layout()
        plt.savefig(f"{self.output_path}vendas_por_estado.png", dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Grafico salvo em: {self.output_path}vendas_por_estado.png")
    
    def plot_monthly_trend(self):
        if self.analytics.df is None or self.analytics.df.empty:
            print("Sem dados para visualizar")
            return
        
        vendas_mensais = self.analytics.get_monthly_sales()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(vendas_mensais['mes'], vendas_mensais['total_venda'], marker='o', linewidth=2)
        ax.set_title('Tendência Mensal de Vendas - 2023')
        ax.set_xlabel('Mês')
        ax.set_ylabel('Faturamento Total (R$)')
        ax.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(f"{self.output_path}tendencia_mensal.png", dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Grafico salvo em: {self.output_path}tendencia_mensal.png")
    
    def plot_correlation_matrix(self):
        if self.analytics.df is None or self.analytics.df.empty:
            print("Sem dados para visualizar")
            return
        
        numeric_cols = ['quantidade', 'preco_unitario', 'total_venda']
        corr_matrix = self.analytics.df[numeric_cols].corr()
        
        fig, ax = plt.subplots(figsize=(8, 6))
        
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                   square=True, linewidths=1, ax=ax)
        ax.set_title('Matriz de Correlação - Vendas')
        
        plt.tight_layout()
        plt.savefig(f"{self.output_path}matriz_correlacao.png", dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Grafico salvo em: {self.output_path}matriz_correlacao.png")
    
    def plot_product_performance(self):
        if self.analytics.df is None or self.analytics.df.empty:
            print("Sem dados para visualizar")
            return
        
        performance = self.analytics.get_product_performance().head(10)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        bars = ax.bar(performance.index, performance['faturamento_total'])
        ax.set_title('Performance Financeira dos Produtos')
        ax.set_xlabel('Produto')
        ax.set_ylabel('Faturamento Total (R$)')
        ax.tick_params(axis='x', rotation=45)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'R$ {height:,.0f}',
                   ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        plt.savefig(f"{self.output_path}performance_produtos.png", dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Grafico salvo em: {self.output_path}performance_produtos.png")
    
    def generate_all_visualizations(self):
        print("Gerando todas as visualizacoes...")
        self.plot_top_products()
        self.plot_sales_by_state()
        self.plot_monthly_trend()
        self.plot_correlation_matrix()
        self.plot_product_performance()
        print(f"Todas as visualizacoes salvas em: {self.output_path}")

if __name__ == "__main__":
    visualizer = SalesVisualizer()
    visualizer.generate_all_visualizations()