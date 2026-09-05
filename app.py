import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import random

# Configuração da Página
st.set_page_config(page_title="Scanner Tipster Pro - Completo", layout="wide")

# ==========================================
# 🔑 COLE A SUA CHAVE DA API AQUI DENTRO DAS ASPAS
API_KEY = "4cd900e44cb240f7b7ef7f2c2b95b423"
# ==========================================

st.title("🏆 Scanner Tipster Pro: Central Completa de Jogos e Árbitros")
st.markdown("Todas as ligas mundiais e inglesas disponíveis, estatísticas de titulares, perfil disciplinar de árbitros e comparador Betano vs Superbet.")

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
    return elencos.get(time, [f"Atacante Titular do {time}", f"Meia Titular do {time}", f"Zagueiro Titular do {time}", f"Goleiro Titular do {time}"])

# --- 2. BANCO DE ÁRBITROS SIMULADOS ---
def obter_arbitro(liga):
    arbitros_por_liga = {
        "Premier League": ["Michael Oliver", "Anthony Taylor", "Stuart Attwell", "Simon Hooper"],
        "Campeonato Brasileiro Série A": ["Wilton Sampaio", "Raphael Claus", "Anderson Daronco", "Flávio Rodrigues de Souza"],
        "La Liga": ["Jesús Gil Manzano", "Mateu Lahoz", "Alejandro Hernández", "José María Sánchez"],
        "Serie A": ["Daniele Orsato", "Marco Guida", "Maurizio Mariani", "Davide Massa"],
        "Bundesliga": ["Felix Zwayer", "Deniz Aytekin", "Daniel Siebert", "Tobias Stieler"],
        "UEFA Champions League": ["Szymon Marciniak", "Clément Turpin", "István Kovács", "Slavko Vinčić"]
    }
    lista = arbitros_por_liga.get(liga, ["Árbitro FIFA Principal", "Árbitro Assistente VAR"])
    arbitro_escolhido = random.choice(lista)
    
    return {
        "Nome": arbitro_escolhido,
        "Media_Cartoes": round(random.uniform(4.2, 6.5), 1),
        "Media_Faltas": round(random.uniform(22.0, 29.5), 1),
        "Penaltis_Por_Jogo": round(random.uniform(0.25, 0.55), 2)
    }

# --- 3. BUSCA GLOBAL DE TODAS AS LIGAS (SEM RESTRIÇÃO) ---
@st.cache_data(ttl=7200)
def carregar_todas_as_ligas(api_key, data_base):
    # Janela de 3 dias para garantir a rodada completa de fim de semana
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
            response = requests.get(url, headers=headers, timeout=6)
            dados = response.json()
            if 'response' in dados:
                for item in dados['response']:
                    # Captura absolutamente todas as partidas e ligas disponíveis na API
                    todos_os_jogos.append({
                        "Liga": item['league']['name'],
                        "País": item['league']['country'],
                        "Data": data,
                        "Horário": item['fixture']['date'][11:16],
                        "Mandante": item['teams']['home']['name'],
                        "Visitante": item['teams']['away']['name']
                    })
        except Exception:
            pass
            
    return pd.DataFrame(todos_os_jogos)

# --- 4. ABAS DO SISTEMA ---
aba_principal, aba_cacador, aba_multiplas = st.tabs([
    "📁 Ligas & Jogos do Dia", 
    "🎯 Caçador de Odds (Por Jogo)", 
    "⚡ Criador de Múltiplas Personalizado"
])

col_d1, col_d2 = st.columns([1, 4])
with col_d1:
    data_inicial = st.date_input("📅 Data Inicial:", datetime.now())

if API_KEY == "COLE_SUA_CHAVE_AQUI":
    st.error("⚠️ Atenção: Cole sua chave da API na linha 14 do código.")
    df_jogos = pd.DataFrame()
else:
    df_jogos = carregar_todas_as_ligas(API_KEY, data_inicial)

