import streamlit as st
import sqlite3
import pandas as pd
import datetime

# Acesso ao banco de dados
def get_connection():
    return sqlite3.connect("erp_finance.db", detect_types=sqlite3.PARSE_DECLTYPES)
#Fluxo de 30 dias
def fetch_fluxo_de_caixa():
    conn = get_connection()
    today = datetime.date.today()
    data_limite = today + datetime.timedelta(days=30)

    query = """
    SELECT
        'Contas a Pagar' AS tipo,
        vencimento,
        fornecedor AS descricao,
        valor
    FROM contas_pagar
    WHERE vencimento BETWEEN ? AND ?
    UNION
    SELECT
        'Contas a Receber' AS tipo,
        cr.vencimento,
        cl.nome AS descricao,
        cr.valor
    FROM contas_receber cr
    INNER JOIN clientes cl ON cr.cliente_id = cl.id
    WHERE cr.vencimento BETWEEN ? AND ?
    ORDER BY vencimento;
    """
    
    df = pd.read_sql_query(query, conn, params=(today, data_limite, today, data_limite))
    conn.close()
    return df

def main():
    st.title("Fluxo de Caixa - Contas a Pagar e Receber nos Próximos 30 Dias")
    
    df = fetch_fluxo_de_caixa()
    if df.empty:
        st.warning("Não há contas a pagar ou a receber nos próximos 30 dias.")
        return
    
    st.subheader("Contas a Pagar e a Receber nos Próximos 30 Dias")
    st.dataframe(df)

    
    total_pagar = df[df['tipo'] == 'Contas a Pagar']['valor'].sum()
    total_receber = df[df['tipo'] == 'Contas a Receber']['valor'].sum()

    saldo_futuro = total_receber - total_pagar

    st.subheader(f"Saldo Futuro Estimado: R$ {saldo_futuro:,.2f}")
    st.write(f"Total de Contas a Pagar: R$ {total_pagar:,.2f}")
    st.write(f"Total de Contas a Receber: R$ {total_receber:,.2f}")
    
    st.subheader("Fluxo de Caixa")
    st.bar_chart(df.groupby("tipo")["valor"].sum())

if __name__ == "__main__":
    main()
