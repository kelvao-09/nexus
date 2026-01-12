import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="Oráculo", page_icon="🔮")

# O TEU ID CONFIGURADO
ID_PASTA_RAIZ = "1_NSyolW53RP-vys0rz3s78LchlfmI7eq" 

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
busca = st.text_input("O que deseja consultar?", placeholder="Ex: Manual de Redes")

if busca and service:
    try:
        # QUERY MELHORADA: 
        # 1. Procura pelo nome
        # 2. Garante que NÃO é uma pasta (mimeType != 'application/vnd.google-apps.folder')
        # 3. Garante que está dentro da sua pasta raiz
        query = (f"name contains '{busca}' and "
                 f"'{ID_PASTA_RAIZ}' in parents and "
                 f"mimeType != 'application/vnd.google-apps.folder' and "
                 f"trashed = false")
        
        results = service.files().list(
            q=query,
            fields="files(id, name, webViewLink, mimeType)",
            pageSize=10
        ).execute()
        
        arquivos = results.get('files', [])

    if arquivos:
        st.write(f"### ✅ Documentos encontrados:")
        for arq in arquivos:
            # Criar um layout limpo para o resultado
            with st.expander(f"📄 {arq['name']}", expanded=True):
                # O webViewLink é o link oficial para abrir o visualizador do Google
                url = arq['webViewLink']
                
                # Botão HTML personalizado para garantir a abertura em nova aba
                st.markdown(f"""
                    <a href="{url}" target="_blank" style="text-decoration: none;">
                        <div style="
                            background-color: #4285F4;
                            color: white;
                            padding: 10px;
                            text-align: center;
                            border-radius: 5px;
                            font-weight: bold;
                            cursor: pointer;
                        ">
                            Visualizar Documento Agora ↗️
                        </div>
                    </a>
                """, unsafe_allow_html=True)
    else:
        st.warning("Nenhum documento específico encontrado com esse nome.")
            
    except Exception as e:
        st.error(f"Erro na busca: {e}")

else:
    st.info("Digite um termo para pesquisar.")
