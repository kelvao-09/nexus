import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Configuração da Página
st.set_page_config(page_title="Oráculo Pro", page_icon="🔮", layout="wide")

# Inicializar estrutura de pastas se não existir
if 'pastas_fav' not in st.session_state:
    st.session_state.pastas_fav = {"Geral": []}

# 2. Estilo CSS
st.markdown("""
<style>
    .fav-item {
        background: #ffffff;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 5px;
        border-left: 4px solid #FFD700;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .btn-open {
        background-color: #4285F4;
        color: white !important;
        padding: 5px 10px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        font-size: 12px;
    }
    .stButton button { width: 100%; }
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
    except: return None

service = get_drive_service()

# 4. Barra Lateral: Gerenciamento Avançado
with st.sidebar:
    st.header("📂 Gerenciar Pastas")
    
    # Criar nova pasta
    with st.expander("➕ Nova Pasta"):
        nome_n = st.text_input("Nome:")
        if st.button("Criar"):
            if nome_n and nome_n not in st.session_state.pastas_fav:
                st.session_state.pastas_fav[nome_n] = []
                st.rerun()

    st.divider()

    # Listar e Editar Pastas
    pastas = list(st.session_state.pastas_fav.keys())
    for pasta in pastas:
        with st.expander(f"📁 {pasta} ({len(st.session_state.pastas_fav[pasta])})"):
            # Opções da Pasta
            col_edit, col_del = st.columns(2)
            
            # Editar Nome da Pasta
            novo_nome = st.text_input("Renomear:", value=pasta, key=f"ren_{pasta}")
            if novo_nome != pasta and st.button("Salvar Nome", key=f"save_{pasta}"):
                st.session_state.pastas_fav[novo_nome] = st.session_state.pastas_fav.pop(pasta)
                st.rerun()
            
            # Deletar Pasta
            if st.button("🗑️ Deletar Pasta", key=f"del_p_{pasta}"):
                if pasta != "Geral":
                    del st.session_state.pastas_fav[pasta]
                    st.rerun()
                else:
                    st.warning("Não é possível deletar a pasta Geral.")

            st.markdown("---")
            
            # Listar Itens e Opção de Mover
            itens = st.session_state.pastas_fav[pasta]
            for idx, item in enumerate(itens):
                st.markdown(f'<div class="fav-item"><b>{item["name"]}</b></div>', unsafe_allow_html=True)
                
                # Mover item
                outras_pastas = [p for p in st.session_state.pastas_fav.keys() if p != pasta]
                if outras_pastas:
                    dest = st.selectbox("Mover para:", outras_pastas, key=f"mov_sel_{pasta}_{idx}")
                    if st.button("Mover", key=f"mov_btn_{pasta}_{idx}"):
                        st.session_state.pastas_fav[dest].append(st.session_state.pastas_fav[pasta].pop(idx))
                        st.rerun()
                
                if st.button("❌ Remover", key=f"rem_itm_{pasta}_{idx}"):
                    st.session_state.pastas_fav[pasta].pop(idx)
                    st.rerun()

# 5. Busca e Resultados (Interface Principal)
st.title("🔮 Oráculo")
c1, c2, c3 = st.columns([1,2,1])
with c2:
    busca = st.text_input("", placeholder="Pesquise o documento...")

if busca and service:
    try:
        q = f"name contains '{busca}' and mimeType != 'application/vnd.google-apps.folder' and trashed = false"
        res = service.files().list(q=q, fields="files(id, name, webViewLink)").execute()
        files = res.get('files', [])

        if files:
            for i, f in enumerate(files):
                with st.container():
                    col_info, col_act = st.columns([3, 2])
                    with col_info:
                        st.markdown(f"#### 📄 {f['name']}")
                        st.markdown(f'<a href="{f["webViewLink"]}" target="_blank" class="btn-open">Abrir</a>', unsafe_allow_html=True)
                    with col_act:
                        p_alvo = st.selectbox("Pasta destino:", list(st.session_state.pastas_fav.keys()), key=f"main_sel_{i}")
                        if st.button("⭐ Favoritar", key=f"main_btn_{i}"):
                            st.session_state.pastas_fav[p_alvo].append({'id': f['id'], 'name': f['name'], 'link': f['webViewLink']})
                            st.toast(f"Salvo em {p_alvo}")
                    st.divider()
        else: st.warning("Nada encontrado.")
    except Exception as e: st.error(f"Erro: {e}")
