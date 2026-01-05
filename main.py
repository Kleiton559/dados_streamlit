# IMPORTAR AS BIBLIOTECAS
import streamlit as st
import pandas as pd
import numpy as np
import sqlite3

# TITULO DO SITE
st.sidebar.title("Integração com Banco de Dados e API´s")

#MANIPULAR NUMERO DE LINHAS COM SLIDEBAR
numeroLinhas = st.sidebar.slider(
    label='Quantidade Informacoes para Visualizar',
    min_value = 0, #MINIMO VALOR
    max_value = 20 #MAXIMO VALOR
)

# CONEXAO COM SQLITE
conn = sqlite3.connect(":memory:") #CRIAR UMA BASE DE DADOS TEMPORÁRIO
cursor = conn.cursor()

# CRIAÇÃO DE TABELAS E INSERÇÃO DE DADOS DE EXEMPLO
cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos(
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        preco REAL NOT NULL
    )
''')

cursor.execute('INSERT INTO produtos (nome,preco) VALUES ("Computador",3500.00)')
cursor.execute('INSERT INTO produtos (nome,preco) VALUES ("Mouse",500.00)')
cursor.execute('INSERT INTO produtos (nome,preco) VALUES ("Teclado",1500.00)')
cursor.execute('INSERT INTO produtos (nome,preco) VALUES ("Oculos Lendarios",600.00)')




# MOSTRAR OS DADOS DA BASE DE DADOS
st.header('Produtos do Banco de Dados')
query = 'SELECT * FROM produtos'
df_produtos = pd.read_sql_query(query, conn)

st.dataframe(df_produtos)

# FECHAR A CONEXAO DO BANCO DE DADOS
conn.close()



###----Exemplo de API----
st.header("Dados de uma API Externa")
st.write(f'Numero de Informações Vizualizadas: {numeroLinhas} Linha(s)')
import requests
try:
    resposta = requests.get(f'https://jsonplaceholder.typicode.com/posts?_limit={numeroLinhas}')
    posts=resposta.json()

    #----Mostrar as informações no Site ----
    for post in posts:
        st.subheader(post['title'])
        st.write(post['body'])
        st.write('---')
except requests.exceptions.RequestException as e:
    #--Caso ocorra algum erro de conexão
    st.error(f'Erro ao acessar ao API: {e}')
