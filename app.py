import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Oráculo Pro", page_icon="🔮", layout="wide")

# Inicializar estrutura de pastas (Memória da Sessão)
if 'pastas_fav' not in st.session_state:
    st.session_state.pastas_fav = {"Geral": []}

# 2. ESTILO CSS (Sofisticação e Visibilidade)
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .fav-item {
        background: white;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 8px;
        border-left: 4px solid #4285F4;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
    }
    .btn-open {
        background-color: #4285F4;
        color: white !important;
        padding: 8px 15px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# 3. AUTENTICAÇÃO
@st.cache_resource
def get_drive_service():
    try:
        creds_info = st.secrets["google_auth"]
        creds = service_account.Credentials.from_service_account_info(
            creds_info, scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        return build('drive', 'v3', credentials=creds)
    except:
        return None

service = get_drive_service()

# 4. BARRA LATERAL (Pastas e Menu ⋮)
with st.sidebar:
    st.title("📂 Navegação")
    
    with st.popover("➕ Nova Pasta", use_container_width=True):
        n_nome = st.text_input("Nome da pasta:")
        if st.button("Criar"):
            if n_nome and n_nome not in st.session_state.pastas_fav:
                st.session_state.pastas_fav[n_nome] = []
                st.rerun()
    
    st.divider()

    for pasta in list(st.session_state.pastas_fav.keys()):
        col_n, col_m = st.columns([0.8, 0.2])
        
        with col_n:
            exp = st.expander(f"📁 {pasta}")
        
        with col_m:
            with st.popover("⋮"):
                st.write(f"Ações: {pasta}")
                novo_n = st.text_input("Renomear:", value=pasta, key=f"re_{pasta}")
                if st.button("Salvar", key=f"sv_{pasta}"):
                    st.session_state.pastas_fav[novo_n] = st.session_state.pastas_fav.pop(pasta)
                    st.rerun()
                if pasta != "Geral":
                    if st.button("🗑️ Excluir", key=st.secrets.get(f"dl_{pasta}", f"dl_{pasta}")):
                        del st.session_state.pastas_fav[pasta]
                        st.rerun()
        
        with exp:
            itens = st.session_state.pastas_fav[pasta]
            if not itens:
                st.caption("Vazia")
            else:
                for idx, item in enumerate(itens):
                    st.markdown(f'<div class="fav-item"><b>{item["name"]}</b><br><a href="{item["link"]}" target="_blank" style="font-size:11px; color:#4285F4;">Abrir ↗️</a></div>', unsafe_allow_html=True)
                    if st.button("❌", key=f"rm_{pasta}_{idx}"):
                        st.session_state.pastas_fav[pasta].pop(idx)
                        st.rerun()

# 5. INTERFACE PRINCIPAL (Pesquisa centralizada)
st.markdown("<h1 style='text-align: center;'>🔮 O Oráculo</h1>", unsafe_allow_html=True)

# Colunas para centralizar a barra
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    busca = st.text_input("Pesquise no Drive", placeholder="O que você procura hoje?", label_visibility="collapsed")

# 6. RESULTADOS
if busca and service:
    try:
        q = f"name contains '{busca}' and mimeType != 'application/vnd.google-apps.folder' and trashed = false"
        res = service.files().list(q=q, fields="files(id, name, webViewLink)").execute()
        arquivos = res.get('files', [])

        if arquivos:
            for i, f in enumerate(arquivos):
                with st.container():
                    col_info, col_fav = st.columns([3, 2])
                    with col_info:
                        st.markdown(f"#### 📄 {f['name']}")
                        st.markdown(f'<a href="{f["webViewLink"]}" target="_blank" class="btn-open">Visualizar</a>', unsafe_allow_html=True)
                    with col_fav:
                        p_dest =
