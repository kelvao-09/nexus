import streamlit as st
import google.generativeai as genai
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="Oráculo", layout="wide")
ak, au = st.secrets.get("gemini_api"), st.secrets.get("google_auth")

# --- ESTILO ---
st.markdown('<style>@keyframes bX{0%{left:0}100%{left:calc(100% - 200px)}}@keyframes bY{0%{top:0}100%{top:calc(100% - 40px)}}.dvd{position:fixed;font-size:18px;font-weight:bold;color:#FFF;background:#000;padding:8px;z-index:999;animation:bX 7s linear infinite alternate,bY 5s linear infinite alternate;}</style><div class="dvd">Esperar é Caminhar</div>',unsafe_allow_html=True)
st.markdown('<h1 style="text-align:center;">O Oráculo</h1>',unsafe_allow_html=True)
st.image("https://lh3.googleusercontent.com/rd-gg-dl/ABS2GSmNEX0Dw0uBJnn9_Hu8tEI4Z14i4rC4Im0Ko5lZ9ojchlG4aV_wxRZ4UEr79bY8Mqaju8oxTGjO1fbO_WwXv4zZaFshmSnkQyh8ahM6ItEDyGh6fjLnJWP5mVyxPQAuBRz5w4GtPHb0fTG1OGTdDqfmbjlpT5angjjW4VyvNLUmnMgeR3ODazEesTwevvX0gpR3w9thS089Xr3hnJTLkaG1aslhVw1hlGYeGOmiRWtQmrmnsxPGMUTVH8PyoyKAuiKsHkGk1lJZ6140NI5BL7di1dcpMfVmsF2li_tkETXUfMNybqciC-p_zCMu38m7VRAym4yyjnCpym-kPCcM0vUED2e7GBodvQ41f97AauzrTFfNTIoaTtoqmLs-hPRi3Hp401ePE2Q7ZdBjPstoiBHqps5cUOeNMIj9mrj4MJC4Lp6n4CMkQDtVXxUAIjhMMaRTNDc6WGeueccUlm7ieu0BYPQE-SeuVHA1ghLPziVOua-2GOlFMsrWY-vmHkRHtgEBcDg4GsQU3bWbQFx_DaYq5_hmJ9SAi_EssTujs_Law3rFnEpHS59Xd-hVD2wbZL_CDsL1MXLk5_W_HpZJro2Xf1yfYw0lCo3Hd-cmZUu2EkbKRAWYpJx5IcqzUG5nWtpSODZ2TbwiGCgVcXVT55x9ae03NPB2IRWdGTSWm2Stx4q-JKSb38IRpOYdP40hZF5X8suxC0c4ZYbIUu9SvLyIJDuHjxNrxnIMMqW6CCeleev2AKcDwyOPSgBFcJxT8ZoZSYzwJhi7q1iUP4pNgUAGSyBI3leRgNtTBImvw07wEiZ-aEtwB-Y1b2IKtIFkoWEb-LOdf9z_kCoKXDHvk14wEfo4WClHogxwfMsVd5jkwTdrTiYdMOQ3rf7Sddns4JKE_4ckmd3qjFahDQONykYfPSDLPQb0OLOxx6IU_2DAqC0BgIRe7QdUPZqvNkgn0alzLmsFpxMq0X6vhPonZnkDc8OLPF6bdcPKCMY8tD-fNK0ZCzy3ngqGR0gwubkq444prYr_jMdZaPK_NDuzT4n8jeAxhIYhQex4mtnVTxVyoytwF5239ABPvxqBE_1EhDEE-wiuxDiV1wlse4eUK0l_6FK_lcW47oOD-XruT1vAG-MJiGveU1hzWU6RESeODo-f_gOBND_hiMlHEh2AbGfWeCzX7EX4dxOv70oo59NzbHs2y4KFq0I=s1024-rj", width=180)

# --- INICIALIZAÇÃO DRIVE ---
@st.cache_resource
def get_drive(auth):
    creds = service_account.Credentials.from_service_account_info(auth, scopes=['https://www.googleapis.com/auth/drive.readonly'])
    return build('drive', 'v3', credentials=creds)

if ak: genai.configure(api_key=ak)
srv = get_drive(au) if au else None

# --- LÓGICA DE ABAS ---
t1, t2 = st.tabs(["🔍 Busca e Leitura", "💬 Chat Inteligente"])

# Variável para guardar o conteúdo do documento na sessão do navegador
if "doc_text" not in st.session_state: st.session_state.doc_text = ""

with t1:
    q = st.text_input("Procure o documento para ler:")
    if q and srv:
        res = srv.files().list(q=f"name contains '{q}'", fields="files(id,name,mimeType,webViewLink)").execute().get('files', [])
        for i in res:
            col1, col2 = st.columns([3, 1])
            col1.markdown(f"📄 **[{i['name']}]({i['webViewLink']})**")
            if col2.button("Ler este", key=i['id']):
                with st.spinner("Lendo documento..."):
                    try:
                        # Se for Google Doc, exporta como texto. Se for arquivo txt, baixa direto.
                        if "google-apps.document" in i['mimeType']:
                            content = srv.files().export(fileId=i['id'], mimeType='text/plain').execute().decode('utf-8')
                        else:
                            content = srv.files().get_media(fileId=i['id']).execute().decode('utf-8')
                        st.session_state.doc_text = content
                        st.success("Documento carregado! Vá para a aba Chat.")
                    except: st.error("Não consegui ler este formato ainda.")

with t2:
    if st.session_state.doc_text:
        st.info("O Oráculo está pronto para responder sobre o documento carregado.")
        p = st.chat_input("O que queres saber sobre o documento?")
        if p:
            md = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"Contexto do documento:\n{st.session_state.doc_text}\n\nPergunta: {p}"
            r = md.generate_content(prompt)
            st.chat_message("assistant").write(r.text)
    else:
        st.warning("Primeiro, procure e clique em 'Ler este' na aba de Busca.")

st.markdown('<p style="text-align:center;font-style:italic;margin-top:40px;">"Esperar é Caminhar"</p>',unsafe_allow_html=True)
