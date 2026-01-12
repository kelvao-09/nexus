import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Configuração da Página
st.set_page_config(page_title="Oráculo Pro", page_icon="🔮", layout="wide")

# Inicializar estrutura de pastas
if 'pastas_fav' not in st.session_state:
    st.session_state.pastas_fav = {"Geral": []}

# 2. Estilo CSS
st.markdown("""
<style>
    .fav-item {
        background: #ffffff;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 5px;
        border-left: 4px solid #FFD700;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .folder-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
    }
    .btn-open {
        background-color: #4285F4;
        color: white !important;
        padding: 5px 10px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Autenticação Drive
@st.cache_resource
def get_drive_service():
    try:
        creds_info = st.secrets["google_auth"]
        creds = service_account.Credentials.from_service_account_info(
            creds_info, scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        return build('drive', 'v3', credentials=creds)
    except: return None

service = get_drive_service()

# 4. Barra Lateral: Gerenciamento com "Três Pontinhos"
with st.sidebar:
    st.header("📂 Suas Pastas")
    
    # Criar nova pasta
    with st.popover("➕ Nova Pasta"):
        nome_n = st.text_input("Nome da pasta:")
        if st.button("Criar"):
            if nome_n and nome_n not in st.session_state.pastas_fav:
                st.session_state.pastas_fav[nome_n] = []
                st.rerun()

    st.divider()

    # Listagem de Pastas
    for pasta in list(st.session_state.pastas_fav.keys()):
        col_folder, col_menu = st.columns([5, 1])
        
        with col_folder:
            # O expander agora serve apenas para ver os arquivos
            exp = st.expander(f"📁 {pasta}")
        
        with col_menu:
            # O "Menu de Três Pontinhos" usando Popover
            with st.popover("⋮"):
                st.markdown(f"**Editar: {pasta}**")
