import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="Oráculo", page_icon="🔮")

# --- COLOQUE O ID DA SUA PASTA AQUI ---
ID_PASTA_RAIZ = "SEU_ID_AQUI" 

@st.cache_resource
def get_drive_service():
    # Carrega as credenciais dos Secrets
    creds_info = st.secrets["google_auth"]
    creds = service_account.Credentials.from_service_account_info(
        creds_info, scopes=['https://www.googleapis.com/auth/drive.readonly']
    )
    return build('drive', 'v3', credentials=creds)

service = get_drive_service()

st.title("🔮 Oráculo")
busca = st.text_input("Qual o problema ou documento?", placeholder="Ex: lentidão")

if busca and service:
    # A query busca em qualquer lugar do Drive que a conta tenha acesso
    # Se quiser restringir a uma pasta, mantenha o ID_PASTA_RAIZ
    query = f"name contains '{busca}' and trashed = false"
    
    results = service.files().list(
        q=query,
        fields="files(id, name, webViewLink, mimeType)"
    ).execute()
    
    arquivos = results.get('files', [])

    if arquivos:
        for arq in arquivos:
            with st.container():
                st.markdown(f"### 📄 {arq['name']}")
                # Link para abrir diretamente
                st.markdown(f'<a href="{arq["webViewLink"]}" target="_blank">Clique aqui para abrir o documento</a>', unsafe_allow_html=True)
                st.divider()
    else:
        st.warning("Nada encontrado.")
