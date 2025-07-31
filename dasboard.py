import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configurações da página
st.set_page_config(
    page_title="Dashboard Provedor de Internet",
    page_icon="🌐",
    layout="wide"
)

# Função para carregar dados
@st.cache_data
def load_data(uploaded_file):
    df = pd.read_excel(uploaded_file)
    
    # Conversões
    df["Vencimento"] = pd.to_datetime(df["Vencimento"], dayfirst=True)
    df["Status"] = df["Status"].map({1: "Ativo", 0: "Cancelado"})
    df["Mês"] = df["Vencimento"].dt.strftime("%Y-%m")
    
    return df

# Interface
st.title("🌐 Dashboard Provedor de Internet")
st.markdown("---")

# Upload de arquivo
uploaded_file = st.file_uploader(
    "Carregue seu arquivo XLSX",
    type="xlsx",
    help="Formato exigido: Colunas 'Cliente', 'Contrato_ID', 'Status', 'Login', 'Vencimento', 'Valor'"
)

if uploaded_file:
    df = load_data(uploaded_file)
    
    # Sidebar - Filtros
    st.sidebar.title("Filtros")
    status_filter = st.sidebar.multiselect(
        "Status do Contrato",
        options=df["Status"].unique(),
        default=["Ativo"]
    )
    
    date_filter = st.sidebar.date_input(
        "Período de Vencimento",
        value=[df["Vencimento"].min(), df["Vencimento"].max()],
        min_value=df["Vencimento"].min(),
        max_value=df["Vencimento"].max()
    )
    
    # Aplicar filtros
    filtered_df = df[
        (df["Status"].isin(status_filter)) &
        (df["Vencimento"].between(*date_filter))
    ]
    
    # Métricas
    st.header("Principais Indicadores")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Contratos", len(df))
    with col2:
        st.metric("Contratos Ativos", len(df[df["Status"] == "Ativo"]))
    with col3:
        st.metric("Valor Mensal (R$)", 
                 f"R$ {filtered_df[filtered_df['Status'] == 'Ativo']['Valor'].sum():,.2f}")
    
    # Gráficos
    st.header("Análise Visual")
    tab1, tab2 = st.tabs(["Evolução Mensal", "Distribuição"])
    
    with tab1:
        monthly_data = df.groupby(["Mês", "Status"]).size().reset_index(name="Contratos")
        fig = px.line(
        monthly_data,
        x="Mês",
        y="Contratos",
        color="Status",
        title="Contratos Ativos vs Cancelados",
        color_discrete_sequence=px.colors.qualitative.Plotly  # 👈 Aqui aplicamos a paleta
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig = px.pie(
            df,
            names="Status",
            title="Distribuição de Status"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabela
    st.header("Dados Detalhados")
    st.dataframe(
        filtered_df,
        column_config={
            "Vencimento": st.column_config.DateColumn("Vencimento", format="DD/MM/YYYY"),
            "Valor": st.column_config.NumberColumn("Valor", format="R$ %.2f")
        },
        hide_index=True,
        use_container_width=True
    )

else:
    st.warning("Por favor, carregue um arquivo para visualizar o dashboard.")
    st.info("Use o arquivo 'exemplo.xlsx' para testes.")