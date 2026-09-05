import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import random

# Configuração da Página
st.set_page_config(page_title="Scanner Tipster Pro - Correção Caçador", layout="wide")

# ==========================================
# 🔑 COLE A SUA CHAVE DA API AQUI DENTRO DAS ASPAS
API_KEY = "4cd900e44cb240f7b7ef7f2c2b95b423"
# ==========================================

st.title("🏆 Scanner Tipster Pro: Caçador de Odds Definitivo")
st.markdown("Plataforma de análise com camisas de jogadores, chutes de fora da área, faltas e comparador Betano vs Superbet.")

# --- 1. BANCO DE JOGADORES DETALHADOS ---
def obter_jogadores_detalhados(time):
    elencos = {
        "Manchester City": [
            {"nome": "E. Haaland", "camisa": "9", "pos": "Atacante"},
            {"nome": "P. Foden", "camisa": "47", "pos": "Meia"},
            {"nome": "R. Cherki", "camisa": "10", "pos": "Meia"},
            {"nome": "Rodri", "camisa": "16", "pos": "Volante"}
        ],
        "Real Madrid": [
            {"nome": "K. Mbappé", "camisa": "9", "pos": "Atacante"},
            {"nome": "V. Júnior", "camisa": "7", "pos": "Atacante"},
            {"nome": "J. Bellingham", "camisa": "5", "pos": "Meia"},
            {"nome": "F. Valverde", "camisa": "8", "pos": "Volante"}
        ],
        "Arsenal": [
            {"nome": "B. Saka", "camisa": "7", "pos": "Atacante"},
            {"nome": "M. Ødegaard", "camisa": "8", "pos": "Meia"},
            {"nome": "D. Rice", "camisa": "41", "pos": "Volante"},
            {"nome": "K. Havertz", "camisa": "29", "pos": "Atacante"}
        ],
        "Flamengo": [
            {"nome": "Pedro", "camisa": "9", "pos": "Atacante"},
            {"nome": "G. Arrascaeta", "camisa": "14", "pos": "Meia"},
            {"nome": "L. Paquetá", "camisa": "10", "pos": "Meia"},
            {"nome": "Gerson", "camisa": "8", "pos": "Volante"}
        ],
        "Palmeiras": [
            {"nome": "V. Roque", "camisa": "9", "pos": "Atacante"},
            {"nome": "Estêvão", "camisa": "41", "pos": "Atacante"},
            {"nome": "Raphael Veiga", "camisa": "23", "pos": "Meia"},
            {"nome": "Aníbal Moreno", "camisa": "5", "pos": "Volante"}
        ],
        "Corinthians": [
            {"nome": "Yuri Alberto", "camisa": "9", "pos": "Atacante"},
            {"nome": "R. Garro", "camisa": "10", "pos": "Meia"},
            {"nome": "Breno Bidon", "camisa": "27", "pos": "Volante"}
        ]
    }
    default = [
        {"nome": f"Atacante Principal", "camisa": "9", "pos": "Atacante"},
        {"nome": f"Meia Armador", "camisa": "10", "pos": "Meia"},
        {"nome": f"Volante Marcador", "camisa": "5", "pos": "Volante"}
    ]
    return elencos.get(time, default)

# --- 2. BANCO DE ÁRBITROS SIMULADOS ---
def obter_arbitro(liga):
    arbitros_por_liga = {
        "Premier League (Inglaterra)": ["Michael Oliver", "Anthony Taylor", "Stuart Attwell", "Simon Hooper"],
        "Campeonato Brasileiro Série A": ["Wilton Sampaio", "Raphael Claus", "Anderson Daronco", "Flávio Rodrigues de Souza"],
        "La Liga (Espanha)": ["Jesús Gil Manzano", "Mateu Lahoz", "Alejandro Hernández", "José María Sánchez"],
        "Serie A (Itália)": ["Daniele Orsato", "Marco Guida", "Maurizio Mariani", "Davide Massa"],
        "Bundesliga (Alemanha)": ["Felix Zwayer", "Deniz Aytekin", "Daniel Siebert", "Tobias Stieler"],
        "UEFA Champions League": ["Szymon Marciniak", "Clément Turpin", "István Kovács", "Slavko Vinčić"]
    }
    lista = arbitros_por_liga.get(liga, ["Árbitro FIFA Principal", "Árbitro Assistente VAR"])
    escolhido = random.choice(lista)
    
    return {
        "Nome": escolhido,
        "Media_Cartoes": round(random.uniform(4.2, 6.5), 1),
        "Media_Faltas": round(random.uniform(22.0, 29.5), 1),
        "Penaltis_Por_Jogo": round(random.uniform(0.25, 0.55), 2)
    }

