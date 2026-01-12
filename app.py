import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="Oráculo Inteligente", page_icon="🔮", layout="wide")

@st.cache_resource
def get_drive_service():
    try:
        # Puxa os dados dos Secrets do Streamlit Cloud
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
        # A query 'contains' busca o termo em qualquer parte do nome do arquivo
        query = f"name contains '{busca}' and mimeType != 'application/vnd.google-apps.folder' and trashed = false"
        
        results = service.files().list(
            q=query,
            fields="files(id, name, webViewLink, mimeType)",
            pageSize=20 
        ).execute()
        
        arquivos = results.get('files', [])

        if arquivos:
            st.success(f"Encontrei {len(arquivos)} documento(s) relacionado(s) a '{busca}':")
            
            for arq in arquivos:
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        # Informação do arquivo encontrada
                        st.markdown(f"#### 📄 {arq['name']}")
                    with col2:
                        # Link direto para visualização no navegador
                        url = arq['webViewLink']
                        st.markdown(f"""
                            <a href="{url}" target="_blank" style="text-decoration: none;">
                                <button style="
                                    background-color: #4285F4;
                                    color: white;
                                    border: none;
                                    padding: 10px 20px;
                                    border-radius: 8px;
                                    cursor: pointer;
                                    font-weight: bold;
                                    width: 100%;">
                                    Abrir Documento
                                </button>
                            </a>
                        """, unsafe_allow_html=True)
                    st.divider()
        else:
            st.warning(f"Nenhum documento encontrado contendo '{busca}'.")
            
    except Exception as e:
        st.error(f"Erro ao processar a busca: {e}")
else:
    st.info("💡 Dica: Você não precisa digitar o nome inteiro, apenas uma palavra-chave.")
