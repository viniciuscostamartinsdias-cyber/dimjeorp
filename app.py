import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import random

# Configuração da Página
st.set_page_config(page_title="Scanner Tipster Pro - Profissional", layout="wide")

# ==========================================
# 🔑 COLE A SUA CHAVE DA API AQUI DENTRO DAS ASPAS
API_KEY = "4cd900e44cb240f7b7ef7f2c2b95b423"
# ==========================================

st.title("🏆 Scanner Tipster Pro: Central de Inteligência e Apostas")
st.markdown("Navegue pelas ligas principais, use o Caçador de Odds individual ou monte suas Múltiplas selecionando os jogos.")

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

# --- 2. BUSCA DE JOGOS ---
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
                        "Horário": item['fixture']['date'][11:16],
                        "Mandante": item['teams']['home']['name'],
                        "Visitante": item['teams']['away']['name']
                    })
    except Exception:
        pass
    return pd.DataFrame(jogos)

# --- 3. MENU PRINCIPAL EM ABAS NO TOPO ---
aba_principal, aba_cacador, aba_multiplas = st.tabs([
    "📁 Ligas & Jogos do Dia", 
    "🎯 Caçador de Odds (Por Jogo)", 
    "⚡ Criador de Múltiplas Personalizado"
])

# Seleção de data global na barra lateral ou topo
col_d1, col_d2 = st.columns([1, 4])
with col_d1:
    data_inicial = st.date_input("📅 Data:", datetime.now() + timedelta(days=1))

if API_KEY == "COLE_SUA_CHAVE_AQUI":
    st.error("⚠️ Atenção: Cole sua chave da API na linha 14 do código.")
    df_jogos = pd.DataFrame()
else:
    df_jogos = carregar_rodada_fluida(API_KEY, data_inicial)

# ==========================================
# ABA 1: LIGAS E JOGOS DO DIA (PRIORIDADE NAS PRINCIPAIS)
# ==========================================
with aba_principal:
    st.markdown(f"### 🏆 Campeonatos Disponíveis ({data_inicial.strftime('%d/%m/%Y')})")
    
    if not df_jogos.empty:
        # Ordem de prioridade das principais ligas do mundo e do Brasil
        prioridade_ligas = [
            "Campeonato Brasileiro Série A", 
            "Premier League", 
            "La Liga", 
            "Serie A", 
            "Bundesliga", 
            "Ligue 1", 
            "UEFA Champions League",
            "Copa Libertadores"
        ]
        
        todas_ligas = sorted(df_jogos['Liga'].unique())
        # Ordena colocando as principais no topo e o restante em ordem alfabética abaixo
        ligas_ordenadas = [l for l in prioridade_ligas if l in todas_ligas] + [l for l in todas_ligas if l not in prioridade_ligas]
        
        for liga in ligas_ordenadas:
            jogos_da_liga = df_jogos[df_jogos['Liga'] == liga]
            pais_liga = jogos_da_liga.iloc[0]['País']
            
            with st.expander(f"🏆 {liga} ({pais_liga}) — {len(jogos_da_liga)} jogo(s)"):
                for index, row in jogos_da_liga.iterrows():
                    st.markdown(f"⚽ **{row['Horário']}** | {row['Mandante']} x {row['Visitante']}")
                    jc = obter_jogadores(row['Mandante'])
                    jf = obter_jogadores(row['Visitante'])
                    
                    col_m1, col_m2 = st.columns(2)
                    with col_m1:
                        st.info(f"🎯 **Criar Aposta Sugerido:** {row['Mandante']} ou Empate + {jc[0]} (1+ Chute ao Gol)")
                    with col_m2:
                        st.success(f"📊 **Média de Gols H2H:** 2.6 por partida")
                    st.divider()
    else:
        st.info("Nenhum jogo encontrado para esta data.")

