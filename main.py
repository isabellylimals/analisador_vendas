from src.database import Database
from src.etl import ETL
from src.analytics import SalesAnalytics
from src.visualizations import SalesVisualizer
import pandas as pd

def main():
    print("Inicializando Analisador de Vendas")
    
    try:
        db = Database()
        db.create_tables()
        
        etl = ETL()
        dados = etl.run_full_etl()
        
        if dados is not None:
            print("\n" + "="*50)
            print("DADOS CARREGADOS COM SUCESSO")
            print("="*50)
            
            print("\nPrimeiras 5 linhas dos dados carregados:")
            print(dados.head())
            
            analytics = SalesAnalytics()
            relatorio = analytics.generate_full_report()
            
            print("\n" + "="*50)
            print("RELATORIO COMPLETO DE VENDAS")
            print("="*50)
            
            estatisticas = relatorio['estatisticas_basicas']
            print("\nESTATISTICAS BASICAS:")
            for key, value in estatisticas.items():
                if isinstance(value, float):
                    print(f"  {key}: R$ {value:,.2f}")
                else:
                    print(f"  {key}: {value}")
            
            print("\nTOP 5 PRODUTOS (por faturamento):")
            print(relatorio['top_produtos'].head())
            
            print("\nCORRELACOES IMPORTANTES:")
            for key, value in relatorio['correlacoes'].items():
                print(f"  {key}: {value:.3f}")
            
            print("\nPRIMEIRAS 5 CIDADES COM MAIOR FATURAMENTO:")
            print(relatorio['segmentos_clientes'].head())
            
            visualizer = SalesVisualizer()
            visualizer.generate_all_visualizations()
            
            print("\n" + "="*50)
            print("ANALISE CONCLUIDA COM SUCESSO!")
            print("="*50)
            print(f"Relatorio salvo em: data/processed/visualizations/")
            
            return dados, relatorio
        else:
            print("Nenhum dado carregado. Verifique a conexao e tente novamente.")
            return None, None
            
    except Exception as e:
        print(f"Erro na execucao: {e}")
        return None, None

if __name__ == "__main__":
    main()