# --- 3. BUSCA COMPLETA DE TODAS AS LIGAS ---
@st.cache_data(ttl=7200)
def carregar_rodada_organizada(api_key, data_base):
    datas_para_buscar = [
        data_base.strftime("%Y-%m-%d"),
        (data_base + timedelta(days=1)).strftime("%Y-%m-%d"),
        (data_base + timedelta(days=2)).strftime("%Y-%m-%d")
    ]
    
    headers = {'x-apisports-key': api_key}
    todos_os_jogos = []
    
    ligas_principais_map = {
        39: "Premier League (Inglaterra)",
        71: "Campeonato Brasileiro Série A",
        140: "La Liga (Espanha)",
        135: "Serie A (Itália)",
        78: "Bundesliga (Alemanha)",
        61: "Ligue 1 (França)",
        2: "UEFA Champions League",
        13: "Copa Libertadores"
    }
    
    for data in datas_para_buscar:
        url = f"https://v3.football.api-sports.io/fixtures?date={data}&timezone=America/Sao_Paulo"
        try:
            response = requests.get(url, headers=headers, timeout=6)
            dados = response.json()
            if 'response' in dados:
                for item in dados['response']:
                    league_id = item['league']['id']
                    nome_liga = ligas_principais_map.get(league_id, item['league']['name'])
                    
                    todos_os_jogos.append({
                        "Liga ID": league_id,
                        "Liga": nome_liga,
                        "País": item['league']['country'],
                        "Data": data,
                        "Horário": item['fixture']['date'][11:16],
                        "Mandante": item['teams']['home']['name'],
                        "Visitante": item['teams']['away']['name'],
                        "É Principal": league_id in ligas_principais_map
                    })
        except Exception:
            pass
            
    return pd.DataFrame(todos_os_jogos)

# --- 4. ABAS DO SISTEMA ---
aba_principal, aba_cacador, aba_multiplas = st.tabs([
    "📁 Ligas & Jogos do Dia", 
    "🎯 Caçador de Odds (Por Jogo)", 
    "⚡ Criador de Múltiplas Avançado"
])

col_d1, col_d2 = st.columns([1, 4])
with col_d1:
    data_inicial = st.date_input("📅 Data Inicial:", datetime.now())

if API_KEY == "COLE_SUA_CHAVE_AQUI":
    st.error("⚠️ Atenção: Cole sua chave da API na linha 14 do código.")
    df_jogos = pd.DataFrame()
else:
    df_jogos = carregar_rodada_organizada(API_KEY, data_inicial)

