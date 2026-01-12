import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configuração da Página
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

# Inicialização de variáveis
if 'historico' not in st.session_state:
    st.session_state.historico = []

# CSS Compacto (Garante o visual sem quebrar o código)
st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; }
    .main-title { text-align: center; font-weight: 300; font-size: 3rem; color: #1A1A1B; }
    .stTextInput input { border-radius: 20px !important; }
    .result-card { background: white; padding: 15px; border-radius: 10px; margin-bottom: 10px; border: 1px solid #EEE; display: flex; justify-content: space-between; align-items: center; }
    .btn-visualizar { background-color: #4285F4; color: white !important; text-decoration: none !important; padding: 5px 15px; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# Autenticação Google Drive
@st.cache_resource
def get_service():
    try:
        if "google_auth" in st.secrets:
            creds = service_account.Credentials.from_service_account_info(
                st.secrets["google_auth"], 
                scopes=['https://www.googleapis.com/auth/drive.readonly']
            )
            return build('drive', 'v3', credentials=creds)
    except: return None
    return None

service = get_service()

# Interface Principal
st.markdown('<h1 class="main-title">🔮 Oráculo</h1>', unsafe_allow_html=True)

# Campo de Busca
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    busca = st.text_input("O que deseja encontrar?", placeholder="Digite aqui...", label_visibility="collapsed")
    
    # Histórico e Limpar
    if st.session_state.historico:
        cols = st.columns(len(st.session_state.historico) + 1)
        for i, termo in enumerate(st.session_state.historico):
            if cols[i].button(termo, key=f"h_{i}"):
                busca = termo
        if cols[-1].button("🗑️"):
            st.session_state.historico = []
            st.rerun()

# Atualiza Histórico
if busca and busca not in st.session_state.historico:
    st.session_state.historico.insert(0, busca)
    st.session_state.historico = st.session_state.historico[:5]

# Resultados (FILTRADOS: Apenas arquivos, sem pastas)
if busca and service:
    try:
        q = f"name contains '{busca}' and mimeType != 'application/vnd.google-apps.folder' and trashed = false"
        res = service.files().list(q=
