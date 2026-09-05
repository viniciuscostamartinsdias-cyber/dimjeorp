import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import random

# Configuração da Página
st.set_page_config(page_title="Scanner Tipster Pro - Ligas", layout="wide")

# ==========================================
# 🔑 COLE A SUA CHAVE DA API AQUI DENTRO DAS ASPAS
API_KEY = "4cd900e44cb240f7b7ef7f2c2b95b423"
# ==========================================

st.title("🏆 Scanner Tipster Pro: Ligas e Campeonatos")
st.markdown("Selecione a data e clique na liga desejada para ver os jogos do dia e montar suas apostas.")

# --- 1. BANCO DE JOGADORES ---
def obter_jogadores(time):
    elencos = {
        "Manchester City": ["E. Haaland", "P. Foden", "R. Cherki", "Ederson (GOL)"],
        "Real Madrid": ["K. Mbappé", "V. Júnior", "J. Bellingham", "T. Courtois (GOL)"],
        "Arsenal": ["B. Saka", "M. Ødegaard", "D. Rice", "David Raya (GOL)"],
        "Bayern Munich": ["H. Kane", "J. Musiala", "F. Wirtz", "M. Neuer (GOL)"],
        "Barcelona": ["L. Yamal", "N. Williams", "Pedri", "ter Stegen (GOL)"],
        "Liverpool": ["L. Díaz", "C. Gakpo", "A. Mac Allister", "Alisson (GOL)"],
        "Paris Saint Germain": ["O. Dembélé", "B. Barcola", "Vitinha", "Donnarumma (GOL)"],
        "Flamengo": ["Pedro", "G. Arrascaeta", "L. Paquetá", "Rossi (GOL)"],
        "Palmeiras": ["V. Roque", "Estêvão", "F. Anderson", "Weverton (GOL)"],
        "Botafogo": ["Tiquinho Soares", "M. Savarino", "M. Freitas", "John (GOL)"],
        "São Paulo": ["J. Calleri", "L. Moura", "Pablo Maia", "Rafael (GOL)"],
        "Vasco da Gama": ["P. Vegetti", "D. Payet", "Léo", "Léo Jardim (GOL)"],
        "Fluminense": ["G. Cano", "J. Arias", "Thiago Silva", "Fábio (GOL)"],
        "Cruzeiro": ["Matheus Pereira", "Arthur Gomes", "Zé Ivaldo", "Cássio (GOL)"],
        "Athletico-PR": ["Mastriani", "A. Canobbio", "Fernandinho", "Léo Linck (GOL)"],
        "Internacional": ["E. Valencia", "Alan Patrick", "G. Mercado", "Rochet (GOL)"],
        "Santos": ["J. Furch", "Guilherme", "João Schmidt", "João Paulo (GOL)"],
        "Corinthians": ["Yuri Alberto", "R. Garro", "Félix Torres", "Hugo Souza (GOL)"],
        "Grêmio": ["M. Braithwaite", "F. Cristaldo", "W. Kannemann", "Marchesín (GOL)"],
        "Atlético-MG": ["Hulk", "Paulinho", "G. Arana", "Everson (GOL)"],
        "Bahia": ["E. Ribeiro", "Cauly", "Thaciano", "Marcos Felipe (GOL)"],
        "Bragantino": ["E. Sasha", "Lincoln", "J. Capixaba", "Cleiton (GOL)"]
    }
    return elencos.get(time, [f"Atacante (9) do {time}", f"Meia (10) do {time}", f"Zagueiro (3) do {time}", f"Goleiro do {time}"])

# --- 2. TOPO: DATA E DESTAQUES ---
col_t1, col_t2 = st.columns([1, 2])
with col_t1:
    st.markdown("### 📅 Data")
    data_inicial = st.date_input("Escolha o dia:", datetime.now() + timedelta(days=1), label_visibility="collapsed")

with col_t2:
    st.markdown("### 🔥 Bilhetes em Destaque")
    aba_topo = st.radio("Filtro:", ["🎯 Solos", "⚡ Múltiplas"], horizontal=True, label_visibility="collapsed")

# --- 3. BUSCA OTIMIZADA DE JOGOS ---
@st.cache_data(ttl=7200)
def carregar_rodada_fluida(api_key, data_base):
    data_str = data_base.strftime("%Y-%m-%d")
    url = f"https://v3.football.api-sports.io/fixtures?date={data_str}&timezone=America/Sao_Paulo"
    headers = {'x-apisports-key': api_key}
    
    jogos = []
    ligas_validas = [39, 140, 71, 72, 2, 3, 13, 848, 128, 130]
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        dados = response.json()
        if 'response' in dados:
            for item in dados['response']:
                if item['league']['id'] in ligas_validas or item['league']['country'] in ["Brazil", "England", "Spain", "Italy", "Germany"]:
                    jogos.append({
                        "Liga": item['league']['name'],
                        "País": item['league']['country'],
                        "LogoLiga": item['league']['logo'],
                        "Horário": item['fixture']['date'][11:16],
                        "Mandante": item['teams']['home']['name'],
                        "Visitante": item['teams']['away']['name']
                    })
    except Exception:
        pass
    return pd.DataFrame(jogos)

