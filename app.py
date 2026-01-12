import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Configurações Iniciais
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

if 'historico' not in st.session_state:
    st.session_state.historico = []

# 2. Estilos CSS
st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; }
    .result-card { background: white; padding: 15px; border-radius: 10px; margin-bottom: 10px; border: 1px solid #EEE; display: flex; justify-content: space-between; align-items: center; }
    .btn-vis { background-color: #4285F4; color: white !important; text-decoration: none !important; padding: 6px 15px; border-radius: 6px; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# 3. Conexão Segura com Google Drive
@st.cache_resource
def get_service():
    try:
        if "google_auth" in st.secrets:
            info = st.secrets["google_auth"]
            sc = ['https://www.googleapis.com/auth/drive.readonly']
            creds = service_account.Credentials.from_service_account_info(info, scopes=sc)
            return build('drive', 'v3', credentials=creds)
    except: return None
    return None

service = get_service()

# 4. Interface Principal
st.markdown("<h1 style='text-align: center;'>🔮 O Oráculo</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    busca = st.text_input("Busca", placeholder="O que deseja encontrar?", label_visibility="collapsed")
    
    # Histórico de Pesquisa
    if st.session_state.historico:
        st.write("")
        cols = st.columns(len(st.session_state.historico) + 1)
        for i, termo in enumerate(st.session_state.historico):
            if cols[i].button(termo, key=f"h_{i}"):
                busca = termo
        # Botão para limpar histórico
        if cols[-1].button("🗑️"):
            st.session_state.historico = []
            st.rerun()

# 5. Lógica do Histórico (CORRIGIDA)
if busca:
    if busca
