import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Configuração de Interface
st.set_page_config(page_title="Oráculo | Search", page_icon="🔮", layout="wide")

# Inicializar histórico na sessão
if 'historico' not in st.session_state:
    st.session_state.historico = []

# 2. Design de Interface (CSS Sofisticado)
st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; }
    .main-title {
        text-align: center;
        font-weight: 300;
        font-size: 3.5rem;
        color: #1A1A1B;
        margin-bottom: 0px;
    }
    .stTextInput input {
        border-radius: 30px !important;
        padding: 12px 25px !important;
        border: 1px solid #E0E0E0 !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03) !important;
    }
    div.stButton > button {
        border-radius: 20px !important;
        background-color: #E8EAED !important;
        color: #5F6368 !important;
        border: none !important;
        padding: 4px 15px !important;
        font-size: 0.85rem !important;
    }
    div.stButton > button:hover {
        background-color: #4285F4 !important;
        color: white !important;
    }
    .result-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1px solid #EEE;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .btn-visualizar {
        background-color: #4285F4;
        color: white !important;
        text-decoration: none !important;
        padding: 8px 20px;
        border-radius: 6px;
        font-weight: 500;
        transition: 0.3s;
    }
</style>
""", unsafe_allow_html=True)

# 3. Autenticação Drive (Linhas encurtadas para evitar cortes)
@st.cache_resource
def get_drive_service():
