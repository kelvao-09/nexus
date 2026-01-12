import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Configuração da Página
st.set_page_config(page_title="Oráculo Pro", page_icon="🔮", layout="wide")

# Inicializar estrutura de pastas
if 'pastas_fav' not in st.session_state:
    st.session_state.pastas_fav = {"Geral": []}

# 2. Estilo CSS para máxima sofisticação
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    
    /* Card de Favorito na Sidebar */
    .fav-item {
        background: #ffffff;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 8px;
        border-left: 4px solid #4285F4;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
    }
    
    /* Título das Pastas */
    .folder-label {
        font-weight: bold;
        font-size: 16px;
        color: #333;
    }

    /* Botão de Visualizar na pesquisa */
    .btn-open {
        background-color: #4285F4;
        color: white !important;
        padding: 8px 15px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: bold;
        font-size: 13px;
        display: inline-block;
        text-align: center;
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

# 4. Barra Lateral: Gerenciamento de Pastas (Onde estão os ⋮)
with st.sidebar:
    st.markdown("# 📂 Pastas")
    
    # Criar nova pasta de
