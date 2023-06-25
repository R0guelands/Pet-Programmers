import pandas as pd
import sqlite3
import streamlit as st
from streamlit_extras.dataframe_explorer import dataframe_explorer
import openpyxl
import re
import base64

tabelas = []  # Lista para armazenar os nomes das tabelas


def sidebar_bg(side_bg):

   side_bg_ext = 'png'

   st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
        background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
        background-repeat: no-repeat;
        background-repeat: no-repeat;
        background-size: 131px;
        background-position: 50% 0%;
        padding-top: 0px;
      }}
      [data-testid="stSidebarNav"]::before {{
                content: "";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }}
      </style>
      """,
      unsafe_allow_html=True,
      )
   
side_bg = 'app/img/logo.png'
sidebar_bg(side_bg)

def formatar_nome_tabela(nome_arquivo):
    nome_arquivo = re.sub(r'\W+', '_', nome_arquivo)  # Substitui caracteres não alfanuméricos por underscores
    nome_arquivo = nome_arquivo.lower()  # Converte para minúsculas
    return nome_arquivo

def ler_excel_criar_db(nome_arquivo):
    # Extrair o nome do arquivo sem a extensão
    nome_tabela = formatar_nome_tabela(nome_arquivo.name.split('.')[0])

    # Ler o arquivo Excel
    df = pd.read_excel(nome_arquivo, engine='openpyxl')

    # Conectar ao banco de dados SQLite3
    conn = sqlite3.connect("excel_data.db")
    cursor = conn.cursor()

    # Criar tabela no banco de dados
    df.to_sql(nome_tabela, conn, if_exists='replace', index=False)

    # Adicionar o nome da tabela à lista de tabelas
    tabelas.append(nome_tabela)

    # Fechar a conexão com o banco de dados
    conn.close()

    return df

def obter_todas_as_tabelas():
    # Conectar ao banco de dados SQLite3
    conn = sqlite3.connect("excel_data.db")

    # Consultar as tabelas no banco de dados
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name is not 'sqlite_sequence' ")
    tabelas = cursor.fetchall()

    # Fechar a conexão com o banco de dados
    conn.close()

    # Retornar uma lista de nomes de tabelas
    return [tabela[0] for tabela in tabelas]

def inserir_dados(nome_tabela, dados):
    # Conectar ao banco de dados SQLite3
    conn = sqlite3.connect("excel_data.db")
    cursor = conn.cursor()

    # Inserir os dados na tabela
    cursor.executemany(f"INSERT INTO {nome_tabela} VALUES ({', '.join(['?'] * len(dados[0]))})", dados)

    # Commit as alterações
    conn.commit()

    # Fechar a conexão com o banco de dados
    conn.close()

def atualizar_dados(nome_tabela, coluna_atualizar, valor_atualizar, coluna_condicao, valor_condicao):
    # Conectar ao banco de dados SQLite3
    conn = sqlite3.connect("excel_data.db")
    cursor = conn.cursor()

    # Atualizar os dados na tabela
    cursor.execute(f"UPDATE {nome_tabela} SET {coluna_atualizar} = ? WHERE {coluna_condicao} = ?", (valor_atualizar, valor_condicao))

    # Commit as alterações
    conn.commit()

    # Fechar a conexão com o banco de dados
    conn.close()

def remover_dados(nome_tabela, coluna_condicao, valor_condicao):
    # Conectar ao banco de dados SQLite3
    conn = sqlite3.connect("excel_data.db")
    cursor = conn.cursor()

    # Remover os dados da tabela
    cursor.execute(f"DELETE FROM {nome_tabela} WHERE {coluna_condicao} = ?", (valor_condicao,))

    # Commit as alterações
    conn.commit()

    # Fechar a conexão com o banco de dados
    conn.close()
    
def remover_tabela(nome_tabela):
    # Conectar ao banco de dados SQLite3
    conn = sqlite3.connect("excel_data.db")
    cursor = conn.cursor()

    # Remover os dados da tabela
    cursor.execute(f"DROP TABLE {nome_tabela}")

    # Commit as alterações
    conn.commit()

    # Fechar a conexão com o banco de dados
    conn.close()

def expander_dml(key,tabela, df):
    with st.expander("Inserir/Atualizar/Deletar Registros"):
        operacao = st.selectbox("Operação:", ["Inserir", "Atualizar", "Deletar", "Deletar Tabela"], key=f"operacao_{key}")

        if operacao == "Inserir":
            st.subheader("Inserir Registros")
            form = st.form(key=f"form_inserir_{key}")
            dados = {}
            for coluna in df.columns:
                valor = form.text_input(coluna)
                dados[coluna] = valor
            if form.form_submit_button("Inserir Registros"):
                inserir_dados(tabela, [tuple(dados.values())])
                st.success("Registros inseridos com sucesso!")

        elif operacao == "Atualizar":
            st.subheader("Atualizar Registros")
            form = st.form(key=f"form_atualizar_{key}")
            coluna_atualizar = form.selectbox("Coluna a ser atualizada:", df.columns)
            valor_atualizar = form.text_input("Novo valor")
            coluna_condicao = form.selectbox("Coluna de condição:", df.columns)
            valor_condicao = form.text_input("Valor de condição")
            if form.form_submit_button("Atualizar Registros"):
                atualizar_dados(tabela, coluna_atualizar, valor_atualizar, coluna_condicao, valor_condicao)
                st.success("Registros atualizados com sucesso!")

        elif operacao == "Deletar":
            st.subheader("Deletar Registros")
            form = st.form(key=f"form_deletar_{key}")
            coluna_condicao = form.selectbox("Coluna de condição:", df.columns)
            valor_condicao = form.text_input("Valor de condição")
            if form.form_submit_button("Deletar Registros"):
                remover_dados(tabela, coluna_condicao, valor_condicao)
                st.success("Registros deletados com sucesso!")
                
        elif operacao == "Deletar Tabela":
            st.subheader("Deletar Tabela")
            form = st.form(key=f"form_drop_table_{key}")
            if form.form_submit_button("Deletar Tabela"):
                remover_tabela(tabela)
                st.success("Tabela deletada com sucesso!")

def plotar_tabelas(dml_on = False):
    # Obter todas as tabelas existentes
    todas_as_tabelas = obter_todas_as_tabelas()

    # Dividir a página em colunas
    num_colunas = len(todas_as_tabelas)
    colunas = st.columns(num_colunas)

    for i, tabela in enumerate(todas_as_tabelas):
    #     with colunas[i]:
        st.subheader(tabela)
        # Conectar ao banco de dados SQLite3
        conn = sqlite3.connect("excel_data.db")

        # Consultar os dados da tabela
        df = pd.read_sql_query(f"SELECT * FROM {tabela}", conn)
        # filtered_df = dataframe_explorer(df, case=False)
        # st.dataframe(filtered_df, use_container_width=True)
        # st.dataframe(df) # Mostrar a tabela no Streamlit
        st.table(df) # Mostrar a tabela no Streamlit

        if dml_on:
            expander_dml(key=f"expander_{tabela}", tabela=tabela, df=df)

       # C
                            
        # Fechar a conexão com o banco de dados
    conn.close()

def main():
    # Título da página
    st.title('Planilhas Estoques')
        
    # Upload do arquivo Excel
    arquivo_excel = st.file_uploader('Selecione o arquivo Excel', type=['xlsx'])
    if arquivo_excel is not None:
        # Ler o arquivo Excel e criar o banco de dados
        df = ler_excel_criar_db(arquivo_excel)

        # Plotar a tabela
        # plotar_tabelas()

    # # Botão para criar nova tabela
    # if st.button("Criar nova tabela"):
    # Plotar todas as tabelas existentes
    plotar_tabelas(dml_on=True)


if __name__ == '__main__':
    main()

