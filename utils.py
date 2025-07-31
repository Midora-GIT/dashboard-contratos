import pandas as pd

def carregar_dados(arquivo):
    df = pd.read_excel(arquivo, engine="openpyxl")
    df['Valor'] = df['Valor'].apply(tratar_valor)
    df['Vencimento'] = pd.to_datetime(df['Vencimento'], format="%d/%m/%Y")
    df['Status'] = df['Status'].map({1: "Ativo", 0: "Cancelado"})
    return df

def tratar_valor(valor_str):
    valor_str = str(valor_str).replace('.', '').replace(',', '.')
    try:
        return float(valor_str)
    except:
        return 0.0

def filtrar_dados(df, clientes, status, data_ini, data_fim):
    if clientes:
        df = df[df['Cliente'].isin(clientes)]
    if status:
        df = df[df['Status'].isin(status)]
    df = df[(df['Vencimento'] >= pd.to_datetime(data_ini)) & (df['Vencimento'] <= pd.to_datetime(data_fim))]
    return df

def calcular_metricas(df):
    total = len(df)
    ativos = len(df[df['Status'] == "Ativo"])
    cancelados = len(df[df['Status'] == "Cancelado"])
    valor_total = df[df['Status'] == "Ativo"]['Valor'].sum()
    media_valor = df[df['Status'] == "Ativo"]['Valor'].mean() if ativos > 0 else 0
    return total, ativos, cancelados, valor_total, media_valor
