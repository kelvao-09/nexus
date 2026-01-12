import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="Oráculo Pro", page_icon="🔮", layout="wide")

# 1. INICIALIZAR ESTRUTURA DE PASTAS (Memória da Sessão)
if 'pastas_fav' not in st.session_state:
    # Estrutura inicial: Geral e uma lista de nomes de pastas
    st.session_state.pastas_fav = {"Geral": []}

# 2. ESTILO CSS
st.markdown("""
<style>
    .fav-item {
        background: #ffffff;
        padding: 8px;
        border-radius: 5px;
        margin-bottom: 5px;
        border-left: 3px solid #FFD700;
        font-size: 13px;
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

# 3. AUTENTICAÇÃO DRIVE
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

# 4. SIDEBAR: ORGANIZAÇÃO EM PASTAS
with st.sidebar:
    st.header("📂 Pastas de Favoritos")
    
    # Criar Nova Pasta
    nova_pasta = st.text_input("Nome da nova pasta:")
    if st.button("Criar Pasta") and nova_pasta:
        if nova_pasta not in st.session_state.pastas_fav:
            st.session_state.pastas_fav[nova_pasta] = []
            st.rerun()

    st.divider()

    # Exibição das Pastas e Conteúdo
    for pasta, itens in st.session_state.pastas_fav.items():
        with st.expander(f"📁 {pasta} ({len(itens)})"):
            if not itens:
                st.write("Vazia")
            for item in itens:
                st.markdown(f'<div class="fav-item"><b>{item["name"]}</b><br><a href="{item["link"]}" target="_blank">Abrir ↗️</a></div>', unsafe_allow_html=True)
            
            if st.button(f"Esvaziar {pasta}", key=f"clear_{pasta}"):
                st.session_state.pastas_fav[pasta] = []
                st.rerun()

# 5. BUSCA E RESULTADOS
st.title("🔮 Oráculo")
c1, c2, c3 = st.columns([1,2,1])
with c2:
    busca = st.text_input("Pesquisar documento:", placeholder="Ex: Manual...")

if busca and service:
    try:
        q = f"name contains '{busca}' and mimeType != 'application/vnd.google-apps.folder' and trashed = false"
        res = service.files().list(q=q, fields="files(id, name, webViewLink, mimeType)").execute()
        files = res.get
