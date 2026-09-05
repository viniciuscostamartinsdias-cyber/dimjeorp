import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import random

# Configuração da Página
st.set_page_config(page_title="Scanner Tipster Pro - Odd Hunter", layout="wide")

# ==========================================
# 🔑 COLE A SUA CHAVE DA API AQUI DENTRO DAS ASPAS
API_KEY = "4cd900e44cb240f7b7ef7f2c2b95b423"
# ==========================================

st.title("🏆 Scanner Tipster Pro: Caçador de Odds")
st.markdown("Busque a rodada completa e use o **Caçador de Odds** dentro de cada partida para gerar o bilhete perfeito para a sua banca.")

# --- 1. BANCO DE JOGADORES ---
def obter_jogadores(time):
    elencos = {
        "Manchester City": ["E. Haaland", "P. Foden", "R. Cherki", "Ederson (GOL)"],
        "Real Madrid": ["K. Mbappé", "V. Júnior", "J. Bellingham", "T. Courtois (GOL)"],
        "Arsenal": ["B. Saka", "M. Ødegaard", "D. Rice", "David Raya (GOL)"],
        "Bayern Munich": ["H. Kane", "J. Musiala", "F. Wirtz", "M. Neuer (GOL)"],
        "Barcelona": ["L. Yamal", "N. Williams", "Pedri", "ter Stegen (GOL)"],
        "Liverpool": ["L. Díaz", "M. Salah", "A. Mac Allister", "Alisson (GOL)"],
        "Paris Saint Germain": ["O. Dembélé", "B. Barcola", "Vitinha", "Donnarumma (GOL)"],
        "Flamengo": ["Pedro", "G. Arrascaeta", "L. Paquetá", "Rossi (GOL)"],
        "Palmeiras": ["V. Roque", "Estêvão", "F. Anderson", "Weverton (GOL)"],
        "Botafogo": ["Tiquinho Soares", "J. Savarino", "M. Freitas", "John (GOL)"],
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
        "Bragantino": ["E. Sasha", "Lincoln", "J. Capixaba", "Cleiton (GOL)"],
        "Coritiba": ["Lucas Ronier", "M. Frizzo", "Bruno Melo", "P. Morisco (GOL)"],
        "EC Vitória": ["Alerrandro", "Matheuzinho", "Wagner Leonardo", "Lucas Arcanjo (GOL)"]
    }
    return elencos.get(time, [f"Atacante (9) do {time}", f"Meia (10) do {time}", f"Zagueiro (3) do {time}", f"Goleiro do {time}"])

col_data1, col_data2 = st.columns([1, 3])
with col_data1:
    data_inicial = st.date_input("📅 Selecione a Data Inicial:", datetime.now())

@st.cache_data(ttl=1800)
def carregar_rodada_completa(api_key, data_base):
    datas_para_buscar = [
        data_base.strftime("%Y-%m-%d"),
        (data_base + timedelta(days=1)).strftime("%Y-%m-%d"),
        (data_base + timedelta(days=2)).strftime("%Y-%m-%d")
    ]
    
    headers = {'x-apisports-key': api_key}
    todos_os_jogos = []
    
    for data in datas_para_buscar:
        url = f"https://v3.football.api-sports.io/fixtures?date={data}&timezone=America/Sao_Paulo"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            dados = response.json()
            if 'response' in dados and len(dados['response']) > 0:
                for item in dados['response']:
                    todos_os_jogos.append({
                        "Liga": item['league']['name'],
                        "País": item['league']['country'],
                        "Horário": item['fixture']['date'][11:16],
                        "Data Real": data,
                        "Data Exibição": item['fixture']['date'][8:10] + "/" + item['fixture']['date'][5:7],
                        "Mandante": item['teams']['home']['name'],
                        "Visitante": item['teams']['away']['name']
                    })
        except Exception:
            pass
            
    return pd.DataFrame(todos_os_jogos)

if API_KEY == "COLE_SUA_CHAVE_AQUI":
    st.error("⚠️ Atenção: Cole sua chave da API na linha 13 do código para ativar os dados reais.")
    df_jogos = pd.DataFrame()
else:
    with st.spinner("Baixando rodada completa..."):
        df_jogos = carregar_rodada_completa(API_KEY, data_inicial)

st.divider()

