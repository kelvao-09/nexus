import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="Oráculo", page_icon="🔮")

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

st.title("🔮 Oráculo")
busca = st.text_input("O que deseja consultar?", placeholder="Ex: Manual")

if busca and service:
    try:
        # Removi a trava de 'parents' para testar o acesso total
        query = f"name contains '{busca}' and mimeType != 'application/vnd.google-apps.folder' and trashed = false"
        
        results = service.files().list(
            q=query,
            fields="files(id, name, webViewLink)",
            pageSize=10
        ).execute()
        
        arquivos = results.get('files', [])

        if arquivos:
            st.write(f"### ✅ Documentos encontrados:")
            for arq in arquivos:
                st.markdown(f"""
                    <div style="border:1px solid #ddd; padding:15px; border-radius:10px; margin-bottom:10px; background-color:#f9f9f9">
                        <p style='margin:0'><strong>{arq['name']}</strong></p>
                        <a href="{arq['webViewLink']}" target="_blank" style="color: #4285F4; text-decoration: none; font-weight: bold;">
                            Abrir Documento Agora ↗️
                        </a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("O Oráculo não encontrou nenhum arquivo com esse nome. Verifique se o arquivo foi compartilhado com o e-mail da API.")
            
    except Exception as e:
        st.error(f"Erro na busca: {e}")
