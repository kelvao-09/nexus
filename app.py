import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Configuração da Página
st.set_page_config(page_title="Oráculo Pro", page_icon="🔮", layout="wide")

# Inicializar estrutura de pastas
if 'pastas_fav' not in st.session_state:
    st.session_state.pastas_fav = {"Geral": []}

# 2. CSS para visual sofisticado
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
        text-align: center;
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
    except:
        return None

service = get_drive_service()

# 4. Barra Lateral (Pastas e Menu ⋮)
with st.sidebar:
    st.title("📂 Favoritos")
    
    with st.popover("➕ Nova Pasta", use_container_width=True):
        n_nome = st.text_input("Nome da pasta:")
        if st.button("Criar"):
            if n_nome and n_nome not in st.session_state.pastas_fav:
                st.session_state.pastas_fav[n_nome] = []
                st.rerun()
    
    st.divider()

    for pasta in list(st.session_state.pastas_fav.keys()):
        col_n, col_m = st.columns([0.85, 0.15])
        
        with col_n:
            exp = st.expander(f"📁 {pasta}")
        
        with col_m:
            with st.popover("⋮"):
                st.write(f"Configurar: {pasta}")
                novo_n = st.text_input("Renomear:", value=pasta, key=f"re_{pasta}")
                if st.button("Salvar Nome", key=f"sv_{pasta}"):
                    st.session_state.pastas_fav[novo_n] = st.session_state.pastas_fav.pop(pasta)
                    st.rerun()
                if pasta != "Geral":
                    if st.button("🗑️ Deletar", key=f"dl_{pasta}"):
                        del st.session_state.pastas_fav[pasta]
                        st.rerun()
        
        with exp:
            itens = st.session_state.pastas_fav[pasta]
            if not itens:
                st.caption("Pasta vazia")
            else:
                for idx, item in enumerate(itens):
                    st.markdown(f'<div class="fav-item"><b>{item["name"]}</b><br><a href="{item["link"]}" target="_blank" style="font-size:11px; color:#4285F4; text-decoration:none;">Abrir ↗️</a></div>', unsafe_allow_html=True)
                    
                    c_mov, c_rem = st.columns([3, 1])
                    with c_mov:
                        outras = [p for p in st.session_state.pastas_fav.keys() if p != pasta]
                        if outras:
                            dest = st.selectbox("Mover:", outras, key=f"mv_{pasta}_{idx}")
                            if st.button("OK", key=f"bt_mv_{pasta}_{idx}"):
                                st.session_state.pastas_fav[dest].append(st.session_state.pastas_fav[pasta].pop(idx))
                                st.rerun()
                    with c_rem:
                        if st.button("❌", key=f"rm_{pasta}_{idx}"):
                            st.session_state.pastas_fav[pasta].pop(idx)
                            st.rerun()

# 5. Interface Principal (Pesquisa Centralizada)
st.markdown("<h1 style='text-align: center;'>🔮 O Oráculo</h1>", unsafe_allow_html=True)

# Centralizar barra de pesquisa
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    busca = st.text_input("Pesquisar:", placeholder="Digite o que deseja encontrar...", label_visibility="collapsed")

# 6. Resultados da Busca
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