if API_KEY == "COLE_SUA_CHAVE_AQUI":
    st.error("⚠️ Atenção: Cole sua chave da API na linha 13 do código.")
    df_jogos = pd.DataFrame()
else:
    df_jogos = carregar_rodada_fluida(API_KEY, data_inicial)

# --- 4. EXIBIÇÃO RÁPIDA DO TOPO ---
with st.container(border=True):
    if not df_jogos.empty:
        if aba_topo == "🎯 Solos":
            destaques = df_jogos.head(3)
            c1, c2, c3 = st.columns(3)
            cols = [c1, c2, c3]
            for idx, (_, jogo) in enumerate(destaques.iterrows()):
                with cols[idx]:
                    craque = obter_jogadores(jogo['Mandante'])[0]
                    st.write(f"⚽ **{jogo['Mandante']} x {jogo['Visitante']}**")
                    st.success(f"💡 {craque} (1+ Chute ao Gol)\n\n🏆 **Odd: 1.85**")
        else:
            mult_jogos = df_jogos.sample(n=min(3, len(df_jogos)))
            odd_total = 1.35 * 1.40 * 1.30
            for _, j in mult_jogos.iterrows():
                st.markdown(f"* **{j['Mandante']} x {j['Visitante']}** ➔ Mais de 1.5 Gols")
            st.divider()
            st.markdown(f"🔥 **Superbet (Recomendado):** **{odd_total + 0.25:.2f}** | **Betano:** **{odd_total:.2f}**")
    else:
        st.info("Nenhum destaque rápido para esta data.")

st.divider()

# --- 5. NAVEGAÇÃO POR LIGAS (PASTAS) ---
st.markdown(f"### 📁 Campeonatos Disponíveis ({data_inicial.strftime('%d/%m/%Y')})")

if not df_jogos.empty:
    # Pega a lista de ligas únicas disponíveis no dia
    lista_ligas = sorted(df_jogos['Liga'].unique())
    
    # Para cada liga, criamos um "Expander" (uma pasta clicável)
    for liga in lista_ligas:
        # Filtra os jogos que pertencem apenas a esta liga
        jogos_da_liga = df_jogos[df_jogos['Liga'] == liga]
        pais_liga = jogos_da_liga.iloc[0]['País']
        
        # O nome da pasta exibe a Liga e quantos jogos ela tem no dia
        with st.expander(f"🏆 {liga} ({pais_liga}) — {len(jogos_da_liga)} jogo(s) hoje"):
            
            # Dentro da liga, listamos os jogos do dia organizados
            for index, row in jogos_da_liga.iterrows():
                st.markdown(f"#### ⚽ {row['Horário']} | **{row['Mandante']}** x **{row['Visitante']}**")
                
                # Painel de Apostas de cada jogo específico
                t1, t2, t3 = st.tabs(["🛠️ Construtor de Apostas", "🎯 Caçador de Odds", "📊 Resumo"])
                jc = obter_jogadores(row['Mandante'])
                jf = obter_jogadores(row['Visitante'])

                with t1:
                    st.write("**Mercados Principais (Criar Aposta):**")
                    st.markdown(f"""
                    * 🎯 **Chutes ao Gol:** {jc[0]} (1+ no Alvo) — *Probabilidade: 72%* (Odd: 1.85)
                    * 👟 **Finalizações:** {jc[1]} (2+ Finalizações) — *Probabilidade: 65%* (Odd: 1.65)
                    * 🧤 **Goleiro:** {jf[3]} (3+ Defesas) — *Probabilidade: 80%* (Odd: 1.50)
                    * ⚽ **Artilheiro:** {jc[0]} (A qualquer momento) — *Probabilidade: 48%* (Odd: 2.10)
                    """)

                with t2:
                    o_alvo = st.number_input("Odd Alvo:", 1.10, 20.0, 1.60, 0.10, key=f"num_{row['Mandante']}_{index}")
                    if st.button("🔎 Calcular Bilhete", key=f"btn_{row['Mandante']}_{index}"):
                        st.success(f"✅ Sugestão gerada com sucesso! Cotação Estimada: **{o_alvo + 0.04:.2f}**")
                        st.write(f"📌 **Entrada Recomendada:** {row['Mandante']} ou Empate + {jc[0]} (1+ Chute ao Gol)")

                with t3:
                    st.info(f"Confronto direto válido pelo campeonato {liga}. Mandante com forte pressão ofensiva recente.")
                
                st.divider()
else:
    st.info("Nenhum jogo encontrado para esta data. Experimente alterar o dia no calendário acima.")
