# pip install pymysql pandas sqlalchemy python-dotenv
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import subprocess

# Conectando banco de dados
def conecta_banco():
    host = os.getenv('DB_HOST')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    database = os.getenv('DB_DATABASE')
    engine = create_engine(
    f'mysql+pymysql://{user}:{password}@{host}/{database}'
    )
    return engine



load_dotenv()
engine = conecta_banco()

# Obteno dados
try:
    subprocess.run('cls', shell=True)
    print('Obteno dados...')
    df_clientes = pd.read_sql('tb_clientes', engine)
    df_pedidos = pd.read_sql('tb_pedidos', engine)
    df_itens = pd.read_sql('tb_itens', engine)
    df_produtos = pd.read_sql('tb_produtos', engine)
    
except Exception as e:
    print(f'Erro ao conectar aos dados - {e}')

# Relacionando
try:
    df_merge1 = pd.merge(
        df_clientes, df_pedidos, on= 'codigo_cliente'
    )
    df_merge2 = pd.merge(
        df_merge1, df_itens, on= 'codigo_pedido'
    )
    df_dados = pd.merge(
        # quando os campos forem diferentes, usara a sintaxe
        df_merge2, df_produtos, on= 'codigo_produto' 
    )

    #print(df_dados)

except Exception as e:
    print(f'Erro ao relacionar os dataframes - {e}')


# Filtrando
try:
    df_pedidos_realizados = df_dados[
        (df_dados['cidade'] == 'Sao Paulo') + 
        (df_dados['cidade'] == 'Curitiba')
    ]

    
    df_pedidos_realizados = df_pedidos_realizados.sort_values(
        by='codigo_pedido',
        ascending=True
    )

    print(df_pedidos_realizados[
        [
            'nome', 'sobrenome', 'cidade',
            'codigo_pedido', 'data_pedido',
            'produto', 'valor'
        ]
    ])

except Exception as e:
    print(f'Erro ao filtrar os dataframes - {e}')