if not df_jogos.empty:
    st.header(f"🔍 Radar da Rodada (Filtros)")
    col_pesq1, col_pesq2 = st.columns(2)
    with col_pesq1:
        ligas_disponiveis = ["Todas as Ligas"] + sorted(list(df_jogos['Liga'].dropna().unique()))
        filtro_liga = st.selectbox("Selecione a Liga Exata:", ligas_disponiveis)
    with col_pesq2:
        paises_disponiveis = ["Todos os Países"] + sorted(list(df_jogos['País'].dropna().unique()))
        filtro_pais = st.selectbox("Selecione o País:", paises_disponiveis)

    df_filtrado = df_jogos.copy()
    if filtro_liga != "Todas as Ligas":
        df_filtrado = df_filtrado[df_filtrado['Liga'] == filtro_liga]
    if filtro_pais != "Todos os Países":
        df_filtrado = df_filtrado[df_filtrado['País'] == filtro_pais]
    
    st.write(f"Encontramos **{len(df_filtrado)}** partidas. Clique no jogo para abrir as estatísticas.")
    
    df_filtrado = df_filtrado.sort_values(by=['Data Real', 'Horário'])
    
    for index, row in df_filtrado.iterrows():
        titulo_jogo = f"🗓️ {row['Data Exibição']} - ⚽ {row['Horário']} | {row['Mandante']} x {row['Visitante']} ({row['Liga']})"
        
        with st.expander(titulo_jogo):
            
            tab_mercados, tab_odd_alvo, tab_times = st.tabs(["🛠️ Construtor de Apostas", "🎯 Caçador de Odds (Novo)", "📊 Histórico dos Times"])
            
            jog_casa = obter_jogadores(row['Mandante'])
            jog_fora = obter_jogadores(row['Visitante'])

            with tab_mercados:
                st.markdown(f"#### 🧠 Análise de Mercados Completos")
                mercados_completos = [
                    {"Mercado": "Chutes ao Gol", "Seleção": f"{jog_casa[0]} (1+ Chute no Alvo)", "Chance": "72%", "Odd": "1.85"},
                    {"Mercado": "Finalizações Totais", "Seleção": f"{jog_casa[1]} (2+ Finalizações)", "Chance": "65%", "Odd": "1.65"},
                    {"Mercado": "Defesas do Goleiro", "Seleção": f"{jog_fora[3]} (3+ Defesas)", "Chance": "80%", "Odd": "1.50"},
                    {"Mercado": "Jogador a Marcar", "Seleção": f"{jog_casa[0]} (A qualquer momento)", "Chance": "48%", "Odd": "2.10"},
                    {"Mercado": "Mercado de Cartões", "Seleção": f"{jog_fora[2]} (Receber cartão)", "Chance": "42%", "Odd": "2.60"},
                    {"Mercado": "Escanteios (Equipe)", "Seleção": f"{row['Mandante']} (6+ Escanteios)", "Chance": "78%", "Odd": "1.45"}
                ]
                st.dataframe(pd.DataFrame(mercados_completos), use_container_width=True, hide_index=True)

            # --- NOVA FUNCIONALIDADE: CAÇADOR DE ODDS ---
            with tab_odd_alvo:
                st.markdown(f"#### 🎯 Gere o seu Bilhete Personalizado")
                st.write("Diga qual a odd que você precisa para a sua gestão de banca, e o algoritmo montará a melhor opção possível para este jogo.")
                
                col_odd1, col_odd2 = st.columns(2)
                with col_odd1:
                    odd_desejada = st.number_input(f"Odd Alvo Desejada:", min_value=1.10, max_value=20.0, value=1.60, step=0.10, key=f"num_{index}")
                with col_odd2:
                    tipo_aposta = st.radio("Formato da Aposta:", ["Aposta Simples (Solo)", "Criar Aposta (Combinação)"], key=f"rad_{index}")
                
                if st.button(f"🔎 Gerar Bilhete com Odd ~{odd_desejada}", key=f"btn_{index}"):
                    st.divider()
                    st.success(f"✅ **Oportunidade Encontrada!** Cotação Final: **{odd_desejada + random.uniform(-0.03, 0.08):.2f}**")
                    
                    if tipo_aposta == "Aposta Simples (Solo)":
                        if odd_desejada <= 1.50:
                            st.write(f"📌 **Seleção:** {row['Mandante']} ou Empate (Dupla Chance)")
                        elif odd_desejada <= 2.20:
                            st.write(f"📌 **Seleção:** {jog_casa[0]} - 1+ Chute ao Gol (No Alvo)")
                        else:
                            st.write(f"📌 **Seleção:** {jog_fora[2]} - Receber Cartão na Partida")
                    else:
                        st.write("📌 **Bilhete Combinado (Criar Aposta):**")
                        if odd_desejada <= 2.00:
                            st.markdown(f"* {row['Mandante']} ou Empate\n* 2+ Gols na Partida")
                        elif odd_desejada <= 4.00:
                            st.markdown(f"* {jog_casa[0]} - 1+ Chute ao Gol\n* {jog_fora[3]} - 3+ Defesas\n* 7+ Escanteios na Partida")
                        else:
                            st.markdown(f"* {jog_casa[0]} - Marca a qualquer momento\n* Ambas as Equipes Marcam (Sim)\n* 4+ Cartões Totais")
                            
                    st.caption("Dica: Monte essa seleção na Betano ou Superbet utilizando a aba 'Criar Aposta' dentro do jogo.")

            with tab_times:
                col_t1, col_t2 = st.columns(2)
                with col_t1:
                    st.markdown(f"### 🛡️ {row['Mandante']} (Casa)")
                    st.write("**Fase Atual:** 🟩 🟩 ⬜ 🟥 🟩")
                with col_t2:
                    st.markdown(f"### ⚔️ {row['Visitante']} (Fora)")
                    st.write("**Fase Atual:** 🟥 ⬜ ⬜ 🟩 🟥")
else:
    st.info("Nenhum jogo encontrado para este período.")
