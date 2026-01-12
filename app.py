import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Configuração da Página
st.set_page_config(page_title="Oráculo Pro", page_icon="🔮", layout="wide")

# Inicializar estrutura de pastas nos favoritos se não existir
if 'pastas_fav' not in st.session_state:
    st.session_state.pastas_fav = {"Geral": []}

# 2. Estilo CSS para Cards e Favoritos
st.markdown("""
<style>
    .fav-item {
        background: #ffffff;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 8px;
        border-left: 4px solid #FFD700;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .btn-open {
        background-color: #4285F4;
        color: white !important;
        padding: 6px 12px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        font-size: 13px;
        display: inline-block;
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
    except Exception:
        return None

service = get_drive_service()

# 4. Sidebar: Gerenciamento de Pastas
with st.sidebar:
    st.header("📂 Minhas Pastas")
    
    # Criar nova pasta
    with st.form("nova_pasta_form", clear_on_submit=True):
        nome_n_pasta = st.text_input("Nova pasta:")
        if st.form_submit_button("Criar"):
            if nome_n_pasta and nome_n_pasta not in st.session_state.pastas_fav:
                st.session_state.pastas_fav[nome_n_pasta] = []
                st.rerun()

    st.divider()

    # Exibir pastas e conteúdos
    for pasta, itens in st.session_state.pastas_fav.items():
        with st.expander(f"📁 {pasta} ({len(itens)})"):
