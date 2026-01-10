import streamlit as st
import pandas as pd

# 1. Configuração da página (DEVE ser a primeira linha de comando Streamlit)
st.set_page_config(page_title="Nexus Dashboard", layout="wide")

# --- MODO NOTURNO (OPÇÃO NATIVA) ---
# DICA: O Streamlit detecta o tema do Windows/Browser automaticamente.
# Mas você pode forçar um botão de alternância visual se desejar.
with st.sidebar:
    st.title("Configurações")
    tema = st.toggle("Ativar Modo Escuro Manual")

# Se você quiser que o app mude cores específicas via código:
if tema:
    st.markdown("""
        <style>
        .stApp {
            background-color: #0E1117;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)

# --- CONTEÚDO DO DASHBOARD ---

# Título Principal
st.title("Nexus")

# Justificativa do Nome
st.markdown("""
> **NEXUS** representa a conexão essencial entre atenção, esforço e gentileza. 
> É o elo que une nossa equipe, fortalecendo a colaboração e o comprometimento 
> para alcançar resultados de excelência.
""")

st.divider()

# --- ÁREA DE METAS DA EQUIPE ---
st.header("Acompanhamento de Metas")

meta_global = 100000
alcancado = 75000
progresso = alcancado / meta_global

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Meta Total", value=f"R$ {meta_global:,.2f}")

with col2:
    st.metric(label="Alcançado", value=f"R$ {alcancado:,.2f}", delta=f"{progresso:.1%}")

with col3:
    st.write("**Progresso da Equipe**")
    st.progress(progresso)

# --- TABELA DE MEMBROS DA EQUIPE ---
st.subheader("Desempenho por Integrante")

dados_equipe = pd.DataFrame({
    "Integrante": ["Ana", "Bruno", "Carlos", "Daniela"],
    "Meta Individual": [25000, 25000, 25000, 25000],
    "Realizado": [22000, 18000, 25000, 10000],
})

dados_equipe["Status (%)"] = (dados_equipe["Realizado"] / dados_equipe["Meta Individual"]) * 100

st.dataframe(dados_equipe, use_container_width=True)

if progresso >= 1.0:
    st.balloons()
    st.success("Excelente! O elo Nexus nos levou ao objetivo!")
