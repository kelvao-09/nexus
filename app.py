import streamlit as st
import pandas as pd

# 1. Configuração da página
st.set_page_config(page_title="Nexus Dashboard", layout="wide")

# --- CABEÇALHO COM BOTÃO INTEGRADO ---
# Criamos colunas para posicionar o título à esquerda e o botão à direita no topo
col_titulo, col_vazia, col_toggle = st.columns([3, 2, 1])

with col_titulo:
    st.title("Nexus")

with col_toggle:
    # O botão fica no topo, simulando o switch da sua imagem
    modo_noturno = st.toggle("Modo Noturno", value=False)

# --- ESTILIZAÇÃO SOFISTICADA (CSS) ---
if modo_noturno:
    # Cores para Modo Noturno: Fundo Grafite Profundo, Texto Branco Neve
    st.markdown("""
        <style>
        .stApp {
            background-color: #121212;
            color: #E0E0E0;
        }
        [data-testid="stMetricValue"] {
            color: #FFFFFF !important;
        }
        [data-testid="stMetricLabel"] {
            color: #B0B0B0 !important;
        }
        blockquote {
            border-left: 5px solid #4F4F4F !important;
            color: #BBBBBB !important;
            background-color: #1E1E1E !important;
        }
        /* Estilização da Tabela no Modo Escuro */
        .stDataFrame div {
            color: #E0E0E0 !important;
        }
        hr {
            border-top: 1px solid #333333 !important;
        }
        </style>
        """, unsafe_allow_html=True)
else:
    # Cores para Modo Claro: Fundo Branco, Texto Cinza Escuro
    st.markdown("""
        <style>
        blockquote {
            border-left: 5px solid #E0E0E0;
            background-color: #F9F9F9;
        }
        </style>
        """, unsafe_allow_html=True)

# --- CONTEÚDO DO DASHBOARD ---

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
    # A barra de progresso do Streamlit já se adapta bem aos temas
    st.progress(progresso)

# --- TABELA DE MEMBROS DA EQUIPE ---
st.subheader("Desempenho por Integrante")

dados_equipe = pd.DataFrame({
    "Integrante": ["Ana", "Bruno", "Carlos", "Daniela"],
    "Meta Individual": [25000, 25000, 25000, 25000],
    "Realizado": [22000, 18000, 25000, 10000],
})
dados_equipe["Status (%)"] = (dados_equipe["Realizado"] / dados_equipe["Meta Individual"]) * 100

# Exibe a tabela
st.dataframe(dados_equipe, use_container_width=True)

# Feedback visual de sucesso
if progresso >= 0.75:
    st.toast("Estamos no caminho certo para a meta Nexus!", icon="🚀")
