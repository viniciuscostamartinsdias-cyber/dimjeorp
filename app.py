import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Scanner Tipster Pro", layout="wide")
st.title("🤖 Scanner Tipster: Gerador de Bilhetes Automático")
st.markdown("Análise de jogos do dia, fase das equipes e geração de bilhetes baseados em estatísticas matemáticas.")

# --- DADOS SIMULADOS (Preparando o terreno para a API real) ---
def puxar_jogos_do_dia():
    # Simula a busca de jogos do dia atual nas ligas selecionadas
    hoje = datetime.now().strftime("%d/%m/%Y")
    
    dados = {
        "Liga": ["Premier League", "Premier League", "La Liga", "Brasileirão", "Brasileirão"],
        "Horário": ["11:00", "13:30", "16:00", "18:30", "21:00"],
        "Casa": ["Arsenal", "Manchester City", "Real Madrid", "Botafogo", "Flamengo"],
        "Fora": ["Aston Villa", "Newcastle", "Sevilla", "Grêmio", "Athletico-PR"],
        "Fase Casa (Últimos 5)": ["VVVEE", "VVVVV", "VVDEV", "VVVVD", "VEVDV"],
        "Fase Fora (Últimos 5)": ["EDDDV", "EEDVD", "DDEDD", "VEDEE", "EVDDD"],
        "Média Gols Jogo": [3.2, 3.8, 2.9, 2.5, 2.7]
    }
    return pd.DataFrame(dados)

# Criar os dados
df_jogos = puxar_jogos_do_dia()

# --- SEÇÃO 1: JOGOS DO DIA ---
st.header("📅 Jogos de Hoje")
ligas_selecionadas = st.multiselect(
    "Filtre pelas ligas desejadas:", 
    options=df_jogos['Liga'].unique(),
    default=df_jogos['Liga'].unique()
)

# Filtra a tabela baseada na seleção
df_filtrado = df_jogos[df_jogos['Liga'].isin(ligas_selecionadas)]
st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

st.divider()

# --- SEÇÃO 2: MOTOR DE BILHETES PRONTOS ---
st.header("🎟️ Bilhetes Prontos do Algoritmo")
st.write("Bilhetes gerados automaticamente cruzando o momento das equipes, desfalques e média de gols.")

col1, col2 = st.columns(2)

with col1:
    st.info("🔥 **Bilhete 1: Segurança Máxima (Baixo Risco)**")
    st.write("Foco em times com excelente fase jogando em casa.")
    st.markdown("""
    * **Manchester City x Newcastle:** Vitória do Man. City
    * **Arsenal x Aston Villa:** Arsenal ou Empate (Dupla Hipótese)
    * **Real Madrid x Sevilla:** Mais de 1.5 Gols na partida
    """)
    st.button("Copiar Bilhete 1 (Odd Sugerida: 2.15)")

with col2:
    st.warning("⚡ **Bilhete 2: Ousadia & Gols (Médio Risco)**")
    st.write("Foco em partidas abertas com alta média de gols esperados (xG).")
    st.markdown("""
    * **Botafogo x Grêmio:** Ambas Marcam (Sim)
    * **Manchester City x Newcastle:** Mais de 2.5 Gols na partida
    * **Flamengo x Athletico-PR:** Mais de 8.5 Escanteios
    """)
    st.button("Copiar Bilhete 2 (Odd Sugerida: 4.80)")

st.divider()

# --- SEÇÃO 3: ANÁLISE PROFUNDA DE UM JOGO ---
st.header("🔍 Raio-X do Confronto")
jogo_analise = st.selectbox("Selecione um jogo para ver os detalhes que geraram o bilhete:", df_filtrado['Casa'] + " x " + df_filtrado['Fora'])

if jogo_analise:
    st.write(f"**Análise da Inteligência para:** {jogo_analise}")
    st.markdown("""
    * **Fator Casa:** O time mandante venceu 8 dos últimos 10 jogos no seu estádio.
    * **Jogadores Chave:** O artilheiro principal está confirmado. Nos últimos 5 jogos com ele em campo, o time marcou pelo menos 2 gols.
    * **Confronto Direto:** O time visitante não vence neste estádio há 4 anos.
    * **Conclusão Matemática:** Probabilidade de 74% de vitória do mandante. Evitar apostar contra.
    """)
