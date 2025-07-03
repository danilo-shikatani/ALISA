import streamlit as st
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Visualizador de Extrato", layout="centered")
st.title("📄 Visualizador de Extrato Bancário - Junho 2025")

# Upload do arquivo
uploaded_file = st.file_uploader("📂 Envie o arquivo Excel do extrato", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name='Extratos')

    # Filtros para 'Historico'
    historico_filters = ['78349656', '42293670', '81876858', '9991621860', '7111107', '2808376752']

    # Filtragem
    df_filtered = df[df['Historico'].astype(str).str.contains('|'.join(historico_filters), na=False)]
    df_filtered['Historico'] = df_filtered['Historico'].apply(lambda x: str(x)[:6] if pd.notnull(x) else x)

    # Agrupamento e soma
    resumo = df_filtered.groupby('Historico')['Valor'].sum().reset_index()
    total_geral = df_filtered['Valor'].sum()

    # Exibição
    st.subheader("🔍 Valores por Histórico")
    st.dataframe(resumo, use_container_width=True)

    st.subheader("🧮 Total Geral")
    st.metric("💰 Valor Total", f"R$ {total_geral:,.2f}".replace('.', 'X').replace(',', '.').replace('X', ','))

else:
    st.info("⏳ Aguardando o envio do arquivo `.xlsx` com a aba `Extratos`.")
