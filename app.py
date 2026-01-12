import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
st.set_page_config(page_title="Oráculo", layout="wide")

# Gatinho que escuta o teclado globalmente
st.markdown("""
<div id="c" style="position:fixed;bottom:20px;right:20px;font-size:50px;z-index:9999;transition:0.1s;pointer-events:none;">🐈‍⬛</div>
<script>
let x=0, y=0;
const g=document.getElementById('c');
// Escuta o teclado em toda a janela (window)
window.parent.document.addEventListener('keydown', (e) => {
    if(e.key=='ArrowUp') y-=30;
    if(e.key=='ArrowDown') y+=30;
    if(e.key=='ArrowLeft') x-=30;
    if(e.key=='ArrowRight') x+=30;
    g.style.transform = `translate(${x}px, ${y}px)`;
    // Impede a página de rolar enquanto você move o gato
    if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.key)) e.preventDefault();
});
</script>
<style>@keyframes f{0%,100%{transform:translateY(0)}50%{transform:translateY(-15px)}}.b{font-size:70px;text-align:center;animation:f 3s infinite;}</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_s():
    if "google_auth" in st.secrets:
        return build('drive','v3',credentials=service_account.Credentials.from_service_account_info(st.secrets["google_auth"],scopes=['https://www.googleapis.com/auth/drive.readonly']))
    return None

s=get_s()
st.markdown('<div class="b">🔮</div><h2 style="text-align:center;">Oráculo</h2>',unsafe_allow_html=True)
q=st.text_input("S",placeholder="Busque aqui...",label_visibility="collapsed")

if q and s:
    try:
        r=s.files().list(q=f"name contains '{q}' and trashed=false",fields="files(name,webViewLink,mimeType)").execute().get('files',[])
        for i in r:
            if 'folder' not in i['mimeType']:st.markdown(f"📄 **[{i['name']}]({i['webViewLink']})**")
    except:st.error("!")
