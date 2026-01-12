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

# Campo de busca
busca = st.text_input("O que você deseja encontrar?", key="input_busca")

# 4. Lógica do Histórico (Gerenciar as 5 últimas)
if busca:
    # Adiciona ao histórico se for uma busca nova
    if busca not in st.session_state.historico:
        st.session_state.historico.insert(0, busca)
        # Mantém apenas os 5 últimos
        st.session_state.historico = st.session_state.historico[:5]

# Exibir botões do histórico
if st.session_state.historico:
    st.write("🕒 **Buscas recentes:**")
    # Cria colunas para os botões do histórico
    cols = st.columns(len(st.session_state.historico))
    for i, termo in enumerate(st.session_state.historico):
        if cols[i].button(termo, key=f"btn_hist_{i}"):
            # Ao clicar, o Streamlit recarrega e podemos usar esse valor
            st.info(f"Refazendo busca por: {termo}")
            busca = termo

st.divider()

# 5. Resultados da Busca
if busca and service:
    try:
        query = f"name contains '{busca}' and mimeType != 'application/vnd.google-apps.folder' and trashed = false"
        res = service.files().list(q=query, fields="files(id, name, webViewLink)").execute()
        arquivos = res.
