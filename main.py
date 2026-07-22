from src.database import Database
from src.etl import ETL
import pandas as pd

def main():
    print("Inicializando Analisador de Vendas")
    
    try:
        db = Database()
        db.create_tables()
        
        etl = ETL()
        dados = etl.run_full_etl()
        
        if dados is not None:
            print("Primeiras 5 linhas dos dados carregados:")
            print(dados.head())
            
            estatisticas = {
                'total_registros': len(dados),
                'periodo_inicio': dados['data_venda'].min() if 'data_venda' in dados.columns else 'N/A',
                'periodo_fim': dados['data_venda'].max() if 'data_venda' in dados.columns else 'N/A',
                'total_vendas': dados['total_venda'].sum() if 'total_venda' in dados.columns else 'N/A'
            }
            print("\nEstatisticas iniciais:")
            for chave, valor in estatisticas.items():
                print(f"{chave}: {valor}")
            
            return dados
        else:
            print("Nenhum dado carregado. Verifique a conexao e tente novamente.")
            return None
            
    except Exception as e:
        print(f"Erro na execucao: {e}")
        return None

if __name__ == "__main__":
    main()