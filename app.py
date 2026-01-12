import streamlit as st
import google.generativeai as genai
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(layout="wide")
ak = st.secrets.get("gemini_api")
au = st.secrets.get("google_auth")

if ak:
    genai.configure(api_key=ak)
    ia = genai.GenerativeModel(
        'gemini-1.5-flash'
    )

@st.cache_resource
def conv_drive():
    if au:
        c = service_account.Credentials.\
            from_service_account_info(
                au, scopes=[
                'https://www.googleapis.com/auth/drive.readonly'
                ])
        return build('drive','v3',credentials=c)
    return None

srv = conv_drive()
if "txt" not in st.session_state:
    st.session_state.txt = ""

# --- ESTILO ---
st.markdown('<style>@keyframes bX{0%{left:0}100%{left:calc(100% - 200px)}}@keyframes bY{0%{top:0}100%{top:calc(100% - 40px)}}.dvd{position:fixed;font-size:18px;font-weight:bold;color:#FFF;background:#000;padding:8px;z-index:999;animation:bX 7s linear infinite alternate,bY 5s linear infinite alternate;}</style><div class="dvd">Esperar é Caminhar</div>',unsafe_allow_html=True)

t1, t2 = st.tabs(["🔍 Busca", "💬 Chat"])

with t1:
    q = st.text_input("Arquivo:")
    if q and srv:
        f = f"name contains '{q}'"
        res = srv.files().list(
            q=f
        ).execute().get('files', [])
        for i in res:
            fid = i.get('id')
            fnm = i.get('name')
            st.write(f"📄 {fnm}")
            if st.button("Ler", key=fid):
                try:
                    # Download em partes para evitar linha longa
                    m = srv.files().get_media(
                        fileId=fid
                    ).execute()
                    st.session_state.txt = \
                        m.decode('utf-8')
                    st.success("Lido!")
                except:
                    st.error("Erro")

with t2:
    tx = st.session_state.txt
    if tx:
        p = st.chat_input("Dúvida?")
        if p:
            prompt = f"Texto: {tx}\n\n{p}"
            r = ia.generate_content(
