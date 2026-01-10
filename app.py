import streamlit as st
import pandas as pd

# 1. Configuração da página (deve ser a primeira instrução)
st.set_page_config(page_title="Nexus Dashboard", layout="wide")

# --- CABEÇALHO COM BOTÃO NO CANTO DIREITO ---
# Criamos 3 colunas: uma para o título, uma grande vazia no meio e uma pequena para o botão
col_titulo, col_espaco, col_switch = st.columns([2, 5, 1])

with col_titulo:
    st.title("Nexus")

with col_switch:
    # O botão fica alinhado à direita, próximo aos ícones nativos do Streamlit
    modo_noturno = st.toggle("Modo Noturno")

# --- LÓGICA DE CORES SOFISTICADAS ---
if modo_noturno:
    # Paleta Escura: Fundo Anthracite, Texto Off-white e Destaques Suaves
    st.markdown("""
        <style>
        .stApp {
            background-color: #1A1C20;
            color: #F0F2F6;
        }
        [data-testid="stMetricValue"] {
            color: #FFFFFF !important;
        }
        [data-testid="stMetricLabel"] {
            color: #A1A3A6 !important;
        }
        blockquote {
            border-left: 5px solid #3E4452 !important;
            background-color: #262930 !important;
            color: #D1D5DB !important;
        }
        /* Cor da tabela no modo escuro */
        .stDataFrame {
            border: 1px solid #3E4452;
        }
        </style>
        """, unsafe_allow_html=True)
else:
    # Paleta Clara: Visual limpo idêntico à sua captura de tela
    st.markdown("""
        <style>
        blockquote {
            border-left: 5px solid #E6E9EF;
            background-color: #F8F9FB;
            color: #555E6F;
        }
        </style>
        """, unsafe_allow_html=True)

# --- CONTEÚDO ---

# Justificativa do Nome
st.markdown("""
> **NEXUS** representa a conexão essencial entre atenção, esforço e gentileza.  
> É o elo que une nossa equipe, fortalecendo a colaboração e o comprometimento  
> para alcançar resultados de excelência.
""")

st.divider()

# --- SEÇÃO DE METAS ---
st.header("Acompanhamento de Metas")

# Dados de exemplo
meta_total = 100000.00
alcancado = 75000.00
progresso = alcancado / meta_total

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(label="Meta Total", value=f"R$ {meta_total:,.2f}")

with c2:
    # Delta indica a porcentagem atingida de forma elegante
    st.metric(label="Alcançado", value=f"R$ {alcancado:,.2f}", delta=f"{progresso:.1%}")

with c3:
    st.write("**Progresso da Equipe**")
    st.progress(progresso)

st.write("") # Espaçamento

# --- TABELA DE DESEMPENHO ---
st.subheader("Desempenho por Integrante")

df = pd.DataFrame({
    "Integrante": ["Ana", "Bruno", "Carlos", "Daniela"],
    "Meta Individual": [25000, 25000, 25000, 25000],
    "Realizado": [22000, 18000, 25000, 10000],
})
df["Status (%)"] = (df["Realizado"] / df["Meta Individual"]) * 100

# Exibição da tabela ocupando a largura total
st.dataframe(df, use_container_width=True, hide_index=True)

# Efeito final de celebração se a meta for atingida
if progresso >= 1.0:
    st.balloons()
