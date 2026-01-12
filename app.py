import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Configuração da Página
st.set_page_config(page_title="Oráculo Simples", page_icon="🔮")

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
        pass
    return None

service = get_drive_service()

# 3. Título Principal
st.markdown("<h1 style='text-align: center;'>🔮 O Oráculo</h1>", unsafe_allow_html=True)

# 4. Aba de Pesquisa
# Criamos uma função para atualizar a busca quando clicar no histórico
def pesquisar_termo(termo):
    st.session_state.termo_atual = termo

# Se não houver termo atual, começa vazio
if 'termo_atual' not in st.session_state:
    st.session_state.termo_atual = ""

busca = st.text_input("O que você deseja encontrar?", value=st.session_state.termo_atual)

# 5. Lógica do Histórico (As 5 últimas)
if busca and busca not in st.session_state.historico:
    # Adiciona ao início da lista e mantém apenas as 5 últimas
    st.session_state.historico.insert(0, busca)
    st.session_state.historico = st.session_state.historico[:5]

if st.session_state.historico:
