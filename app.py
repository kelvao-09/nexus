import streamlit as st
import pandas as pd

# 1. Configuração da página
st.set_page_config(page_title="Nexus Dashboard", layout="wide")

# --- CABEÇALHO COM BOTÃO NO CANTO DIREITO ---
col_titulo, col_espaco, col_switch = st.columns([2, 5, 1])

with col_titulo:
    st.title("Nexus")

with col_switch:
    modo_noturno = st.toggle("Modo Noturno")

# --- LÓGICA DE CORES SOFISTICADAS ---
if modo_noturno:
    st.markdown("""
        <style>
        .stApp { background-color: #1A1C20; color: #F0F2F6; }
        [data-testid="stMetricValue"] { color: #FFFFFF !important; }
        [data-testid="stMetricLabel"] { color: #A1A3A6 !important; }
        blockquote { border-left: 5px solid #3E4452 !important; background-color: #262930 !important; color: #D1D5DB !important; }
        .stDataFrame { border: 1px solid #3E4452; }
        </style>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        blockquote { border-left: 5px solid #E6E9EF; background-color: #F8F9FB; color: #555E6F; }
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

# Lista de Colaboradores
colaboradores = [
    "ANDERSON GABRIEL ALVES LIMA", "GEOVAN GOMES DE OLIVEIRA JUNIOR", "DAVI COSTA ALVES",
    "KETILY KAYANE QUEIROZ ALVES", "FRANCISCO HIGO DAMACENA SOUZA", "AMANDA CRISTINA DA SILVA",
    "LYLYAN VITORIA CAMPELO DE FRANCA", "THIAGO DE FREITAS LIMA", "CARLOS EDUARDO ARRUDA SILVA",
    "MATHEUS IRLAN NASCIMENTO BESSA", "JOAO VICTOR FAGUNDES DA SILVA", "WILMA SAMARA SILVA MENDONCA",
    "MAURICIO PAULINO FLORES JUNIOR", "MATHEUS KAWAN OLIVEIRA SANTOS", "JOSEFA FERNANDA DA SILVA",
    "FRANCISCO BRUNO VICTOR SOUZA"
]

# Configurações de Valores
