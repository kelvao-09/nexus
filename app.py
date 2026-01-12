import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Configuração da Página
st.set_page_config(page_title="Oráculo Pro", page_icon="🔮", layout="wide")

# Inicializar estrutura de pastas se não existir
if 'pastas_fav' not in st.session_state:
    st.session_state.pastas_fav = {"Geral": []}

# 2. Estilo CSS para Cards
st.markdown("""
<style>
    .fav-item {
        background: #ffffff;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 8px;
        border-left: 4px solid #FFD700;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .btn-open {
        background-color: #4285F4;
        color: white !important;
        padding: 6px 12px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# 3. Autenticação Drive
@st.cache_resource
def get_drive_service():
    try:
        creds_info = st.secrets["google_auth"]
        creds = service_account.Credentials.from_service_account_info(
            creds_info, scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        return build('drive', 'v3', credentials=creds)
    except Exception:
        return None

service = get_drive_service()

# 4. Sidebar: Gerenciamento de Pastas
with st.sidebar:
    st.header("📂 Pastas de Favoritos")
    
    # Criar nova pasta
    with st.form("nova_pasta_form", clear_on_submit=True):
        nome_n_pasta = st.text_input("Nome da pasta:")
        if st.form_submit_button("Criar"):
            if nome_n_pasta and nome_n_pasta not in st.session_state.pastas_fav:
                st.session_state.pastas_fav[nome_n_pasta] = []
                st.rerun()

    st.divider()

    # Exibir pastas e conteúdos (Indentação corrigida aqui)
    for pasta, itens in st.session_state.pastas_fav.items():
        with st.expander(f"📁 {pasta} ({len(itens)})"):
            if not itens:
                st.write("Pasta vazia")
            else:
                for item in itens:
                    st.markdown(f"""
                        <div class="fav-item">
                            <b>{item['name']}</b><br>
                            <a href="{item['link']}" target="_blank" style="font-size:11px; color:#4285F4;">Abrir ↗️</a>
                        </div>
                    """, unsafe_allow_html=True)
            
            if st.button(f"Limpar {pasta}", key=f"clear_{pasta}"):
                st.session_state.pastas_fav[pasta] = []
                st.rerun()

# 5. Interface Principal
st.markdown("<h1 style='text-align: center;'>🔮 O Oráculo</h1>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1,2,1])
with c2:
    busca = st.text_input("", placeholder="Pesquise seu documento...")

if busca and service:
    try:
        query = f"name contains '{busca}' and mimeType != 'application/vnd.google-apps.folder' and trashed = false"
        res = service.files().list(q=query, fields="files(id, name, webViewLink, mimeType)").execute()
        files = res.get('files', [])

        if files:
            for i, f in enumerate(files):
                with st.container():
                    col_info, col_fav = st.columns([3, 2])
                    with col_info:
                        st.markdown(f"#### 📄 {f['name']}")
                        st.markdown(f'<a href="{f["webViewLink"]}" target="_blank" class="btn-open">Abrir</a>', unsafe_allow_html=True)
                    
                    with col_fav:
                        pasta_sel = st.selectbox("Salvar em:", list(st.session_state.pastas_fav.keys()), key=f"sel_{i}")
                        if st.button(f"⭐ Adicionar", key=f"btn_{i}"):
                            st.session_state.pastas_fav[pasta_sel].append({
                                'id': f['id'], 'name': f['name'], 'link': f['webViewLink']
                            })
                            st.toast(f"Salvo em {pasta_sel}!")
                            st.rerun()
                    st.divider()
        else:
            st.warning("Nada encontrado.")
    except Exception as e:
        st.error(f"Erro: {e}")
