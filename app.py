import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# CONFIGURAÇÕES DE PÁGINA
st.set_page_config(page_title="Oráculo Drive", page_icon="🔮", layout="centered")

# --- COLOQUE O ID DA SUA PASTA AQUI ---
# Exemplo: se a URL é drive.google.com/drive/folders/1abc123... o ID é 1abc123...
ID_PASTA_RAIZ = "SEU_ID_DA_PASTA_AQUI" 

@st.cache_resource
def get_drive_service():
    try:
        # Puxa os dados dos Secrets (que você já configurou)
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
st.write("Pesquise por manuais, planilhas ou procedimentos.")

busca = st.text_input("", placeholder="Digite o que você procura (ex: lentidão)...")

if busca and service:
    # Query que busca o nome e garante que o arquivo pertence à sua pasta raiz
    # e não está na lixeira
    query = f"name contains '{busca}' and '{ID_PASTA_RAIZ}' in parents and trashed = false"
    
    try:
        results = service.files().list(
            q=query,
            fields="files(id, name, webViewLink, mimeType)"
        ).execute()
        
        arquivos = results.get('files', [])

        if arquivos:
            st.markdown(f"### ✅ Encontrei {len(arquivos)} documento(s):")
            for arq in arquivos:
                # Layout elegante para cada resultado
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{arq['name']}**")
                    with col2:
                        # Link que abre direto no visualizador do Google
                        st.markdown(f'''
                            <a href="{arq['webViewLink']}" target="_blank" style="text-decoration: none;">
                                <button style="
                                    background-color: #4285F4;
                                    color: white;
                                    border: none;
                                    padding: 5px 15px;
                                    border-radius: 5px;
                                    cursor: pointer;">
                                    Abrir
                                </button>
                            </a>
                        ''', unsafe_allow_html=True)
                    st.divider()
        else:
            st.warning("Nenhum documento encontrado com esse nome.")
            
    except Exception as e:
        st.error(f"Erro na busca: {e}")

elif not service:
    st.info("Configurando conexão com o Google Drive...")
else:
    st.info("O Oráculo está pronto para sua pergunta.")