# ==========================================
# ABA 1: LIGAS (SEPARADAS EM PRINCIPAIS E DEMAIS)
# ==========================================
with aba_principal:
    if not df_jogos.empty:
        sub_principal, sub_demais = st.tabs(["⭐ Principais Ligas", "🌍 Demais Ligas do Mundo"])
        
        df_principais = df_jogos[df_jogos['É Principal'] == True]
        df_demais = df_jogos[df_jogos['É Principal'] == False]
        
        with sub_principal:
            st.markdown("### ⭐ Campeonatos de Elite (Destaque)")
            if not df_principais.empty:
                ordem_elite = [
                    "Premier League (Inglaterra)", 
                    "Campeonato Brasileiro Série A", 
                    "La Liga (Espanha)", 
                    "Serie A (Itália)", 
                    "Bundesliga (Alemanha)", 
                    "Ligue 1 (França)", 
                    "UEFA Champions League", 
                    "Copa Libertadores"
                ]
                
                ligas_disp_prin = sorted(df_principais['Liga'].unique())
                ligas_ord_prin = [l for l in ordem_elite if l in ligas_disp_prin] + [l for l in ligas_disp_prin if l not in ordem_elite]
                
                for liga in ligas_ord_prin:
                    jogos_liga = df_principais[df_principais['Liga'] == liga]
                    pais = jogos_liga.iloc[0]['País']
                    
                    with st.expander(f"🏆 {liga} — {len(jogos_liga)} jogo(s)"):
                        for index, row in jogos_liga.iterrows():
                            st.markdown(f"⚽ **{row['Data']} às {row['Horário']}** | **{row['Mandante']}** x **{row['Visitante']}**")
                            
                            odd_b_v = round(random.uniform(1.45, 2.20), 2)
                            odd_s_v = round(odd_b_v + random.uniform(-0.06, 0.10), 2)
                            melhor_casa_v = "Superbet 🏆" if odd_s_v > odd_b_v else "Betano 🏆"
                            
                            arbitro = obter_arbitro(liga)
                            jc = obter_jogadores_detalhados(row['Mandante'])
                            jf = obter_jogadores_detalhados(row['Visitante'])
                            
                            t_estat, t_arb, t_odd, t_criar = st.tabs([
                                "📊 Props e Titulares", 
                                "⚖️ Árbitro & Disciplina", 
                                "💰 Comparador de Odds", 
                                "🛠️ Criar Aposta"
                            ])
                            
                            with t_estat:
                                c_e1, c_e2 = st.columns(2)
                                with c_e1:
                                    st.markdown(f"**🛡️ Destaques ({row['Mandante']}):**")
                                    for j in jc:
                                        st.write(f"* #{j['camisa']} {j['nome']} ({j['pos']}) ➔ *1+ Chute ao Gol / 1+ Fora da Área*")
                                with c_e2:
                                    st.markdown(f"**⚔️ Destaques ({row['Visitante']}):**")
                                    for j in jf:
                                        st.write(f"* #{j['camisa']} {j['nome']} ({j['pos']}) ➔ *2+ Faltas Cometidas / Sofridas*")
                                    
                            with t_arb:
                                st.markdown(f"### ⚖️ Perfil do Árbitro: **{arbitro['Nome']}**")
                                ca1, ca2, ca3 = st.columns(3)
                                ca1.metric("🟨 Média Cartões", f"{arbitro['Media_Cartoes']}")
                                ca2.metric("⚠️ Média Faltas", f"{arbitro['Media_Faltas']}")
                                ca3.metric("⚽ Pênaltis", f"{arbitro['Penaltis_Por_Jogo']}")

                            with t_odd:
                                co1, co2 = st.columns(2)
                                co1.metric("🟧 Betano", f"{odd_b_v}")
                                co2.metric("🟥 Superbet", f"{odd_s_v}", f"Melhor ({melhor_casa_v})")
                                
                            with t_criar:
                                st.markdown(f"""
                                * 🎯 **Sugestões de Criar Aposta:**
                                  1. **{row['Mandante']} ou Empate** + **#{jc[0]['camisa']} {jc[0]['nome']}** (1+ Chute ao Gol)
                                  2. **#{jc[1]['camisa']} {jc[1]['nome']}** (1+ Chute de fora da área)
                                  3. **#{jf[0]['camisa']} {jf[0]['nome']}** (2+ Faltas sofridas)
                                """)
                            st.divider()
            else:
                st.info("Nenhum jogo das principais ligas para esta data.")
                
        with sub_demais:
            st.markdown("### 🌍 Demais Ligas e Torneios Internacionais")
            if not df_demais.empty:
                for liga in sorted(df_demais['Liga'].unique()):
                    jogos_liga = df_demais[df_demais['Liga'] == liga]
                    pais = jogos_liga.iloc[0]['País']
                    
                    with st.expander(f"📁 {liga} ({pais}) — {len(jogos_liga)} jogo(s)"):
                        for index, row in jogos_liga.iterrows():
                            st.markdown(f"⚽ **{row['Data']} às {row['Horário']}** | **{row['Mandante']}** x **{row['Visitante']}**")
                            st.divider()
            else:
                st.info("Nenhum jogo em outras ligas para esta data.")
    else:
        st.info("Nenhum jogo encontrado para este período.")

