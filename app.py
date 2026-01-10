import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Nexus Dashboard", layout="wide")

# Título Principal
st.title("Nexus")

# Justificativa do Nome (em itálico ou destaque)
st.markdown("""
> **NEXUS** representa a conexão essencial entre atenção, esforço e gentileza. 
> É o elo que une nossa equipe, fortalecendo a colaboração e o comprometimento 
> para alcançar resultados de excelência.
""")

st.divider()

# --- ÁREA DE METAS DA EQUIPE ---
st.header("Acompanhamento de Metas")

# Exemplo de dados (você poderá conectar a uma planilha depois)
meta_global = 100000
alcancado = 75000
progresso = alcancado / meta_global

# Exibição de Métricas em Colunas
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Meta Total", value=f"R$ {meta_global:,.2f}")

with col2:
    st.metric(label="Alcançado", value=f"R$ {alcancado:,.2f}", delta=f"{progresso:.1%}")

with col3:
    st.write("**Progresso da Equipe**")
    st.progress(progresso)

# --- TABELA DE MEMBROS DA EQUIPE ---
st.subheader("Desempenho por Integrante")

# Criando um pequeno exemplo de tabela
dados_equipe = pd.DataFrame({
    "Integrante": ["Ana", "Bruno", "Carlos", "Daniela"],
    "Meta Individual": [25000, 25000, 25000, 25000],
    "Realizado": [22000, 18000, 25000, 10000],
})

dados_equipe["Status (%)"] = (dados_equipe["Realizado"] / dados_equipe["Meta Individual"]) * 100

st.dataframe(dados_equipe, use_container_width=True)

# Mensagem motivacional baseada no nome Nexus
if progresso >= 1.0:
    st.balloons()
    st.success("Excelente! O elo Nexus nos levou ao objetivo!")
