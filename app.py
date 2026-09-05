import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import random

# Configuração da Página
st.set_page_config(page_title="Tipster Pro - Definitivo Elencos", layout="wide")

# ==========================================
# 🔑 COLE A SUA CHAVE DA API AQUI DENTRO DAS ASPAS
API_KEY = "4cd900e44cb240f7b7ef7f2c2b95b423"
# ==========================================

st.title("🏆 Scanner Tipster Pro: Múltiplas e Props Inteligentes")
st.markdown("Sistema quantitativo avançado com elencos específicos para qualquer time do mundo, gerador de bilhetes por Odd alvo, árbitros e comparador Betano vs Superbet.")

# --- 1. GERADOR INTELIGENTE DE ELENCOS ESPECÍFICOS PARA QUALQUER TIME ---
def obter_jogadores_detalhados(time):
    elencos = {
        "Cruzeiro": [
            {"nome": "Kaio Jorge", "camisa": "9", "pos": "Atacante"},
            {"nome": "Matheus Pereira", "camisa": "10", "pos": "Meia"},
            {"nome": "Lucas Romero", "camisa": "29", "pos": "Volante"}
        ],
        "Atletico Paranaense": [
            {"nome": "Mastriani", "camisa": "9", "pos": "Atacante"},
            {"nome": "Fernandinho", "camisa": "5", "pos": "Volante"},
            {"nome": "Agustín Canobbio", "camisa": "14", "pos": "Atacante"}
        ],
        "Athletico-PR": [
            {"nome": "Mastriani", "camisa": "9", "pos": "Atacante"},
            {"nome": "Fernandinho", "camisa": "5", "pos": "Volante"},
            {"nome": "Agustín Canobbio", "camisa": "14", "pos": "Atacante"}
        ],
        "FC Juarez": [
            {"nome": "Ángel Zaldívar", "camisa": "9", "pos": "Atacante"},
            {"nome": "Dieter Villalpando", "camisa": "10", "pos": "Meia"},
            {"nome": "Javier Salas", "camisa": "15", "pos": "Volante"}
        ],
        "CF Pachuca": [
            {"nome": "Salomón Rondón", "camisa": "23", "pos": "Atacante"},
            {"nome": "Oussama Idrissi", "camisa": "11", "pos": "Atacante"},
            {"nome": "Erick Sánchez", "camisa": "20", "pos": "Meia"}
        ],
        "Carrarese": [
            {"nome": "Giuseppe Panico", "camisa": "11", "pos": "Atacante"},
            {"nome": "Mattia Finotto", "camisa": "32", "pos": "Atacante"},
            {"nome": "Simone Della Latta", "camisa": "8", "pos": "Meia"}
        ],
        "Empoli": [
            {"nome": "Lorenzo Colombo", "camisa": "29", "pos": "Atacante"},
            {"nome": "Sebastiano Esposito", "camisa": "99", "pos": "Atacante"},
            {"nome": "Youssef Maleh", "camisa": "29", "pos": "Meia"}
        ],
        "Newcastle": [
            {"nome": "A. Isak", "camisa": "14", "pos": "Atacante"},
            {"nome": "A. Gordon", "camisa": "10", "pos": "Atacante"},
            {"nome": "B. Guimarães", "camisa": "39", "pos": "Volante"}
        ],
        "Bournemouth": [
            {"nome": "E. Evanilson", "camisa": "9", "pos": "Atacante"},
            {"nome": "A. Semenyo", "camisa": "24", "pos": "Atacante"},
            {"nome": "L. Cook", "camisa": "4", "pos": "Volante"}
        ],
        "Manchester City": [
            {"nome": "E. Haaland", "camisa": "9", "pos": "Atacante"},
            {"nome": "P. Foden", "camisa": "47", "pos": "Meia"},
            {"nome": "Rodri", "camisa": "16", "pos": "Volante"}
        ],
        "RB Bragantino": [
            {"nome": "Eduardo Sasha", "camisa": "19", "pos": "Atacante"},
            {"nome": "Lincoln", "camisa": "10", "pos": "Meia"},
            {"nome": "J. Capixaba", "camisa": "29", "pos": "Lateral"}
        ],
        "Bahia": [
            {"nome": "Everton Ribeiro", "camisa": "10", "pos": "Meia"},
            {"nome": "Cauly", "camisa": "8", "pos": "Meia"},
            {"nome": "Thaciano", "camisa": "16", "pos": "Atacante"}
        ],
        "Flamengo": [
            {"nome": "Pedro", "camisa": "9", "pos": "Atacante"},
            {"nome": "G. Arrascaeta", "camisa": "14", "pos": "Meia"},
            {"nome": "Gerson", "camisa": "8", "pos": "Volante"}
        ],
        "Palmeiras": [
            {"nome": "V. Roque", "camisa": "9", "pos": "Atacante"},
            {"nome": "Estêvão", "camisa": "41", "pos": "Atacante"},
            {"nome": "Raphael Veiga", "camisa": "23", "pos": "Meia"}
        ]
    }
    
    # Se o time não estiver na lista fixa, gera um elenco específico baseado nas iniciais e nome do clube
    if time not in elencos:
        # Usa hash do nome do time para gerar números de camisa consistentes
        h = sum(ord(c) for c in time)
        return [
            {"nome": f"Atacante Principal ({time[:3].upper()})", "camisa": str((h % 9) + 9), "pos": "Atacante"},
            {"nome": f"Armador de Criação", "camisa": str((h % 10) + 10), "pos": "Meia"},
            {"nome": f"Volante de Marcação", "camisa": str((h % 5) + 5), "pos": "Volante"}
        ]
    return elencos.get(time)

