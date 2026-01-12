import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Configuração Principal
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

# Inicializar histórico
if 'historico' not in st.session_state:
    st.session_state.historico = []

# 2. Estilos CSS (Corrigido e Fechado)
st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; }
    .main-title {
        text-align: center; font-weight: 300;
        font-size: 3.5rem; color: #1A1A1B; margin-bottom: 5px;
    }
    .stTextInput input {
        border-radius: 30px !important; padding: 12px 25px !important;
        border: 1px solid #E0E0E0 !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03) !important;
    }
    div.stButton > button {
        border-radius: 20px !important; background-color: #E8EAED !important;
        color: #5F6368 !important; border: none !important;
        padding: 4px 15px !important; font-size: 0.85rem !important;
    }
    div.stButton > button:hover {
        background-color: #4285F4 !important; color: white !important;
    }
    .result-card {
        background: white; padding: 1.2rem; border-radius: 12px;
        margin-bottom: 1rem; border: 1px solid #EEE;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        display: flex; justify-content: space-between; align-items: center;
    }
    .btn-visualizar {
        background-color: #4285F4; color: white !important;
        text-decoration: none !important; padding: 8px 20px;
        border-radius: 6px; font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# 3. Autenticação Drive
@st.cache_resource
def get_drive_service():
    try:
        if "google_auth" in st.secrets:
            info = st.secrets["google_auth"]
            sc = ['https://www.googleapis.com/auth/drive.readonly']
            creds = service_account.Credentials.from_service_account_info(info, scopes=sc)
            return build('drive', 'v3', credentials=creds)
    except: return None
    return None

service = get_drive_service()

# 4. Título e Barra de Pesquisa
st.markdown('<h1 class="main-title">🔮 Oráculo</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #70757A; margin-bottom: 2rem;'>Busca Inteligente</p>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    busca = st.text_input("Busca", placeholder="O que deseja encontrar?", label_visibility="collapsed")
    
    # Histórico de Pesquisa e Botão Limpar
    if st.session_state.historico:
        st.write("")
        n_tags = len(st.session_state.historico)
        # Colunas para tags + lixeira
        cols = st.columns([1] * n_tags + [0.4])
        
        for i, termo in enumerate(st.session_state.historico):
            if cols[i].button(termo, key=f"h_{i}"):
                busca = termo
        
        # Botão Limpar Sofisticado
        if cols[-1].button("🗑️", help="Limpar histórico"):
            st.session_state.historico = []
            st.rerun()

# Lógica do Histórico
if busca and busca not in st.session_state.historico:
    st.session_state.historico.insert(0, busca)
    st.session_state.historico = st.session_state.historico[:5]

st.markdown("<br>", unsafe_allow_html=True)

# 5. Resultados
if busca and service:
    try:
        q = f"name contains '{busca}' and trashed = false"
        res = service.files().list(q=q, fields="files(id, name, webViewLink)").execute()
        arquivos = res.get('files', [])

        if arquivos:
            for arq in arquivos:
                st.markdown(f"""
                <div class="result-card">
                    <div>
                        <div style="color: #1A73E8; font-weight: 500; font-size: 1.1rem;">📄 {arq['name']}</div>
                        <div style="color: #70757A; font-size: 0.85rem;">Google Drive</div>
                    </div>
                    <a href="{arq['webViewLink']}" target="_blank" class="btn-visualizar">Abrir</a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Nenhum arquivo encontrado.")
    except Exception:
        st.error("Erro na comunicação com o Drive.")
