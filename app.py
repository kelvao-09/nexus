import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

if 'historico' not in st.session_state:
    st.session_state.historico = []

# --- CSS ---
st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; }
    .result-card { background: white; padding: 15px; border-radius: 10px; margin-bottom: 10px; border: 1px solid #EEE; display: flex; justify-content: space-between; align-items: center; }
    .btn-vis { background-color: #4285F4; color: white !important; text-decoration: none !important; padding: 6px 15px; border-radius: 6px; }
</style>
""", unsafe_allow_html=True)

# --- Autenticação ---
@st.cache_resource
def get_service():
    try:
        if "google_auth" in st.secrets:
            info = st.secrets["google_auth"]
            # Escopo de leitura
            scope = ['https://www.googleapis.com/auth/drive.readonly']
            creds = service_account.Credentials.from_service_account_info(info, scopes=scope)
            return build('drive', 'v3', credentials=creds)
        else:
            st.error("ERRO: 'google_auth' não encontrado nos Secrets do Streamlit.")
            return None
    except Exception as e:
        st.error(f"ERRO DE AUTENTICAÇÃO: {e}")
        return None

service = get_service()

# --- Interface ---
st.markdown("<h1 style='text-align: center;'>🔮 Oráculo</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    busca = st.text_input("Busca", placeholder="Digite o nome do ficheiro...", label_visibility="collapsed")
    
    if st.session_state.historico:
        cols = st.columns(len(st.session_state.historico) + 1)
        for i, termo in enumerate(st.session_state.historico):
            if cols[i].button(termo, key=f"h_{i}"):
                busca = termo
        if cols[-1].button("🗑️"):
            st.session_state.historico = []
            st.rerun()

if busca and busca not in st.session_state.historico:
    st.session_state.historico.insert(0, busca)
    st.session_state.historico = st.session_state.historico[:5]

# --- Busca ---
if busca:
    if service:
        try:
            # Query ajustada para ser mais abrangente na busca de nomes
            q = f"name contains '{busca}' and mimeType != 'application/vnd.google-apps.folder' and trashed = false"
            
            # Chamada ao Drive
            results = service.files().list(
                q=q, 
                fields="files(id, name, webViewLink)",