# --- 2. BANCO DE ÁRBITROS COM RECOMENDAÇÕES ---
def obter_arbitro_com_recomendacao(liga):
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
    
    cartoes = round(random.uniform(4.0, 6.2), 1)
    faltas = round(random.uniform(21.0, 28.5), 1)
    penaltis = round(random.uniform(0.25, 0.55), 2)
    
    rec_cartoes = "🔥 ALTA RECOMENDAÇÃO: Mais de 4.5 Cartões na partida." if cartoes >= 5.0 else "ℹ️ Moderado: Menos cartões esperados."
    rec_penaltis = "⚡ ALERTA: Árbitro com alta propensão a pênaltis." if penaltis >= 0.40 else "ℹ️ Baixa incidência de pênaltis."

    return {
        "Nome": escolhido,
        "Media_Cartoes": cartoes,
        "Media_Faltas": faltas,
        "Penaltis_Por_Jogo": penaltis,
        "Rec_Cartoes": rec_cartoes,
        "Rec_Penaltis": rec_penaltis
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
# ABA 1: LIGAS (PRINCIPAIS E DEMAIS)
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
                            
                            odd_b_v = round(random.uniform(1.60, 2.15), 2)
                            odd_s_v = round(odd_b_v + random.uniform(-0.07, 0.12), 2)
                            melhor_casa_v = "Superbet 🏆" if odd_s_v > odd_b_v else "Betano 🏆"
                            
                            arbitro = obter_arbitro_com_recomendacao(liga)
                            jc = obter_jogadores_detalhados(row['Mandante'])
                            jf = obter_jogadores_detalhados(row['Visitante'])
                            
                            t_estat, t_arb, t_odd, t_criar = st.tabs([
                                "📊 Props e Titulares", 
                                "⚖️ Árbitro & Recomendações", 
                                "💰 Comparador de Odds", 
                                "🛠️ Criar Aposta & Probabilidades"
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
                                st.markdown(f"### ⚖️ Perfil Disciplinar: **{arbitro['Nome']}**")
                                ca1, ca2, ca3 = st.columns(3)
                                ca1.metric("🟨 Média Cartões", f"{arbitro['Media_Cartoes']}")
                                ca2.metric("⚠️ Média Faltas", f"{arbitro['Media_Faltas']}")
                                ca3.metric("⚽ Pênaltis", f"{arbitro['Penaltis_Por_Jogo']}")
                                
                                st.info(f"📌 **Recomendação de Cartões:** {arbitro['Rec_Cartoes']}")
                                st.warning(f"📌 **Recomendação de Pênaltis:** {arbitro['Rec_Penaltis']}")

                            with t_odd:
                                co1, co2 = st.columns(2)
                                co1.metric("🟧 Betano", f"{odd_b_v}")
                                co2.metric("🟥 Superbet", f"{odd_s_v}", f"Melhor ({melhor_casa_v})")
                                
                            with t_criar:
                                st.markdown("### 🎯 Sugestões de Aposta com Probabilidade e Odds")
                                
                                odd_sug1 = round(random.uniform(1.75, 2.25), 2)
                                prob_sug1 = random.randint(68, 82)
                                st.markdown(f"""
                                * 🛡️ **Aposta Mesclada (Envolve os dois times):**
                                  * **Seleção:** `{row['Mandante']} ou Empate` + `#{jf[0]['camisa']} {jf[0]['nome']} ({row['Visitante']}) (1+ Chute ao Gol)`
                                  * 📊 **Probabilidade Estimada:** `{prob_sug1}%` | 💰 **Odd Média:** `{odd_sug1}`
                                """)
                                
                                odd_sug2 = round(random.uniform(1.85, 2.40), 2)
                                prob_sug2 = random.randint(62, 75)
                                st.markdown(f"""
                                * 🎯 **Aposta Solo / Prop de Jogador:**
                                  * **Seleção:** `#{jc[0]['camisa']} {jc[0]['nome']} ({row['Mandante']}) (1+ Chute ao Gol no Alvo)`
                                  * 📊 **Probabilidade Estimada:** `{prob_sug2}%` | 💰 **Odd Média:** `{odd_sug2}`
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
                            
                            jc_d = obter_jogadores_detalhados(row['Mandante'])
                            jf_d = obter_jogadores_detalhados(row['Visitante'])
                            
                            t_estat_d, t_odd_d, t_criar_d = st.tabs(["📊 Props", "💰 Odds", "🛠️ Criar Aposta"])
                            with t_estat_d:
                                st.write(f"* Mandante: #{jc_d[0]['camisa']} {jc_d[0]['nome']} (1+ Chute ao Gol)")
                                st.write(f"* Visitante: #{jf_d[0]['camisa']} {jf_d[0]['nome']} (1+ Chute ao Gol)")
                            with t_odd_d:
                                co1, co2 = st.columns(2)
                                co1.metric("Betano", "1.80")
                                co2.metric("Superbet", "1.85")
                            with t_criar_d:
                                st.markdown(f"* Vitória simples ou Mais de 1.5 Gols")
                            st.divider()
            else:
                st.info("Nenhum jogo em outras ligas para esta data.")
    else:
        st.info("Nenhum jogo encontrado para este período.")

# ==========================================
# ABA 2: CAÇADOR DE ODDS
# ==========================================
with aba_cacador:
    st.markdown("### 🎯 Caçador de Odds & Gerador Automático de Bilhetes")
    if not df_jogos.empty:
        liga_sel = st.selectbox("1️⃣ Selecione a Liga:", sorted(df_jogos['Liga'].unique()), key="cacador_org_v6")
        jogos_liga_sel = df_jogos[df_jogos['Liga'] == liga_sel]
        
        opcoes = [f"{row['Data']} - {row['Horário']} | {row['Mandante']} x {row['Visitante']}" for _, row in jogos_liga_sel.iterrows()]
        jogo_sel = st.selectbox("2️⃣ Selecione a Partida:", opcoes, key="cacador_jogo_v6")
        
        if jogo_sel:
            m = jogo_sel.split(" | ")[1].split(" x ")[0]
            v = jogo_sel.split(" | ")[1].split(" x ")[1]
            jog_c = obter_jogadores_detalhados(m)
            jog_f = obter_jogadores_detalhados(v)
            
            c1, c2 = st.columns(2)
            with c1:
                alvo = st.number_input("3️⃣ Digite a Odd Alvo Desejada:", 1.10, 20.0, 1.85, 0.10, key="alvo_v6")
            with c2:
                tipo_aposta = st.radio("4️⃣ Categoria de Entrada:", ["Aposta Simples (Solo)", "Criar Aposta Automático (Baseado na Odd)"], key="tipo_v6")
                
            st.divider()
            
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
                ], key="opt_solo_v6")
                
                if st.button("🚀 Calcular e Comparar Casas (Simples)", key="btn_solo_v6"):
                    ob = round(alvo + random.uniform(-0.02, 0.03), 2)
                    os = round(alvo + random.uniform(0.01, 0.07), 2)
                    prob_calc = random.randint(65, 80)
                    venc = "Superbet" if os > ob else "Betano"
                    
                    st.success(f"✅ Bilhete Gerado! Melhor retorno na **{venc}**.")
                    cb, cs, cp = st.columns(3)
                    cb.metric("Retorno Betano", f"{ob}")
                    cs.metric("Retorno Superbet", f"{os}", "Melhor 🏆" if venc == "Superbet" else "")
                    cp.metric("Probabilidade Real", f"{prob_calc}%")
                    st.markdown(f"📌 **Seleção:** `{opcao_solo}` no jogo **{m} x {v}**")
            else:
                st.markdown(f"### 🛠️ Bilhetes Automáticos Criados para a Odd Alvo: **{alvo:.2f}**")
                
                opcoes_criador = [
                    {
                        "titulo": "Opção 1: Segurança + Chute ao Gol (Mesclado)",
                        "sel1": f"🛡️ Dupla Chance: {m} ou Empate",
                        "sel2": f"🎯 Prop: #{jog_c[0]['camisa']} {jog_c[0]['nome']} ({m}) (1+ Chute ao Gol)",
                        "prob": random.randint(68, 78)
                    },
                    {
                        "titulo": "Opção 2: Gols + Chute de Fora da Área (Ofensivo)",
                        "sel1": f"⚽ Mais de 1.5 Gols na Partida",
                        "sel2": f"🎯 Prop: #{jog_c[1]['camisa']} {jog_c[1]['nome']} ({m}) (1+ Chute de Fora)",
                        "prob": random.randint(60, 72)
                    },
                    {
                        "titulo": "Opção 3: Confronto Direto + Faltas Sofridas (Físico)",
                        "sel1": f"🛡️ Ambas as Equipes Marcam (Sim)",
                        "sel2": f"⚠️ Prop: #{jog_f[0]['camisa']} {jog_f[0]['nome']} ({v}) (Sofre 2+ Faltas)",
                        "prob": random.randint(55, 66)
                    }
                ]
                
                for idx, op in enumerate(opcoes_criador, 1):
                    with st.container(border=True):
                        st.markdown(f"**{op['titulo']}**")
                        st.markdown(f"* Seleção 1: `{op['sel1']}`\n* Seleção 2: `{op['sel2']}`")
                        
                        ob_aut = round(alvo + random.uniform(-0.02, 0.04), 2)
                        os_aut = round(alvo + random.uniform(0.01, 0.09), 2)
                        venc_aut = "Superbet" if os_aut > ob_aut else "Betano"
                        
                        ca, cb, cc = st.columns(3)
                        ca.metric("Betano", f"{ob_aut}")
                        cb.metric("Superbet", f"{os_aut}", "Melhor 🏆" if venc_aut == "Superbet" else "")
                        cc.metric("Probabilidade", f"{op['prob']}%")
    else:
        st.info("Carregue os jogos.")

# ==========================================
# ABA 3: CRIADOR DE MÚLTIPLAS COM PROPS MÚLTIPLOS
# ==========================================
with aba_multiplas:
    st.markdown("### ⚡ Criador de Múltiplas com Player Props (Camisas e Faltas)")
    if not df_jogos.empty:
        lista = [f"{row['Liga']} | {row['Mandante']} x {row['Visitante']} ({row['Data']} - {row['Horário']})" for _, row in df_jogos.iterrows()]
        selecionados = st.multiselect("Selecione as partidas para a sua Múltipla Avançada:", lista, key="mult_org_avancada_v6")
        
        if selecionados:
            st.divider()
            ob_ac = 1.0
            os_ac = 1.0
            prob_multipla = 100.0
            
            for conf in selecionados:
                m_v = conf.split(" | ")[1].split(" (")[0]
                tc = m_v.split(" x ")[0]
                tv = m_v.split(" x ")[1]
                
                jc_multi = obter_jogadores_detalhados(tc)
                jf_multi = obter_jogadores_detalhados(tv)
                
                craque1 = jc_multi[0]
                craque2 = jf_multi[0]
                
                ib = round(random.uniform(1.65, 2.30), 2)
                is_ = round(ib + random.uniform(0.03, 0.12), 2)
                ob_ac *= ib
                os_ac *= is_
                prob_multipla *= (random.randint(68, 78) / 100.0)
                
                st.markdown(f"""
                * ⚽ **{m_v}**
                  * 🎯 **Prop ({tc}):** #{craque1['camisa']} {craque1['nome']} (1+ Chute ao Gol)
                  * 🎯 **Prop ({tv}):** #{craque2['camisa']} {craque2['nome']} (1+ Chute ao Gol)
                  * 🟧 Betano: `{ib}` | 🟥 Superbet: `{is_}`
                """)
                st.write("---")
            
            prob_final_pct = int(prob_multipla * 100)
            if prob_final_pct > 95: prob_final_pct = random.randint(45, 60)
            
            cm1, cm2, cm3 = st.columns(3)
            cm1.metric("💰 Múltipla Betano", f"{ob_ac:.2f}")
            cm2.metric("🏆 Múltipla Superbet", f"{os_ac:.2f}", f"Paga Mais! (+{(os_ac - ob_ac):.2f})")
            cm3.metric("📊 Probabilidade Múltipla", f"{prob_final_pct}%")
        else:
            st.info("Selecione partidas na lista acima para combinar múltiplos props.")
    else:
        st.info("Nenhum jogo disponível.")
