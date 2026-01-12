import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# CONFIGURAÇÕES DE PÁGINA
st.set_page_config(page_title="Oráculo Drive", page_icon="🔮", layout="centered")

# --- O TEU ID CONFIGURADO ---
ID_PASTA_RAIZ = "1_NSyolW53RP-vys0rz3s78LchlfmI7eq" 

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
        st.error(f"Erro ao carregar credenciais: {e}")
        return None

service = get_drive_service()

# --- INTERFACE ---
st.title("🔮 Oráculo de Documentos")
st.write("Pesquise por manuais, planilhas ou procedimentos no Google Drive.")

busca = st.text_input("", placeholder="Digite o que procura (ex: lentidão)...")

if busca and service:
    try:
        # Query: Procura ficheiros que contenham o nome digitado 
        # e que estejam dentro da pasta raiz ou das suas subpastas
        query = f"name contains '{busca}' and '{ID_PASTA_RAIZ}' in parents and trashed = false"
        
        # Caso queiras pesquisar em TODAS as subpastas de forma profunda, 
        # usa esta query alternativa: query = f"name contains '{busca}' and trashed = false"
        
        results = service.files().list(
            q=query,
            fields="files(id, name, webViewLink, mimeType)",
            spaces='drive'
        ).execute()
        
        arquivos = results.get('files', [])

        if arquivos:
            st.markdown(f"### ✅ Encontrei {len(arquivos)} resultado(s):")
            for arq in arquivos:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{arq['name']}**")
                    with col2:
                        # Link que abre direto no visualizador do Google (Docs, Sheets, PDF)
                        st.markdown(f'''
                            <a href="{arq['webViewLink']}" target="_blank" style="text-decoration: none;">
                                <button style="
                                    background-color: #4285F4;
                                    color: white;
                                    border: none;
                                    padding: 6px 16px;
                                    border-radius: 5px;
                                    cursor: pointer;
                                    font-weight: bold;">
                                    Abrir ↗️
                                </button>
                            </a>
                        ''', unsafe_allow_html=True)
                    st.divider()
        else:
            st.warning("Nenhum documento encontrado com esse nome nesta pasta.")
            
    except Exception as e:
        if "404" in str(e):
            st.error("Erro 404: O Google não encontrou a pasta. Verifica se o ID está correto e se partilhaste a pasta com o e-mail da Service Account.")
        else:
            st.error(f"Erro na busca: {e}")

elif not service:
    st.info("A aguardar ligação com o Google Drive...")
else:
    st.info("Digite uma palavra-chave para começar a pesquisa.")
