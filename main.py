import streamlit as st
import pandas as pd
import plotly.express as px
from utils import carregar_dados, filtrar_dados, calcular_metricas
from datetime import datetime

st.set_page_config(page_title="Dashboard Provedor de Internet", layout="wide")
st.markdown('<link rel="stylesheet" href="style.css">', unsafe_allow_html=True)

st.title("📊 Dashboard Provedor de Internet")

# Upload do arquivo
arquivo = st.file_uploader("Upload de Dados (.XLSX)", type=["xlsx"])

if arquivo:
    df = carregar_dados(arquivo)

    # Filtros
    cliente_selecionado = st.multiselect("Filtro por Cliente", options=sorted(df['Cliente'].unique()))
    status_selecionado = st.multiselect("Filtro por Status", options=sorted(df['Status'].unique()))
    data_inicio = st.date_input("Data Inicial", value=datetime(2023, 1, 1))
    data_fim = st.date_input("Data Final", value=datetime(2023, 12, 31))

    dados_filtrados = filtrar_dados(df, cliente_selecionado, status_selecionado, data_inicio, data_fim)

    # Métricas
    total, ativos, cancelados, valor_total, media_valor = calcular_metricas(dados_filtrados)
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("🗂️ Total de Contratos", total)
    col2.metric("✅ Contratos Ativos", ativos)
    col3.metric("❌ Contratos Cancelados", cancelados)
    col4.metric("💰 Valor Total (Ativos)", f"R$ {valor_total:,.2f}")
    col5.metric("📎 Média por Contrato", f"R$ {media_valor:,.2f}")

    # Gráficos
    df_temp = dados_filtrados.copy()
    df_temp['Ano'] = df_temp['Vencimento'].dt.year
    df_temp['Mês'] = df_temp['Vencimento'].dt.month

    with st.expander("📈 Contratos Ativos x Cancelados"):
        linha = px.line(df_temp, x='Vencimento', y='Contrato_ID', color='Status', markers=True,
                        title="Evolução de Contratos")
        st.plotly_chart(linha, use_container_width=True)

    with st.expander("📊 Distribuição por Status"):
        pizza = px.pie(df_temp, names='Status', title="Distribuição de Clientes por Status")
        st.plotly_chart(pizza, use_container_width=True)

    with st.expander("💸 Receita Mensal/Anual"):
        receita = df_temp[df_temp['Status'] == 'Ativo'].groupby(['Ano', 'Mês'])['Valor'].sum().reset_index()
        area = px.area(receita, x='Mês', y='Valor', color='Ano', title="Receita por Período")
        st.plotly_chart(area, use_container_width=True)

    # Tabela
    with st.expander("📋 Tabela de Contratos"):
        st.dataframe(dados_filtrados)
else:
    st.info("⚠️ Por favor, faça o upload de um arquivo .XLSX com os dados.")