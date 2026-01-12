import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Configuração e Estilo
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

if 'hist' not in st.session_state:
    st.session_state.hist = []

st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; }
    .card { background: white; padding: 15px; border-radius: 10px; margin-bottom: 10px; border: 1px solid #EEE; display: flex; justify-content: space-between; align-items: center; }
    .btn { background-color: #4285F4; color: white !important; text-decoration: none !important; padding: 6px 15px; border-radius: 6px; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# 2. Conexão Drive
@st.cache_resource
def get_svc():
    try:
        if "google_auth" in st.secrets:
            auth = st.secrets["google_auth"]
            creds = service_account.Credentials.from_service_account_info(auth, scopes=['https://www.googleapis.com/auth/drive.readonly'])
            return build('drive', 'v3', credentials=creds)
    except: return None
    return None

svc = get_svc()

# 3. Interface Principal
st.markdown("<h1 style='text-align: center;'>🔮 O Oráculo</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    busca = st.text_input("Busca", placeholder="Pesquisar arquivo...", label_visibility="collapsed")
    
    # Histórico clicável
    if st.session_state.hist:
        cols = st.columns(len(st.session_state.hist) + 1)
        for i, t in enumerate(st.session_state.hist):
            if cols[i].button(t, key=f"h_{i}"):
                busca = t
        if cols[-1].button("🗑️"):
            st.session_state.hist = []
            st.rerun()

# 4. Lógica do Histórico (Aqui estava o erro anterior)
if busca:
    if busca not in st.session_state.hist:
        st.session_state.hist.insert(0, busca)
        st.session_state.hist = st.session_state.hist[:5]

# 5. Busca e Resultados (Apenas Arquivos, Sem Pastas)
if busca and svc:
    try:
        # Filtro: Contém nome, NÃO é pasta, NÃO está na lixeira
        q = f"name contains '{busca}' and mimeType != 'application/vnd.google-apps.folder' and trashed = false"
        res = svc.files().list(q=q, fields="files(id, name, webViewLink)").execute()
        files = res.get('files', [])
        
        if files:
            st.markdown("<br>", unsafe_allow_html=True)
            for f in files:
                st.markdown(f"""
                <div class="card">
                    <div><b>📄 {f['name']}</b></div>
                    <a href="{f['webViewLink']}" target="_blank" class="btn">Abrir</a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Nenhum arquivo encontrado.")
    except Exception as e:
        st.error(f"Erro na busca: {e}")
