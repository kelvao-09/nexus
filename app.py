import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Configuração e Estilo
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

if 'hist' not in st.session_state:
    st.session_state.hist = []

# CSS com Animação de Levitação e Estilo dos Cards
st.markdown("""
<style>
    @keyframes levitate {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-12px); }
        100% { transform: translateY(0px); }
    }
    .stApp { background-color: #F8F9FA; }
    .floating-icon {
        font-size: 70px; text-align: center;
        animation: levitate 3s ease-in-out infinite;
        margin-bottom: 10px;
    }
    .card-box {
        background: white; padding: 15px; border-radius: 10px;
        border: 1px solid #EEE; margin-bottom: 10px;
        display: flex; justify-content: space-between; align-items: center;
    }
</style>
""", unsafe_allow_html=True)

# 2. Conexão Drive
@st.cache_resource
def get_svc():
    try:
        if "google_auth" in st.secrets:
            auth = st.secrets["google_auth"]
            creds = service_account.Credentials.from_service_account_info(
                auth, scopes=['https://www.googleapis.com/auth/drive.readonly'])
            return build('drive', 'v3', credentials=creds)
    except: return None
    return None

svc = get_svc()

# 3. Interface Principal
st.markdown('<div class="floating-icon">🔮</div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; margin-top: -15px;'>O Oráculo</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    busca = st.text_input("Busca", placeholder="Pesquisar...", key="main_in", label_visibility="collapsed")
    
    if st.session_state.hist:
        h_list = st.session_state.hist
        cols = st.columns(len(h_list) + 1)
        for i, t in enumerate(h_list):
            if
