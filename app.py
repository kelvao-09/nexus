import streamlit as st
import os

# Configuração da página
st.set_page_config(page_title="Oráculo de Suporte", page_icon="🔮")

# Estilização para centralizar a barra de busca
st.markdown("""
    <style>
    .main {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .stTextInput {
        width: 70% !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🔮 Oráculo de Soluções")
st.subheader("Como posso te ajudar hoje?")

# Campo de pesquisa centralizado
query = st.text_input("Digite o problema (ex: lentidão, erro de login, rede)", placeholder="O que está acontecendo?")

# Simulação de uma base de dados (Pode ser substituído por busca em arquivos reais)
base_conhecimento = {
    "lentidão": "documento_performance_v1.pdf",
    "conexão": "guia_redes_config.pdf",
    "senha": "recuperacao_acesso.txt",
    "banco de dados": "query_optimization.pdf"
}

if query:
    query_clean = query.lower().strip()
    encontrado = False
    
    st.write(f"### Resultados para: {query}")
    
    # Lógica de busca simples por palavra-chave
    for chave, arquivo in base_conhecimento.items():
        if chave in query_clean:
            st.success(f"✅ Encontrei uma solução!")
            st.info(f"Assunto: {chave.capitalize()}")
            
            # Aqui você criaria o botão de download ou link para o arquivo
            st.write(f"📄 Arquivo disponível: **{arquivo}**")
            
            # Exemplo de botão de download (assumindo que o arquivo existe na pasta 'documentos')
            # with open(f"documentos/{arquivo}", "rb") as f:
            #    st.download_button("Baixar Documento", f, file_name=arquivo)
            
            encontrado = True
    
    if not encontrado:
        st.warning("Nenhum documento específico encontrado. Tente outras palavras-chave como 'rede' ou 'acesso'.")

else:
    st.info("Digite uma palavra-chave acima para consultar a base de conhecimento.")
