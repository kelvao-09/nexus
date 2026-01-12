import streamlit as st
import os

# Configurações básicas
st.set_page_config(page_title="Oráculo", page_icon="🔮")

st.title("🔮 Oráculo de Documentos")

# Nome da pasta (verifique se está igual no GitHub)
PASTA_DOCS = "documentos"

# Barra de pesquisa
busca = st.text_input("O que você deseja encontrar?", placeholder="Digite aqui...")

if busca:
    # Verifica se a pasta existe
    if os.path.exists(PASTA_DOCS):
        arquivos = os.listdir(PASTA_DOCS)
        
        # Filtra os arquivos (procura o termo digitado no nome do arquivo)
        resultados = [f for f in arquivos if busca.lower() in f.lower()]
        
        if resultados:
            st.write(f"### ✅ Encontrei {len(resultados)} resultado(s):")
            
            for nome_arquivo in resultados:
                caminho_completo = os.path.join(PASTA_DOCS, nome_arquivo)
                
                # Botão de Download
                with open(caminho_completo, "rb") as f:
                    st.download_button(
                        label=f"Baixar: {nome_arquivo}",
                        data=f.read(),
                        file_name=nome_arquivo,
                        key=nome_arquivo # Importante para não dar erro de botões duplicados
                    )
        else:
            st.warning("Nenhum documento encontrado com esse nome.")
    else:
        st.error(f"Erro: A pasta '{PASTA_DOCS}' não foi encontrada no repositório.")
else:
    st.info("Digite uma palavra-chave para começar a busca.")