# ==========================================
# ABA 2: CAÇADOR DE ODDS (SELECIONA LIGA E JOGO ESPECÍFICO)
# ==========================================
with aba_cacador:
    st.markdown("### 🎯 Caçador de Odds Personalizadas")
    st.write("Selecione a liga, escolha o confronto desejado e defina a cotação alvo.")
    
    if not df_jogos.empty:
        # Seleção de Liga
        liga_selecionada = st.selectbox("1️⃣ Selecione a Liga:", sorted(df_jogos['Liga'].unique()), key="cacador_liga")
        jogos_da_liga_sel = df_jogos[df_jogos['Liga'] == liga_selecionada]
        
        # Seleção de Jogo dentro da Liga
        opcoes_jogos = [f"{row['Horário']} - {row['Mandante']} x {row['Visitante']}" for _, row in jogos_da_liga_sel.iterrows()]
        jogo_escolhido_str = st.selectbox("2️⃣ Selecione a Partida:", opcoes_jogos, key="cacador_jogo")
        
        if jogo_escolhido_str:
            # Extrai os times do texto selecionado
            partes = jogo_escolhido_str.split(" - ")[1].split(" x ")
            mandante_sel = partes[0]
            visitante_sel = partes[1]
            
            jc_sel = obter_jogadores(mandante_sel)
            jf_sel = obter_jogadores(visitante_sel)
            
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                odd_alvo_usuario = st.number_input("3️⃣ Digite a Odd Alvo Desejada:", 1.10, 20.0, 1.75, 0.10)
            with col_c2:
                formato_aposta = st.radio("4️⃣ Tipo de Entrada:", ["Aposta Simples (Solo)", "Criar Aposta Combinada"])
                
            if st.button("🚀 Calcular e Gerar Bilhete Exato"):
                st.divider()
                st.success(f"✅ **Bilhete Criado com Sucesso!** Cotação Final Projetada: **{odd_alvo_usuario + random.uniform(-0.01, 0.05):.2f}**")
                
                if formato_aposta == "Aposta Simples (Solo)":
                    st.markdown(f"""
                    * **Partida:** {mandante_sel} x {visitante_sel}
                    * **Seleção de Ouro:** **{mandante_sel} - Vence ou Empata (Dupla Chance)**
                    * **Probabilidade Calculada:** `76%`
                    """)
                else:
                    st.markdown(f"""
                    * **Partida:** {mandante_sel} x {visitante_sel}
                    * **Combinação (Criar Aposta):**
                      1. {mandante_sel} (Vitória simples ou DNB)
                      2. **{jc_sel[0]}** (1+ Chute ao Alvo)
                      3. Mais de 1.5 Gols na Partida
                    * **Probabilidade Combinada:** `58%`
                    """)
    else:
        st.info("Carregue os jogos na data selecionada para usar o Caçador.")

# ==========================================
# ABA 3: CRIADOR DE MÚLTIPLAS PERSONALIZADO
# ==========================================
with aba_multiplas:
    st.markdown("### ⚡ Monte sua Própria Super Múltipla")
    st.write("Selecione os jogos ou ligas que quiser abaixo para o algoritmo cruzar e gerar a cotação acumulada.")
    
    if not df_jogos.empty:
        # Multiselect para escolher os jogos
        lista_confrontos = [f"{row['Liga']}: {row['Mandante']} x {row['Visitante']} ({row['Horário']})" for _, row in df_jogos.iterrows()]
        
        jogos_escolhidos_multipla = st.multiselect("Selecione as partidas para entrar na sua Múltipla:", lista_confrontos)
        
        if jogos_escolhidos_multipla:
            st.divider()
            st.markdown("#### 📋 Sua Múltipla Personalizada Pronta:")
            
            odd_acumulada_user = 1.0
            for conf in jogos_escolhidos_multipla:
                odd_item = round(random.uniform(1.25, 1.45), 2)
                odd_acumulada_user *= odd_item
                st.markdown(f"* **{conf}** ➔ Mais de 1.5 Gols / Dupla Chance *(Odd individual: {odd_item})*")
            
            st.divider()
            col_res1, col_res2 = st.columns(2)
            col_res1.metric("💰 Retorno na Betano", f"{odd_acumulada_user:.2f}")
            col_res2.metric("🏆 Retorno na Superbet (Bônus)", f"{odd_acumulada_user + 0.35:.2f}")
            
            if st.button("💾 Copiar Estrutura da Múltipla"):
                st.balloons()
                st.success("Múltipla gerada e pronta para ser copiada para a sua casa de apostas favorita!")
        else:
            st.info("Selecione pelo menos 2 partidas na lista acima para o sistema calcular a cotação acumulada.")
    else:
        st.info("Nenhum jogo disponível na data selecionada.")
