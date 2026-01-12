import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Configuração da Página e Estilo CSS
st.set_page_config(page_title="Oráculo Pro", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .doc-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        transition: 0.3s;
    }
    .doc-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-left: 5px solid #4285F4;
    }
    .doc-info {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .btn-open {
        background-color: #4285F4;
        color: white !important;
        padding: 10px 20px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Autenticação
@st.cache_resource
def get_drive_service():
    try:
        creds_info = st.secrets["google_auth"]
        creds = service_account.Credentials.from_service_account_info(
            creds_info, scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        st.error("Erro de Autenticação. Verifique os Secrets.")
        return None

service = get_drive_service()

# 3. Cabeçalho
st.markdown("<h1 style='text-align: center;'>🔮 O Oráculo</h1>", unsafe_allow_html=True)
col_search_1, col_search_2, col_search_3 = st.columns([1,2,1])
with col_search_2:
    busca = st.text_input("", placeholder="Digite sua pesquisa aqui...")

# 4. Resultados
if busca and service:
    try:
        query = f"name contains '{busca}' and mimeType != 'application/vnd.google-apps.folder' and trashed = false"
        results = service.files().list(q=query, fields="files(id, name, webViewLink, mimeType)").execute()
        arquivos = results.get('files', [])

        if arquivos:
            for arq in arquivos:
                # Ícones por tipo
                m = arq['mimeType']
                icon = "📕" if 'pdf' in m else "📗" if 'sheet' in m else "📘" if 'document' in m else "📄"
                
                st.markdown(f"""
                    <div class="doc-card">
                        <div class="doc-info">
                            <span style="font-size: 2rem;">{icon}</span>
                            <div>
                                <h4 style="margin:0;">{arq['name']}</h4>
                                <small style="color: gray;">Documento do Google Drive</small>
                            </div>
                        </div>
                        <a href="{arq['webViewLink']}" target="_blank" class="btn-open">Abrir</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Nenhum documento encontrado.")
    except Exception as e:
        st.error(f"Erro na consulta: {e}")
