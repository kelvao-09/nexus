import streamlit as st
import os

# 1. Configurações Iniciais da Página
st.set_page_config(
    page_title="Oráculo de Suporte",
    page_icon="🔮",
    layout="centered"
)

# 2. Estilização CSS para centralizar e melhorar o visual
st.markdown("""
    <style>
    .main {
        text-align: center;
    }
    .stTextInput {
        max-width: 600px;
        margin: 0 auto;
    }
    .stDownloadButton {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Título e Cabeçalho
st.title("🔮 Oráculo de Conhecimento")
st.write("Digite o nome do problema ou do documento que você precisa encontrar.")

# 4. Configuração da Pasta (Verifique se no GitHub o nome é exatamente este)
PASTA_DOCS = "documentos"

# 5. Campo de Pesquisa Centralizado
busca = st.text_input("", placeholder="Ex: lentidão, rede, acesso, erro...")

st.markdown("---") # Linha divisória

# 6. Lógica de Busca e Exibição
if busca:
    # Verifica se a pasta existe no repositório
    if os.path.exists(PASTA_DOCS):
        # Lista todos os arquivos dentro da pasta
        todos_arquivos = os.listdir(PASTA_DOCS)
        
        # Filtra os arquivos com base na busca (ignora maiúsculas/minúsculas)
        resultados = [f for f in todos_arquivos if busca.lower() in f.lower()]
        
        if resultados:
            st.success
