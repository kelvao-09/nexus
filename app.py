import streamlit as st
import google.generativeai as genai
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configs
ak, au = st.secrets.get("gemini_api"), st.secrets.get("google_auth")
if ak:
    genai.configure(api_key=ak)
    md = genai.GenerativeModel('gemini-1.5-flash')

if "txt" not in st.session_state: st.session_state.txt = ""

st.title("O Oráculo")
t1, t2 = st.tabs(["Busca", "Chat"])

with t1:
    q = st.text_input("Arquivo:")
    if q and au:
        c = service_account.Credentials.from_service_account_info(au, scopes=['https://www.googleapis.com/auth/drive.readonly'])
        s = build('drive', 'v3', credentials=c)
        res = s.files().list(q=f"name contains '{q}'").execute().get('files', [])
        for i in res:
            st.write(f"📄 {i['name']}")
            if st.button("Ler", key=i['id']):
                try:
                    # Tenta exportar como texto puro (funciona para Google Docs)
                    m = s.files().export(fileId=i['id'], mimeType='text/plain').execute()
                    st.session_state.txt = m.decode('utf-8')
                    st.success("Lido com sucesso!")
                except:
                    try:
                        # Tenta baixar direto (funciona para arquivos .txt)
                        m = s.files().get_media(fileId=i['id']).execute()
                        st.session_state.txt = m.decode('utf-8')
                        st.success("Lido com sucesso!")
                    except:
                        st.error("Formato incompatível (tente Google Docs ou .txt)")

with t2:
    if st.session_state.txt:
        p = st.chat_input("Dúvida?")
        if p:
            r = md.generate_content(f"Doc: {st.session_state.txt[:5000]}\n\nPergunta: {p}")
            st.chat_message("assistant").write(r.text)
    else: st.warning("Leia um arquivo primeiro.")
