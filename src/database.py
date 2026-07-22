import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.port = os.getenv('DB_PORT')
        self.database = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.engine = None
        self._connect()
    
    def _connect(self):
        try:
            connection_string = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            self.engine = create_engine(connection_string, echo=False)
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Conexao com PostgreSQL estabelecida com sucesso")
        except SQLAlchemyError as e:
            print(f"Erro ao conectar ao PostgreSQL: {e}")
            raise
    
    def execute_query(self, query, params=None):
        try:
            with self.engine.connect() as conn:
                if params:
                    result = conn.execute(text(query), params)
                else:
                    result = conn.execute(text(query))
                conn.commit()
                return result
        except SQLAlchemyError as e:
            print(f"Erro ao executar query: {e}")
            raise
    
    def execute_read_query(self, query, params=None):
        try:
            with self.engine.connect() as conn:
                if params:
                    result = conn.execute(text(query), params)
                else:
                    result = conn.execute(text(query))
                return result.fetchall()
        except SQLAlchemyError as e:
            print(f"Erro ao executar query de leitura: {e}")
            raise
    
    def create_tables(self):
        queries = [
            """
            CREATE TABLE IF NOT EXISTS produtos (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                categoria VARCHAR(50),
                preco_unitario DECIMAL(10,2),
                custo_unitario DECIMAL(10,2)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS clientes (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE,
                telefone VARCHAR(20),
                cidade VARCHAR(50),
                estado VARCHAR(2),
                data_cadastro DATE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS vendas (
                id SERIAL PRIMARY KEY,
                cliente_id INTEGER REFERENCES clientes(id),
                produto_id INTEGER REFERENCES produtos(id),
                data_venda DATE NOT NULL,
                quantidade INTEGER NOT NULL,
                preco_venda DECIMAL(10,2),
                desconto DECIMAL(5,2) DEFAULT 0
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS categorias_produtos (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(50) UNIQUE NOT NULL,
                descricao TEXT
            )
            """
        ]
        
        for query in queries:
            try:
                self.execute_query(query)
                print(f"Tabela criada/verificada com sucesso")
            except SQLAlchemyError as e:
                print(f"Erro ao criar tabela: {e}")
                raise

if __name__ == "__main__":
    db = Database()
    db.create_tables()
    print("Banco de dados configurado com sucesso")