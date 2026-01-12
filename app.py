import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
st.set_page_config(page_title="Oráculo", layout="wide")

# Frase "Esperar é Caminhar" com efeito DVD Bounce
st.markdown('<style>@keyframes bounceX {0% {left:0;} 100% {left:calc(100% - var(--w));}} @keyframes bounceY {0% {top:0;} 100% {top:calc(100% - var(--h));}} .bouncing-text {position:fixed;font-size:30px;font-weight:bold;color:#FFF;background-color:#000;padding:10px;white-space:nowrap;animation:bounceX 7s linear infinite alternate, bounceY 5s linear infinite alternate;z-index:999;--w:300px;--h:50px;display:inline-block;}@media (max-width:600px){.bouncing-text{font-size:20px;--w:200px;--h:40px;}}@keyframes f{0%,100%{transform:translateY(0)}50%{transform:translateY(-15px)}}.b{font-size:70px;text-align:center;animation:f 3s infinite;}</style><div class="bouncing-text">Esperar é Caminhar</div>', unsafe_allow_html=True)

@st.cache_resource
def get_s():
 if "google_auth" in st.secrets:
  return build('drive','v3',credentials=service_account.Credentials.from_service_account_info(st.secrets["google_auth"],scopes=['https://www.googleapis.com/auth/drive.readonly']))
 return None
s=get_s()
st.markdown('<div class="b">🔮</div><h2 style="text-align:center;">O Oráculo</h2>',unsafe_allow_html=True)
q=st.text_input("S",placeholder="Busque...",label_visibility="collapsed")
if q and s:
 r=s.files().list(q=f"name contains '{q}' and trashed=false",fields="files(name,webViewLink,mimeType)").execute().get('files',[])
 for i in r:
  if 'folder' not in i['mimeType']:st.markdown(f"📄 **[{i['name']}]({i['webViewLink']})**")
