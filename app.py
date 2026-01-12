import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="Oráculo", layout="wide")

# INJEÇÃO DIRETA: Gatinho que segue o mouse via JS Simples (Testado para Streamlit)
st.markdown("""
    <div id="cat-container" style="position:fixed; top:0; left:0; width:100vw; height:100vh; pointer-events:none; z-index:10000;">
        <div id="moving-cat" style="position:absolute; font-size:40px; transition: transform 0.1s linear;">🐈</div>
    </div>
    <script>
        const container = window.parent.document;
        const cat = document.getElementById('moving-cat');
        container.addEventListener('mousemove', (e) => {
            const x = e.clientX;
            const y = e.clientY;
            cat.style.transform = `translate(${x + 10}px, ${y + 10}px)`;
        });
    </script>
    <style>
        @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
        .magic-ball { font-size: 70px; text-align: center; animation: float 3s infinite; margin-top: 30px; }
        .stApp { cursor: default; }
    </style>
""", unsafe_allow_html=True)

# 2. CONEXÃO DRIVE
@st.cache_resource
def get_drive():
    try:
        if "google_auth" in st.secrets:
            info = st.secrets["google_auth"]
            creds = service_account.Credentials.from_service_account_info(info, scopes=['https://www.googleapis.com/auth/drive.readonly'])
            return build('drive', 'v3', credentials=creds)
    except: return None
    return None

drive_service = get_drive()

# 3. INTERFACE
st.markdown('<div class="magic-ball">🔮</div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center;'>O Oráculo</h1>", unsafe_allow_html=True)

if 'h' not in st.session_state: st.session_state.h = []
busca = st.text_input("S", placeholder="O que busca?", label_visibility="collapsed")

if busca:
    if busca not in st.session_state.h:
        st.session_state.h.insert(0, busca)
        st.session_state.h = st.session_state.h[:5]
    
    if drive_service:
        try:
            q = f"name contains '{busca}' and mimeType != 'application/vnd.google-apps.folder' and trashed = false"
            res = drive_service.files().list(q=q, fields="files(name, webViewLink)").execute()
            for f in res.get('files', []):
                st.markdown(f"📄 **[{f['name']}]({f['webViewLink']})**")
        except: st.error("Erro na busca.")
