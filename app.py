import streamlit as st
import google.generativeai as genai
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configurações iniciais
ak = st.secrets.get("gemini_api")
au = st.secrets.get("google_auth")

if ak:
    genai.configure(api_key=ak)
    md = genai.GenerativeModel('gemini-1.5-flash')

if "txt" not in st.session_state:
    st.session_state.txt = ""

st.title("O Oráculo")

# Abas simples
t1, t2 = st.tabs(["Busca", "Chat"])

with t1:
    q = st.text_input("Arquivo:")
    if q and au:
        c = service_account.Credentials.from_service_account_info(au, scopes=['https://www.googleapis.com/auth/drive.readonly'])
        s = build('drive', 'v3', credentials=c)
        # Busca simplificada
        res = s.files().list(q=f"name contains '{q}'").execute().get('files', [])
        for i in res:
            st.write(f"📄 {i['name']}")
            if st.button("Ler", key=i['id']):
                try:
                    # Tenta ler Google Docs ou arquivo comum
                    if "google-apps.document" in i['mimeType']:
                        m = s.files().export(fileId=i['id'], mimeType='text/plain').execute()
                    else:
                        m = s.files().get_media(fileId=i['id']).execute()
                    st.session_state.txt = m.decode('utf-8')
                    st.success("Lido!")
                except:
                    st.error("Erro ao ler")

with t2:
    if st.session_state.txt:
        p = st.chat_input("Dúvida sobre o doc?")
        if p:
            # Prompt curto para evitar corte
            ctx = st.session_state.txt[:5000] # Limite de texto
            full_p = f"Doc: {ctx}\n\nPergunta: {p}"
            resp = md.generate_content(full_p)
            st.write(resp.text)
    else:
        st.warning("Leia um arquivo na aba Busca.")