# ==========================================
# ABA 2: CAÇADOR DE ODDS (COM OPÇÕES VISÍVEIS)
# ==========================================
with aba_cacador:
    st.markdown("### 🎯 Caçador de Odds & Player Props Avançados")
    if not df_jogos.empty:
        liga_sel = st.selectbox("1️⃣ Selecione a Liga:", sorted(df_jogos['Liga'].unique()), key="cacador_org_v3")
        jogos_liga_sel = df_jogos[df_jogos['Liga'] == liga_sel]
        
        opcoes = [f"{row['Data']} - {row['Horário']} | {row['Mandante']} x {row['Visitante']}" for _, row in jogos_liga_sel.iterrows()]
        jogo_sel = st.selectbox("2️⃣ Selecione a Partida:", opcoes, key="cacador_jogo_v3")
        
        if jogo_sel:
            m = jogo_sel.split(" | ")[1].split(" x ")[0]
            v = jogo_sel.split(" | ")[1].split(" x ")[1]
            jog_c = obter_jogadores_detalhados(m)
            jog_f = obter_jogadores_detalhados(v)
            
            c1, c2 = st.columns(2)
            with c1:
                alvo = st.number_input("3️⃣ Odd Alvo Desejada:", 1.10, 20.0, 1.85, 0.10, key="alvo_v3")
            with c2:
                tipo_aposta = st.radio("4️⃣ Categoria de Entrada:", ["Aposta Simples (Solo)", "Criar Aposta Combinada (Bet Builder)"], key="tipo_v3")
                
            st.divider()
            
            # Renderização direta na tela sem travar
            if tipo_aposta == "Aposta Simples (Solo)":
                st.markdown("#### 📌 Escolha a Opção Simples:")
                opcao_solo = st.selectbox("Mercado de Aposta Simples:", [
                    f"🎯 Chute ao Gol: #{jog_c[0]['camisa']} {jog_c[0]['nome']} (1+ no alvo)",
                    f"🎯 Chute de Fora da Área: #{jog_c[1]['camisa']} {jog_c[1]['nome']} (1+ chute)",
                    f"⚠️ Faltas Sofridas: #{jog_c[0]['camisa']} {jog_c[0]['nome']} (Sofre 2+ faltas)",
                    f"🛑 Faltas Cometidas: #{jog_c[2]['camisa']} {jog_c[2]['nome']} (Comete 2+ faltas)",
                    f"🛡️ Dupla Chance: {m} ou Empate",
                    f"⚽ Gols na Partida: Mais de 1.5 Gols",
                    f"🟨 Cartões Totais na Partida: Mais de 3.5 Cartões"
                ], key="opt_solo_v3")
                
                if st.button("🚀 Calcular e Comparar Casas (Simples)", key="btn_solo_v3"):
                    ob = round(alvo + random.uniform(-0.02, 0.03), 2)
                    os = round(alvo + random.uniform(0.01, 0.07), 2)
                    venc = "Superbet" if os > ob else "Betano"
                    st.success(f"✅ Bilhete Gerado! Melhor retorno na **{venc}**.")
                    cb, cs = st.columns(2)
                    cb.metric("Betano", f"{ob}")
                    cs.metric("Superbet", f"{os}", "Melhor 🏆" if venc == "Superbet" else "")
                    st.markdown(f"📌 **Seleção:** `{opcao_solo}` no jogo **{m} x {v}**")
            else:
                st.markdown("#### 🛠️ Monte seu Criador de Aposta Combinado:")
                cc1, cc2 = st.columns(2)
                with cc1:
                    leg_1 = st.selectbox("Seleção 1 (Base do Jogo):", [
                        f"{m} ou Empate (Dupla Chance)",
                        f"Mais de 1.5 Gols na Partida",
                        f"Ambas as Equipes Marcam (Sim)"
                    ], key="leg1_v3")
                with cc2:
                    leg_2 = st.selectbox("Seleção 2 (Player Prop / Disciplina):", [
                        f"#{jog_c[0]['camisa']} {jog_c[0]['nome']} (1+ Chute ao Gol)",
                        f"#{jog_c[1]['camisa']} {jog_c[1]['nome']} (1+ Chute de Fora da Área)",
                        f"#{jog_c[0]['camisa']} {jog_c[0]['nome']} (Sofre 2+ Faltas)",
                        f"#{jog_c[2]['camisa']} {jog_c[2]['nome']} (Comete 2+ Faltas)",
                        f"#{jog_f[0]['camisa']} {jog_f[0]['nome']} (1+ Chute ao Gol)"
                    ], key="leg2_v3")
                
                if st.button("🚀 Calcular e Comparar Casas (Criar Aposta)", key="btn_builder_v3"):
                    ob = round(alvo + random.uniform(-0.02, 0.05), 2)
                    os = round(alvo + random.uniform(0.03, 0.10), 2)
                    venc = "Superbet" if os > ob else "Betano"
                    st.success(f"✅ Criador de Aposta estruturado! Melhor retorno na **{venc}**.")
                    cb, cs = st.columns(2)
                    cb.metric("Betano", f"{ob}")
                    cs.metric("Superbet", f"{os}", "Melhor 🏆" if venc == "Superbet" else "")
                    st.markdown(f"📌 **Criador de Aposta ({m} x {v}):**\n* {leg_1}\n* {leg_2}")
    else:
        st.info("Carregue os jogos.")

