import streamlit as st
import os

# CONFIGURAÇÕES INICIAIS
st.set_page_config(page_title="Oráculo", page_icon="🔮")

# --- AJUSTE ESTES DADOS ---
# Substitua pelo seu usuário e nome do repositório no GitHub
USUARIO_GITHUB = "seu-usuario"
REPOSITORIO_GITHUB = "nome-do-seu-repo"
PASTA_DOCS = "documentos"
# --------------------------

st.title("🔮 Oráculo de Documentos")

busca = st.text_input("O que você deseja encontrar?", placeholder="Digite aqui...")

if busca:
    if os.path.exists(PASTA_DOCS):
        arquivos = os.listdir(PASTA_DOCS)
        resultados = [f for f in arquivos if busca.lower() in f.lower()]
        
        if resultados:
            st.write(f"### ✅ Encontrei {len(resultados)} resultado(s):")
            
            for nome_arquivo in resultados:
                # Criamos o link oficial do GitHub para "Visualização Direta" (Raw)
                # Esse link faz o navegador abrir o PDF ou imagem em vez de baixar
                url_github = f"https://github.com/{USUARIO_GITHUB}/{REPOSITORIO_GITHUB}/blob/main/{PASTA_DOCS}/{nome_arquivo}"
                
                # Criamos um botão visual que abre o link
                st.markdown(f"""
                    <a href="{url_github}" target="_blank" style="text-decoration: none;">
                        <div style="
                            background-color: #4CAF50;
                            color: white;
                            padding: 10px 20px;
                            text-align: center;
                            border-radius: 5px;
                            margin: 5px 0;
                            cursor: pointer;
                            display: inline-block;
                            font-weight: bold;
                        ">
                            📄 Abrir documento: {nome_arquivo}
                        </div>
                    </a>
                """, unsafe_allow_html=True)
        else:
            st.warning("Nenhum documento encontrado.")
    else:
        st.error("Pasta de documentos não encontrada.")
else:
    st.info("Digite uma palavra-chave para começar.")
