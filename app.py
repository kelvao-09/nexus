import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Configuração da Página
st.set_page_config(page_title="Oráculo", page_icon="🔮")

# Inicializar o histórico na memória da sessão
if 'historico' not in st.session_state:
    st.session_state.historico = []

# 2. Autenticação Drive
@st.cache_resource
def get_drive_service():
    try:
        if "google_auth" in st.secrets:
            creds_info = st.secrets["google_auth"]
            creds = service_account.Credentials.from_service_account_info(
                creds_info, scopes=['https://www.googleapis.com/auth/drive.readonly']
            )
            return build('drive', 'v3', credentials=creds)
    except:
        return None
    return None

service = get_drive_service()

# 3. Interface Principal
st.markdown("<h1 style='text-align: center;'>🔮 O Oráculo</h1>", unsafe_allow_html=True)

# Campo de busca (Aba de pesquisa)
busca = st.text_input("O que você deseja encontrar?", key="main_search")

# 4. Lógica do Histórico (5 últimas)
if busca:
    if busca not in st.session_state.historico:
        st.session_state.historico.insert(0, busca)
        st.session_state.historico = st.session_state.historico[:5]

# Exibir histórico como botões clicáveis
if st.session_state.historico:
    st.write("🕒 **Buscas recentes:**")
    cols = st.columns(len(st.session_state.historico))
    for i, termo in enumerate(st.session_state.historico):
        if cols[i].button(termo, key=f"h_{i}"):
            # Ao clicar, fazemos a busca por esse termo
            busca = termo

st.divider()

# 5. Resultados da Busca
if busca and service:
    try:
        query = f"name contains '{busca}' and mimeType != 'application/vnd.google-apps.folder' and trashed = false"
        res = service.files().list(q=query, fields="files(id, name, webViewLink)").execute()
        arquivos = res.get('files', [])

        if arquivos:
            st.write(f"### Resultados para: {busca}")
            for arq in arquivos:
                col_arq, col_link = st.columns
