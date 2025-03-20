import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

#acesso ao banco 
def get_connection():
    return sqlite3.connect("erp_finance.db", detect_types=sqlite3.PARSE_DECLTYPES)

#Consulta Fornecedor
def fetch_contas_pagar_agrupado():
    conn = get_connection()
    query = """
    SELECT fornecedor, SUM(valor) as total_devido
    FROM contas_pagar
    GROUP BY fornecedor
    ORDER BY total_devido DESC
    LIMIT 10
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def main():
    st.title("Distribuição das Contas a Pagar por Fornecedor")
    df = fetch_contas_pagar_agrupado()
    if df.empty:
        st.warning("Nenhum dado disponível para exibição.")
        return
    
    st.subheader("Principais fornecedores e valores")
    st.dataframe(df)

    # Menu - Escolha do tipo de gráfico
    tipo_grafico = st.radio("Escolha o tipo de gráfico:", ("Pizza", "Barras"))

    fig, ax = plt.subplots(figsize=(8, 5))

    if tipo_grafico == "Pizza":
        ax.pie(df["total_devido"], labels=df["fornecedor"], autopct="%1.1f%%", startangle=90, colors=plt.cm.Paired.colors)
        ax.set_title("Distribuição por Fornecedor")
    
    elif tipo_grafico == "Barras":
        ax.bar(df["fornecedor"], df["total_devido"], color="red")
        ax.set_xlabel("Fornecedor")
        ax.set_ylabel("Valor (R$)")
        ax.set_title("Valores por Fornecedor")
        ax.set_xticklabels(df["fornecedor"], rotation=45, ha="right")

    st.pyplot(fig)

if __name__ == "__main__":
    main()