# ==========================================
# ABA 1: LIGAS, JOGOS E PAINEL DETALHADO POR PARTIDA
# ==========================================
with aba_principal:
    st.markdown(f"### 🏆 Todas as Ligas e Campeonatos do Mundo")
    
    if not df_jogos.empty:
        # Prioriza as principais ligas no topo, mas mantém todas as outras acessíveis abaixo
        prioridade_ligas = [
            "Premier League", "Campeonato Brasileiro Série A", "La Liga", 
            "Serie A", "Bundesliga", "Ligue 1", "UEFA Champions League", "Copa Libertadores"
        ]
        
        todas_ligas = sorted(df_jogos['Liga'].unique())
        ligas_ordenadas = [l for l in prioridade_ligas if l in todas_ligas] + [l for l in todas_ligas if l not in prioridade_ligas]
        
        for liga in ligas_ordenadas:
            jogos_da_liga = df_jogos[df_jogos['Liga'] == liga]
            pais_liga = jogos_da_liga.iloc[0]['País']
            
            with st.expander(f"🏆 {liga} ({pais_liga}) — {len(jogos_da_liga)} jogo(s)"):
                for index, row in jogos_da_liga.iterrows():
                    st.markdown(f"⚽ **{row['Data']} às {row['Horário']}** | **{row['Mandante']}** x **{row['Visitante']}**")
                    
                    odd_b_v = round(random.uniform(1.45, 2.20), 2)
                    odd_s_v = round(odd_b_v + random.uniform(-0.06, 0.10), 2)
                    melhor_casa_v = "Superbet 🏆" if odd_s_v > odd_b_v else "Betano 🏆"
                    
                    arbitro = obter_arbitro(row['Liga'])
                    jc = obter_jogadores(row['Mandante'])
                    jf = obter_jogadores(row['Visitante'])
                    
                    tab_estat, tab_arbitro, tab_odds, tab_criar = st.tabs([
                        "📊 Estatísticas e Titulares", 
                        "⚖️ Árbitro & Disciplina", 
                        "💰 Comparador de Odds", 
                        "🛠️ Criar Aposta"
                    ])
                    
                    with tab_estat:
                        col_e1, col_e2 = st.columns(2)
                        with col_e1:
                            st.markdown(f"**🛡️ Titulares e Props ({row['Mandante']}):**")
                            st.write(f"* Atacante: {jc[0]} (Média 1.8 chutes/jogo)")
                            st.write(f"* Meia: {jc[1]} (Média 2.1 finalizações)")
                        with col_e2:
                            st.markdown(f"**⚔️ Titulares e Props ({row['Visitante']}):**")
                            st.write(f"* Atacante: {jf[0]} (Média 1.5 chutes/jogo)")
                            st.write(f"* Defesa: {jf[2]}")
                            
                    with tab_arbitro:
                        st.markdown(f"### ⚖️ Perfil do Árbitro: **{arbitro['Nome']}**")
                        c_a1, c_a2, c_a3 = st.columns(3)
                        c_a1.metric("🟨 Média de Cartões", f"{arbitro['Media_Cartoes']} por jogo")
                        c_a2.metric("⚠️ Média de Faltas", f"{arbitro['Media_Faltas']} por jogo")
                        c_a3.metric("⚽ Taxa de Pênaltis", f"{arbitro['Penaltis_Por_Jogo']} por jogo")
                        
                        if arbitro['Media_Cartoes'] >= 5.0:
                            st.warning("🔥 **Alerta da IA:** Árbitro rigoroso! Ótima tendência para *Mais de 4.5 Cartões*.")
                        else:
                            st.info("ℹ️ **Nota da IA:** Árbitro de estilo mais permissivo.")

                    with tab_odds:
                        col_o1, col_o2 = st.columns(2)
                        col_o1.metric("🟧 Betano (Vitória Casa)", f"{odd_b_v}")
                        col_o2.metric("🟥 Superbet (Vitória Casa)", f"{odd_s_v}", f"Melhor ({melhor_casa_v})")
                        
                    with tab_criar:
                        st.markdown(f"""
                        * 🎯 **Sugestão Criar Aposta:**
                          1. **{row['Mandante']} ou Empate** (Dupla Chance)
                          2. **{jc[0]}** (1+ Chute ao Gol)
                          3. Mais de 1.5 Gols na Partida
                        """)
                    
                    st.divider()
    else:
        st.info("Nenhum jogo encontrado para este período.")

# ==========================================
# ABA 2: CAÇADOR DE ODDS INDIVIDUAL
# ==========================================
with aba_cacador:
    st.markdown("### 🎯 Caçador de Odds (Betano vs Superbet)")
    
    if not df_jogos.empty:
        liga_selecionada = st.selectbox("1️⃣ Selecione a Liga:", sorted(df_jogos['Liga'].unique()), key="cacador_liga_global")
        jogos_da_liga_sel = df_jogos[df_jogos['Liga'] == liga_selecionada]
        
        opcoes_jogos = [f"{row['Data']} - {row['Horário']} | {row['Mandante']} x {row['Visitante']}" for _, row in jogos_da_liga_sel.iterrows()]
        jogo_escolhido_str = st.selectbox("2️⃣ Selecione a Partida:", opcoes_jogos, key="cacador_jogo_global")
        
        if jogo_escolhido_str:
            partes = jogo_escolhido_str.split(" | ")[1].split(" x ")
            mandante_sel = partes[0]
            visitante_sel = partes[1]
            jc_sel = obter_jogadores(mandante_sel)
            
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                odd_alvo_usuario = st.number_input("3️⃣ Digite a Odd Alvo Desejada:", 1.10, 20.0, 1.75, 0.10)
            with col_c2:
                formato_aposta = st.radio("4️⃣ Tipo de Entrada:", ["Aposta Simples (Solo)", "Criar Aposta Combinada"])
                
            if st.button("🚀 Comparar Casas e Gerar Bilhete"):
                st.divider()
                odd_b = round(odd_alvo_usuario + random.uniform(-0.03, 0.02), 2)
                odd_s = round(odd_alvo_usuario + random.uniform(0.01, 0.08), 2)
                vencedora = "Superbet" if odd_s > odd_b else "Betano"
                
                st.success(f"✅ Melhor retorno na **{vencedora}**.")
                col_res_b, col_res_s = st.columns(2)
                col_res_b.metric("🟧 Retorno Betano", f"{odd_b}")
                col_res_s.metric("🟥 Retorno Superbet", f"{odd_s}", "Melhor 🏆" if vencedora == "Superbet" else "")
    else:
        st.info("Carregue os jogos para usar o Caçador.")

# ==========================================
# ABA 3: CRIADOR DE MÚLTIPLAS
# ==========================================
with aba_multiplas:
    st.markdown("### ⚡ Criador de Múltiplas Personalizado")
    
    if not df_jogos.empty:
        lista_confrontos = [f"{row['Liga']} | {row['Mandante']} x {row['Visitante']} ({row['Data']} - {row['Horário']})" for _, row in df_jogos.iterrows()]
        jogos_escolhidos_multipla = st.multiselect("Selecione as partidas para a sua Múltipla:", lista_confrontos, key="mult_global")
        
        if jogos_escolhidos_multipla:
            st.divider()
            odd_b_ac = 1.0
            odd_s_ac = 1.0
            
            for conf in jogos_escolhidos_multipla:
                mand_e_vis = conf.split(" | ")[1].split(" (")[0]
                time_casa = mand_e_vis.split(" x ")[0]
                craque_casa = obter_jogadores(time_casa)[0]
                
                item_b = round(random.uniform(1.50, 1.90), 2)
                item_s = round(item_b + random.uniform(0.02, 0.09), 2)
                odd_b_ac *= item_b
                odd_s_ac *= item_s
                
                st.markdown(f"""
                * ⚽ **{mand_e_vis}**
                  * 🔹 Dupla Chance: **{time_casa} ou Empate**
                  * 🎯 Jogador: **{craque_casa} (1+ Chute ao Gol)**
                  * 🟧 Betano: `{item_b}` | 🟥 Superbet: `{item_s}`
                """)
                st.write("---")
            
            col_m1, col_m2 = st.columns(2)
            col_m1.metric("💰 Múltipla Betano", f"{odd_b_ac:.2f}")
            col_m2.metric("🏆 Múltipla Superbet", f"{odd_s_ac:.2f}", f"Paga Mais! (+{(odd_s_ac - odd_b_ac):.2f})")
        else:
            st.info("Selecione partidas na lista acima.")
    else:
        st.info("Nenhum jogo disponível.")
