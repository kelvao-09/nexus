import streamlit as st
import google.generativeai as genai
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="O Oráculo", layout="wide")

# --- ESTILO E ANIMAÇÃO (DVD BOUNCE) ---
st.markdown('<style>@keyframes bX{0%{left:0}100%{left:calc(100% - 220px)}}@keyframes bY{0%{top:0}100%{top:calc(100% - 50px)}}.dvd{position:fixed;font-size:20px;font-weight:bold;color:#FFF;background:#000;padding:10px;z-index:999;animation:bX 7s linear infinite alternate,bY 5s linear infinite alternate;}</style><div class="dvd">Esperar é Caminhar</div>', unsafe_allow_html=True)

# --- CONEXÕES (DRIVE E GEMINI) ---
@st.cache_resource
def iniciar_servicos():
    s = None
    if "google_auth" in st.secrets:
        sc = ['https://www.googleapis.com/auth/drive.readonly']
        s = build('drive', 'v3', credentials=service_account.Credentials.from_service_account_info(st.secrets["google_auth"], scopes=sc))
    
    if "gemini_api" in st.secrets:
        genai.configure(api_key=st.secrets["gemini_api"])
    
    return s

srv = iniciar_servicos()

# --- INTERFACE PRINCIPAL ---
st.markdown('<h1 style="text-align:center;">O Oráculo</h1>', unsafe_allow_html=True)
st.image("https://lh3.googleusercontent.com/rd-gg-dl/ABS2GSmNEX0Dw0uBJnn9_Hu8tEI4Z14i4rC4Im0Ko5lZ9ojchlG4aV_wxRZ4UEr79bY8Mqaju8oxTGjO1fbO_WwXv4zZaFshmSnkQyh8ahM6ItEDyGh6fjLnJWP5mVyxPQAuBRz5w4GtPHb0fTG1OGTdDqfmbjlpT5angjjW4VyvNLUmnMgeR3ODazEesTwevvX0gpR3w9thS089Xr3hnJTLkaG1aslhVw1hlGYeGOmiRWtQmrmnsxPGMUTVH8PyoyKAuiKsHkGk1lJZ6140NI5BL7di1dcpMfVmsF2li_tkETXUfMNybqciC-p_zCMu38m7VRAym4yyjnCpym-kPCcM0vUED2e7GBodvQ41f97AauzrTFfNTIoaTtoqmLs-hPRi3Hp401ePE2Q7ZdBjPstoiBHqps5cUOeNMIj9mrj4MJC4Lp6n4CMkQDtVXxUAIjhMMaRTNDc6WGeueccUlm7ieu0BYPQE-SeuVHA1ghLPziVOua-2GOlFMsrWY-vmHkRHtgEBcDg4GsQU3bWbQFx_DaYq5_hmJ9SAi_EssTujs_Law3rFnEpHS59Xd-hVD2wbZL_CDsL1MXLk5_W_HpZJro2Xf1yfYw0lCo3Hd-cmZUu2EkbKRAWYpJx5IcqzUG5nWtpSODZ2TbwiGCgVcXVT55x9ae03NPB2IRWdGTSWm2Stx4q-JKSb38IRpOYdP40hZF5X8suxC0c4ZYbIUu9SvLyIJDuHjxNrxnIMMqW6CCeleev2AKcDwyOPSgBFcJxT8ZoZSYzwJhi7q1iUP4pNgUAGSyBI3leRgNtTBImvw07wEiZ-aEtwB-Y1b2IKtIFkoWEb-LOdf9z_kCoKXDHvk14wEfo4WClHogxwfMsVd5jkwTdrTiYdMOQ3rf7Sddns4JKE_4ckmd3qjFahDQONykYfPSDLPQb0OLOxx6IU_2DAqC0BgIRe7QdUPZqvNkgn0alzLmsFpxMq0X6vhPonZnkDc8OLPF6bdcPKCMY8tD-fNK0ZCzy3ngqGR0gwubkq444prYr_jMdZaPK_NDuzT4n8jeAxhIYhQex4mtnVTxVyoytwF5239ABPvxqBE_1EhDEE-wiuxDiV1wlse4eUK0l_6FK_lcW47oOD-XruT1vAG-MJiGveU1hzWU6RESeODo-f_gOBND_hiMlHEh2AbGfWeCzX7EX4dxOv70oo59NzbHs2y4KFq0I=s1024-rj", width=250)

# Criando Abas para não bagunçar a tela
tab1, tab2 = st.tabs(["🔍 Busca de Arquivos", "💬 Chat com Documento"])

with tab1:
    q = st.text_input("O que você procura no Drive?", placeholder="Digite o nome do arquivo...")
    if q and srv:
        r = srv.files().list(q=f"name contains '{q}' and trashed=false", fields="files(id, name, webViewLink, mimeType)").execute().get('files', [])
        for i in r:
            if 'folder' not in i['mimeType']:
                st.markdown(f"📄 **[{i['name']}]({i['webViewLink']})**")

with tab2:
    st.subheader("Converse com o Oráculo")
    if "gemini_api" not in st.secrets:
        st.warning("Adicione a chave 'gemini_api' nos Secrets para ativar o chat.")
    else:
        pergunta = st.chat_input("Pergunte algo sobre seus arquivos...")
        if pergunta:
            model = genai.GenerativeModel('gemini-1.5-flash')
            # Aqui ele responde de forma geral até você selecionar um arquivo específico
            resposta = model.generate_content(f"Você é o sábio Oráculo. Responda: {pergunta}")
            st.write(resposta.text)