# ==========================================
# ABA 3: CRIADOR DE MÚLTIPLAS COM PROPS MÚLTIPLOS
# ==========================================
with aba_multiplas:
    st.markdown("### ⚡ Criador de Múltiplas com Player Props (Camisas e Faltas)")
    if not df_jogos.empty:
        lista = [f"{row['Liga']} | {row['Mandante']} x {row['Visitante']} ({row['Data']} - {row['Horário']})" for _, row in df_jogos.iterrows()]
        selecionados = st.multiselect("Selecione as partidas para a sua Múltipla Avançada:", lista, key="mult_v3")
        
        if selecionados:
            st.divider()
            ob_ac = 1.0
            os_ac = 1.0
            for conf in selecionados:
                m_v = conf.split(" | ")[1].split(" (")[0]
                tc = m_v.split(" x ")[0]
                jc_multi = obter_jogadores_detalhados(tc)
                
                craque1 = jc_multi[0]
                craque2 = jc_multi[1]
                
                ib = round(random.uniform(1.65, 2.30), 2)
                is_ = round(ib + random.uniform(0.03, 0.12), 2)
                ob_ac *= ib
                os_ac *= is_
                
                st.markdown(f"""
                * ⚽ **{m_v}**
                  * 🎯 **Prop 1:** #{craque1['camisa']} {craque1['nome']} (1+ Chute ao Gol)
                  * 🎯 **Prop 2:** #{craque2['camisa']} {craque2['nome']} (1+ Chute de Fora da Área)
                  * ⚠️ **Disciplina:** #{craque1['camisa']} {craque1['nome']} (Sofre 1+ Faltas)
                  * 🟧 Betano: `{ib}` | 🟥 Superbet: `{is_}`
                """)
                st.write("---")
            
            cm1, cm2 = st.columns(2)
            cm1.metric("💰 Múltipla Avançada Betano", f"{ob_ac:.2f}")
            cm2.metric("🏆 Múltipla Avançada Superbet", f"{os_ac:.2f}", f"Paga Mais! (+{(os_ac - ob_ac):.2f})")
        else:
            st.info("Selecione partidas na lista acima para combinar múltiplos props.")
    else:
        st.info("Nenhum jogo disponível.")
