import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Configuração de Interface
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

if 'historico' not in st.session_state:
    st.session_state.historico = []

# 2. Design de Interface (CSS Consolidado para evitar erros)
st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; }
    .main-title { text-align: center; font-weight: 300; font-size: 3.5rem; color: #1A1A1B; }
    .stTextInput input { border-radius: 30px !important; padding: 12px 25px !important; border: 1px solid #E0E0E0 !important; }
    div.stButton > button { border-radius: 20px !important; background-color: #E8EAED !important; color: #5F6368 !important; border: none !important; }
    div.stButton > button:hover { background-color: #4285F4 !important; color: white !important; }
    .result-card { background: white; padding: 1.2rem; border-radius: 12px; margin-bottom: 1rem; border: 1px solid #EEE; display: flex; justify-content: space-between; align-items: center; }
    .btn-visualizar { background-color: #4285F4; color: white !important; text-decoration: none !important; padding: 8px 20px; border-radius: 6px; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# 3. Autenticação Drive
@st.cache_resource
def get_drive_service():
    try:
        if "google_auth" in st.secrets:
            info = st.secrets["google_auth"]
            scope = ['https://www.googleapis.com/auth/drive.readonly']
            creds = service_account.Credentials.from_service_account_info(info, scopes=scope)
            return build('drive', 'v3', credentials=creds)
    except: return None
    return None

service = get_drive_service()

# 4. Título e Barra de Pesquisa
st.markdown('<h1 class="main-title">🔮 Oráculo</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #70757A; margin-bottom: 2rem;'>Busca de Arquivos</p>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    busca = st.text_input("Busca", placeholder="O que deseja encontrar?", label_visibility="collapsed")
