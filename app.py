import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração da Página
st.set_page_config(page_title="Nexus Dashboard", layout="wide", page_icon="📊")

st.title("📊 Painel de Indicadores - Nexus")
st.markdown("---")

# 2. Carregamento dos Dados
@st.cache_data
def load_data():
    # O seu link direto do GitHub
    url = "https://raw.githubusercontent.com/kelvao-09/nexus/refs/heads/main/.devcontainer/TAM.csv"
    return pd.read_csv(url)

try:
    df = load_data()

    # 3. Métricas de Resumo (Exemplo: Total de linhas)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Registros", len(df))
    
    # 4. Exibição da Tabela
    st.subheader("📋 Visualização dos Dados (TAM)")
    st.dataframe(df, use_container_width=True)

    # 5. Gráfico Automático
    # Ele tenta encontrar colunas com números para criar um gráfico
    colunas_numericas = df.select_dtypes(include=['number']).columns.tolist()
    
    if colunas_numericas:
        st.markdown("---")
        st.subheader("📈 Análise Visual")
        metrica = st.selectbox("Selecione a métrica para visualizar:", colunas_numericas)
        
        # Cria um gráfico de barras (ajuste 'x' para o nome de uma coluna de texto se souber qual é)
        eixo_x = df.columns[0] # Pega a primeira coluna (ex: Nome ou Data) para o eixo X
        fig = px.bar(df, x=eixo_x, y=metrica, title=f"Distribuição de {metrica}", color=metrica)
        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar o arquivo: {e}")
    st.info("Certifique-se de que o arquivo TAM.csv está no caminho correto dentro do GitHub.")
