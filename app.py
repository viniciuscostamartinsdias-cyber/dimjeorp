import streamlit as st
import pandas as pd
import random

# Configuração da Página
st.set_page_config(page_title="Scanner de Apostas Pro", layout="wide")
st.title("⚽ Scanner de Apostas: Análise e Prognósticos")

st.markdown("""
Painel analítico para jogos do dia. O algoritmo cruza estatísticas de equipes com as odds atuais da **Betano** e **Superbet** para encontrar oportunidades de valor.
""")

# --- SIMULAÇÃO DE DADOS (Aqui entrará a integração com a API depois) ---
def buscar_jogos_do_dia():
    # Simulação do que uma API retornaria
    dados = {
        "Liga": ["Brasileirão", "Brasileirão", "Premier League", "La Liga"],
        "Time Casa": ["Flamengo", "Palmeiras", "Arsenal", "Real Madrid"],
        "Time Fora": ["Fluminense", "São Paulo", "Chelsea", "Barcelona"],
        "Odd Casa (Betano)": [1.80, 2.10, 2.30, 1.95],
        "Odd Fora (Superbet)": [4.20, 3.50, 3.10, 3.80],
        "Gols Casa (Média)": [2.1, 1.8, 2.5, 2.2],
        "Gols Fora (Média)": [1.1, 1.2, 1.5, 1.4]
    }
    return pd.DataFrame(dados)

df_jogos = buscar_jogos_do_dia()

# --- INTERFACE DO USUÁRIO ---
st.subheader("📅 Jogos de Hoje")
st.dataframe(df_jogos, use_container_width=True)

st.divider()

# --- MOTOR DE RECOMENDAÇÃO ---
st.subheader("💡 Algoritmo de Sugestão de Aposta")
jogo_selecionado = st.selectbox("Selecione um jogo para análise profunda:", df_jogos['Time Casa'] + " x " + df_jogos['Time Fora'])

# Lógica de cálculo simulada
if st.button("Analisar Jogo e Gerar Aposta"):
    st.info(f"Analisando histórico de {jogo_selecionado}...")
    
    # Exemplo de lógica que criaríamos:
    # Se a média de gols dos dois times for alta, sugere Over 2.5
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("**Sugestão de Aposta: Mais de 2.5 Gols na Partida**")
        st.write("**Probabilidade calculada pelo Algoritmo:** 68%")
        st.write("**Justificativa:** Ambas as equipes têm média superior a 1.5 gols marcados por partida nos últimos 5 confrontos.")
        
    with col2:
        st.warning("**Onde Apostar (Melhor Odd):**")
        st.write("🏆 **Betano:** Odd 1.95")
        st.write("🥈 Superbet: Odd 1.88")
        st.write("*Aposta de Valor (EV+) encontrada!*")

st.caption("Aviso: Apostas esportivas envolvem risco financeiro. Este algoritmo utiliza estatísticas para sugerir tendências matemáticas, mas não garante resultados.")
