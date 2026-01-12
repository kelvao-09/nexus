import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Configuração de Alta Performance
st.set_page_config(page_title="Oráculo | Inteligência de Dados", page_icon="🔮", layout="wide")

# Inicializar histórico
if 'historico' not in st.session_state:
    st.session_state.historico = []

# 2. CSS Customizado para Sofisticação
st.markdown("""
<style>
    /* Fundo e Fonte Principal */
    .stApp { background-color: #FDFDFD; }
    
    /* Título Centralizado e Elegante */
    .main-title {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #1E1E1E;
        text-align: center;
        font-weight: 300;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }

    /* Estilização da Barra de Pesquisa */
    .stTextInput input {
        border-radius: 25px !important;
        border: 1px solid #E0E0E0 !important;
        padding: 10px 25px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }

    /* Botões de Histórico como Tags */
    div.stButton > button {
        border-radius: 20px !important;
        background-color: #F0F2F6 !important;
        color: #555 !important;
        border: none !important;
        padding: 4px 15px !important;
        font-size: 0.85rem !important;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #4285F4 !important;
        color: white !important;
    }

    /* Card de Resultados */
    .result-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #F0F0F0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Link 'Abrir' Sofisticado */
    .btn-link {
        color: #4285F4 !important;
        text-decoration: none !important;
        font-weight: 600;
        font-size: 0.9rem;
        border: 1px solid #4285F4;
        padding: 6px 16px;
        border-radius: 6px;
        transition: 0.3s;
    }
    .btn-link:hover {
        background: #4285F4;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Autenticação Drive
@st.cache_resource
def get_drive_service():
    try:
        if "google_auth" in st.secrets:
            creds = service_account.Credentials.from_service_account_info(
                st.secrets["google_auth"], 
                scopes=['https://www.googleapis.com/auth/drive.readonly']
            )
            return build('drive', 'v3', credentials=creds)
    except: return None
    return None

service = get_drive_service()

# 4. Conteúdo Central
st.markdown('<h1 class="main-title">🔮 Oráculo</h1>', unsafe_allow_html=True)
st.
