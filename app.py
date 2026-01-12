import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Configuração da Página
st.set_page_config(page_title="Oráculo Pro", page_icon="🔮", layout="wide")

# Inicializar o estado de favoritos se não existir
if 'favoritos' not in st.session_state:
    st.session_state.favoritos = []

# 2. Estilo CSS (Corrigido para evitar SyntaxError)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    
    /* Card de Documento Principal */
    .doc-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #efefef;
    }
    
    /* Sidebar de Favoritos */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }
    
    .fav-item {
        background: #fdfdfd;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 4px solid #FFD700;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
    }
    
    .btn-open {
        background-color: #4285F4;
        color: white !important;
        padding: 8px 18px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Autenticação Drive
@st.cache_resource
def get_drive_service():
    try:
