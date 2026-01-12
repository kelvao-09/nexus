import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Oráculo Pro", page_icon="🔮", layout="wide")

# Inicializar estrutura de pastas na memória da sessão
if 'pastas_fav' not in st.session_state:
    st.session_state.pastas_fav = {"Geral": []}

# 2. ESTILO CSS (Sofisticação e Cards)
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .fav-item {
        background: white;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 8px;
        border-left: 4px solid #4285F4;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
    }
    .btn-open {
        background-color: #4285F4;
        color: white !important;
        padding: 8px 15px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        text-align: center;
    }
    /* Estilo para o menu de 3 pontinhos */
    .stPopover button {
        border: none !important;
        background: transparent !important;
        font-size: 20px !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. AUTENTICAÇÃO DRIVE
@st.cache_resource
def get_drive_service():
    try:
        creds_info = st.secrets["google_auth"]
        creds = service_account.Credentials.from_service_account_info(
            creds_info, scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        return build('drive', 'v3', credentials=creds)
    except:
        return None

service = get_drive_service()

# 4. BARRA LATERAL (Pastas com Menu ⋮)
with st.sidebar:
    st.title
