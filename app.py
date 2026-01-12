import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Configuração e Estilo
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

if 'hist' not in st.session_state:
    st.session_state.hist = []

# CSS com Animação de Levitação
st.markdown("""
<style>
    @keyframes levitate {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }
    .stApp { background-color: #F8F9FA; }
    .floating-icon {
        font-size: 80px; text-align: center;
        animation: levitate 3s ease-in-out infinite;
    }
    .card { 
        background: white; padding: 15px; border-radius: 10px; 
        margin-bottom: 10px; border: 1px solid #EEE; 
        display: flex; justify-content: space-between; align-items: center; 
    }
    .btn { 
        background-color: #4285F4; color: white !important; 
        text-decoration: none !important; padding: 6px 15px; 
        border-radius: 6px; font-weight: 500; 
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
st.markdown("<h1 style='text-align: center; margin-top: -20px;'>O Oráculo</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    busca = st.text_input("Busca", placeholder="Pesquisar...", key="main_in", label_visibility="collapsed")
    
    # Histórico clicável
    if st.session_state.hist:
        st.write("")
        h_list = st.session_state.hist
        cols = st.columns(len(h_list) + 1)
        for i, t in enumerate(h_list):
            if cols[i].button(t, key=f"h_{i}"):
                busca = t
        if cols[-1].button("🗑️"):
            st.session_state.hist = []
            st.rerun()

# 4. Lógica do Histórico (Linha encurtada para evitar AttributeError)
if busca and busca not in st.session_state.hist:
    st.session_state.hist.insert(0, busca)
    st.session_state.hist = st.session_state.hist[:5]

# 5. Resultados (Apenas Arquivos)
if busca and svc:
    try:
        q = f"name contains '{busca}' and mimeType != 'application/vnd.google-apps.folder' and trashed = false"
        res = svc.files().list(q=q, fields="files(id, name, webViewLink)").execute()
        files = res.get('files', [])
        
        if files:
            st.markdown("<br>", unsafe_allow_html=True)
            for f in files:
                st.markdown(f"""
                <div class
