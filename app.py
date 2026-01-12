import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="Oráculo Total", page_icon="🔮", layout="wide")

@st.cache_resource
def get_drive_service():
    try:
        creds_info = st.secrets["google_auth"]
        creds = service_account.Credentials.from_service_account_info(
            creds_info, 
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        st.error(f"Erro de Autenticação: {e}")
        return None

service = get_drive_service()

st.title("🔮 Oráculo Inteligente")
st.write("Digite qualquer parte do nome do arquivo (ex: 'jogo', 'rede', 'analise')")

# Campo de pesquisa
busca = st.text_input("O que você procura?", placeholder="Digite aqui...")

if busca and service:
    try:
        # Removi a restrição de pasta 'parents' para que ele vasculhe TUDO 
        # o que você compartilhou com o e-mail da Service Account.
        # O 'contains' garante que ache "jogo" dentro de "análise de jogos".
        query = f"name contains '{busca}' and mimeType != 'application/vnd.google-apps.folder' and trashed = false"
        
        results = service.files().list(
            q=query,
            fields="files(id, name, webViewLink, mimeType)",
            pageSize=20 # Aumentei para mostrar mais resultados de uma vez
        ).execute()
        
        arquivos = results.get('files', [])

        if arquivos:
            st.success(f"Encontrei {len(arquivos)} documento(s) relacionado(s) a '{busca}':")
            
            # Criando uma grade de resultados
            for arq in arquivos:
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        # Mostra o nome completo
