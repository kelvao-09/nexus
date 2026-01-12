import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Configuração da Página
st.set_page_config(page_title="Oráculo Pro", page_icon="🔮", layout="wide")

# Inicializar o estado de favoritos na sessão
if 'favoritos' not in st.session_state:
    st.session_state.favoritos = []

# 2. Estética Sofisticada (CSS)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }
    .fav-item {
        background: #fdfdfd;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 4px solid #FFD700;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
    }
    .btn-open {
        background-color: #4285F4;
        color: white !important;
        padding: 8px 18px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        display: inline-block;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Autenticação com Google Drive
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

# 4. Barra Lateral de Favoritos
with st.sidebar:
    st.markdown("## ⭐ Favoritos")
    st.markdown("---")
    if not st.session_state.favoritos:
        st.info("Sua lista está vazia.")
    else:
        for fav in st.session_state.favoritos:
            st.markdown(f"""
                <div class="fav-item">
                    <strong style='font-size:14px;'>{fav['name']}</strong><br>
                    <a href="{fav['link']}" target="_blank" style='font-
