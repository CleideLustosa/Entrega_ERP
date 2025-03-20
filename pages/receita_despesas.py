import streamlit as st
import sqlite3
import pandas as pd
import datetime

# Acesso ao banco
def get_connection():
    return sqlite3.connect("erp_finance.db", detect_types=sqlite3.PARSE_DECLTYPES)

# Calcula Receita x Despesas
def fetch_receita_despesa():
    conn = get_connection()
    cursor = conn.cursor()
    
    today = datetime.date.today()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = (first_day_of_month + datetime.timedelta(days=31)).replace(day=1) - datetime.timedelta(days=1)
    
    query_receita = """
    SELECT SUM(valor) AS total_receita
    FROM lancamentos
    WHERE tipo = 'Receita' AND data BETWEEN ? AND ?
    """
    query_despesa = """
    SELECT SUM(valor) AS total_despesa
    FROM lancamentos
    WHERE tipo = 'Despesa' AND data BETWEEN ? AND ?
    """
    
    cursor.execute(query_receita, (first_day_of_month, last_day_of_month))
    total_receita = cursor.fetchone()[0] or 0  
    
    cursor.execute(query_despesa, (first_day_of_month, last_day_of_month))
    total_despesa = cursor.fetchone()[0] or 0  
    
    conn.close()
    
    return total_receita, total_despesa

def main():
    st.title("Receita x Despesa - Mês Atual")
    
    total_receita, total_despesa = fetch_receita_despesa()
    
    st.subheader("Totais do mês atual:")
    st.write(f"Receita Total: R$ {total_receita:,.2f}")
    st.write(f"Despesa Total: R$ {total_despesa:,.2f}")
    
    
    st.subheader("Receita vs Despesas")
    data = pd.DataFrame({
        "Categoria": ["Receita", "Despesa"],
        "Total": [total_receita, total_despesa]
    })
    st.bar_chart(data.set_index("Categoria"))

if __name__ == "__main__":
    main()


