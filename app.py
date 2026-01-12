import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Configuração da Página
st.set_page_config(page_title="Oráculo Pro", page_icon="🔮", layout="wide")

# Inicializar favoritos
if 'favoritos' not in st.session_state:
    st.session_state.favoritos = []

# 2. Estilo CSS
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .fav-card {
        background: #ffffff;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 8px;
        border-left: 5px solid #FFD700;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .btn-open {
        background-color: #4285F4;
        color: white !important;
        padding: 8px 15px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
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
    except:
        return None

service = get_drive_service()

# 4. Sidebar de Favoritos
with st.sidebar:
    st.header("⭐ Favoritos")
    if not st.session_state.favoritos:
        st.write("Nenhum favorito salvo.")
    else:
        for fav in st.session_state.favoritos:
            st.markdown(f'<div class="fav-card"><b>{fav["name"]}</b><br><a href="{fav["link"]}" target="_blank" style="font-size:12px; color:#4285F4;">Ver Documento</a></div>', unsafe_allow_html=True)
        if st.button("Limpar Lista"):
            st.session_state.favoritos = []
            st.rerun()

# 5. Busca Principal
st.markdown("<h1 style='text-align: center;'>🔮 O Oráculo</h1>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1,2,1])
with c2:
    busca = st.text_input("", placeholder="O que você precisa encontrar?")

if busca and service:
    try:
        q = f"name contains '{busca}' and mimeType != 'application/vnd.google-apps.folder' and trashed = false"
        res = service.files().list(q=q, fields="files(id, name, webViewLink, mimeType)").execute()
        files = res.get('files', [])

        if files:
            for i, f in enumerate(files):
                # Determinar ícone
                m = f['mimeType']
                icon = "📕" if 'pdf' in m else "📗" if 'sheet' in m else "📘" if 'document' in m else "📄"
                
                with st.container():
                    col_txt, col_fav, col_link = st.columns([6, 1, 1])
                    with col_txt:
                        st.markdown(f"#### {icon} {f['name']}")
                    with col_fav:
                        if st.button("⭐", key=f"f_{i}"):
                            if not any(fav['id'] == f['id'] for fav in st.session_state.favoritos):
                                st.session_state.favoritos.append({'id': f['id'], 'name': f['name'], 'link': f['webViewLink']})
                                st.toast("Salvo nos favoritos!")
                                st.rerun()
                    with col_link:
                        st.markdown(f'<a href="{f["webViewLink"]}" target="_blank" class="btn-open">Abrir</a>', unsafe_allow_html=True)
                    st.divider()
        else:
            st.warning("Nada encontrado.")
    except Exception as e:
        st.error(f"Erro: {e}")
