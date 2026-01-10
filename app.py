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
            background-color: #F9
