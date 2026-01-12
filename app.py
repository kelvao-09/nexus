import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Configuração Principal
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

# Inicializar histórico
if 'historico' not in st.session_state:
    st.session_state.historico = []

# 2. Estilos CSS (Sofisticação Visual)
st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; }
    .main-title {
        text-align: center; font-weight: 300;
        font-size: 3.5rem; color: #1A1A1B; margin-bottom: 5px;
    }
    .stTextInput input {
        border-radius: 30px !important; padding: 12px 25px !important;
        border: 1px solid #E0E0E0 !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03) !important;
    }
    /* Tags de Histórico */
    div.stButton > button {
        border-radius: 20px !important; background-color: #E8EAED !important;
        color: #5F6368 !important; border: none !important;
        padding: 4px 15px !important; font-size: 0.85rem !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #4285F4 !important; color: white !important;
    }
    /* Botão Limpar Especial */
    .clear-btn button {
        background-color: transparent !important;
        color: #999 !important; border: 1px solid #EEE !important;
    }
    .clear-btn button:hover {
        border-color: #FF4B4B !important; color: #FF4B4B !important;
