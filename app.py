import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Configuração e Estilo
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

if 'hist' not in st.session_state:
    st.session_state.hist = []

# CSS Compacto com Animação
st.markdown("""
<style>
    @keyframes move { 0%, 100% {transform: translateY(0);} 50% {transform: translateY(-15px);} }
    .floating { font-size: 70px; text-align: center; animation: move 3s infinite; }
    .card { background: white; padding: 12px; border-radius: 8px; border: 1px solid #EEE; margin-bottom: 8px; }
</style>
""", unsafe_allow_html=True)

# 2. Conexão Drive
@st.cache_resource
def get_svc():
    try:
        if "google_auth" in st.secrets:
            sec = st.secrets["google_auth"]
            sco = ['https://www.googleapis.com/auth/drive.readonly']
            creds = service_account.Credentials.from_service_account_info(sec, scopes=sco)
            return build('drive', 'v3', credentials=creds)
    except: return None
    return None

svc = get_svc()

# 3. Interface
st.markdown('<div class="floating">🔮</div>', unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>O Oráculo</h2>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    busca = st.text_input("S", placeholder="O que busca?", label_visibility="collapsed")
    
    # Histórico Simplificado
    if st.session_state.hist:
        h_cols = st.columns(len(st.session_state.hist) + 1)
        for i, t in enumerate(st.session_state.hist):
            if h_cols[i].button(t, key=f"h{i}"): busca = t
        if h_cols[-1].button("🗑️"):
            st.session_state.hist = []
            st.rerun()

# Lógica de Dados
if busca and busca not in st.session_state.hist:
    st.session_state.hist.insert(0, busca)
    st.session_state.hist = st.session_state.hist[:5]

# 4. Resultados (Apenas Arquivos)
if busca and svc:
    try:
        # Filtro: Nome contém texto E não é pasta
        q = f"name contains '{busca}' and mimeType != 'application/vnd.google-apps.folder' and trashed = false"
        res =
