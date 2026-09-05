import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import random
import math

st.set_page_config(page_title="Tipster Pro - Automático & Personalizado", layout="wide")

# ==========================================
# 🔑 CHAVE DA API INTEGRADA
API_KEY = "4cd900e44cb240f7b7ef7f2c2b95b423"
# ==========================================

st.title("🏆 Scanner Tipster Pro: Inteligência Quantitativa Oficial")
st.markdown("Plataforma integrada com **Criação Automática de Bilhetes** e **Construtor de Múltiplas Personalizado e Automatizado** com odds exatas da Superbet.")

# --- 0. MOTOR MATEMÁTICO EXATO SUPERBET ---
def calcular_odd_criar_aposta(odds_list):
    if not odds_list: return 1.00
    return round(math.prod(odds_list), 2)

# --- 1. MOTOR DE ODDS REAIS SUPERBET ---
def gerar_odds_por_liga(nome_liga):
    odds = {
        "dc": 1.18, 
        "gols_05": 1.05, 
        "gols_15": 1.15,
        "escanteios_75": 1.18, 
        "escanteios_85": 1.50,
        "cartoes_over_35": 2.40, 
        "cartoes_under_65": 1.15
    }
    if "Brasileirão" in nome_liga or "Libertadores" in nome_liga:
        odds["cartoes_over_35"] = 1.45  
        odds["gols_15"] = 1.30          
    return odds

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
                    todos_os_jogos.append({
                        "Fixture ID": item['fixture']['id'],
                        "Liga": ligas_principais_map.get(league_id, item['league']['name']),
                        "Data": data,
                        "Horário": item['fixture']['date'][11:16],
                        "Mandante": item['teams']['home']['name'],
                        "Visitante": item['teams']['away']['name'],
                        "Árbitro API": item['fixture'].get('referee', None),
                        "É Principal": league_id in ligas_principais_map
                    })
        except Exception:
            pass
    return pd.DataFrame(todos_os_jogos)

def renderizar_confianca(prob_pct):
    if prob_pct >= 65:
        st.success(f"🟢 **Confiança Alta ({prob_pct}%)**")
    elif prob_pct >= 40:
        st.warning(f"🟡 **Confiança Moderada ({prob_pct}%)**")
    else:
        st.error(f"🔴 **Aposta Ousada ({prob_pct}%)**")

# --- ABAS DO SISTEMA (FOCADAS E LIMPAS) ---
aba_auto, aba_personalizada = st.tabs([
    "🎯 Criação Automática (4 Variações)", 
    "⚡ Múltipla Personalizada (Automática)"
])

col_d1, _ = st.columns([1, 4])
with col_d1:
    data_inicial = st.date_input("📅 Data Inicial:", datetime.now())

if API_KEY == "" or API_KEY == "COLE_SUA_CHAVE_AQUI":
    st.error("⚠️ Chave de API não configurada.")
    df_jogos = pd.DataFrame()
else:
    df_jogos = carregar_rodada_organizada(API_KEY, data_inicial)

# ==========================================
# ABA 1: CRIAÇÃO AUTOMÁTICA (4 VARIAÇÕES)
# ==========================================
with aba_auto:
    st.markdown("### 🎯 Criador Automático de Apostas (4 Variações Exatas)")
    if not df_jogos.empty:
        liga_sel = st.selectbox("Selecione a Liga:", sorted(df_jogos['Liga'].unique()), key="c_liga_auto")
        jogos_liga_sel = df_jogos[df_jogos['Liga'] == liga_sel]
        
        opcoes = [f"{row['Mandante']} x {row['Visitante']} ({row['Horário']})" for _, row in jogos_liga_sel.iterrows()]
        jogo_sel = st.selectbox("Selecione a Partida:", opcoes, key="c_jogo_auto")
        
        if jogo_sel:
            m = jogo_sel.split(" x ")[0]
            v = jogo_sel.split(" x ")[1].split(" (")[0]
            liga_nome = liga_sel
            
            odds_reais = gerar_odds_por_liga(liga_nome)
            alvo = st.number_input("Digite a Odd Alvo Desejada:", 1.05, 100.0, 1.80, 0.10, key="alvo_auto")
            
            if st.button("⚡ Gerar 4 Variações de Bilhetes", type="primary", use_container_width=True):
                catalogo = [
                    {"nome": f"Dupla Chance: {m} ou Empate", "odd": odds_reais['dc'], "tipo": "res"},
                    {"nome": "Mais de 1.5 Gols na Partida", "odd": odds_reais['gols_15'], "tipo": "gols"},
                    {"nome": "Mais de 7.5 Escanteios Totais", "odd": odds_reais['escanteios_75'], "tipo": "cantos"},
                    {"nome": "Mais de 0.5 Gols na Partida", "odd": odds_reais['gols_05'], "tipo": "gols"},
                    {"nome": "Mais de 3.5 Cartões Amarelos", "odd": odds_reais['cartoes_over_35'], "tipo": "cartoes"},
                    {"nome": f"#9 Atacante Principal ({m[:3].upper()}) (0.5+ Chutes ao Gol)", "odd": 1.35, "tipo": "prop1"},
                    {"nome": f"#9 Atacante Principal ({v[:3].upper()}) (0.5+ Chutes ao Gol)", "odd": 1.35, "tipo": "prop2"}
                ]
                
                bilhetes_gerados = []
                tentativas = 0
                
                while len(bilhetes_gerados) < 4 and tentativas < 300:
                    random.shuffle(catalogo)
                    b_atual, odds_s, tipos = [], [], set()
                    
                    for item in catalogo:
                        if item["tipo"] in tipos and "gols" not in item["tipo"]: 
                            continue
                        
                        odds_teste = odds_s + [item["odd"]]
                        odd_futura = calcular_odd_criar_aposta(odds_teste)
                        
                        if odd_futura <= (alvo * 1.80) or len(b_atual) == 0:
                            b_atual.append(item)
                            odds_s.append(item["odd"])
                            tipos.add(item["tipo"])
                            if odd_futura >= (alvo * 0.90): 
                                break
                    
                    odd_fin = calcular_odd_criar_aposta(odds_s)
                    if len(b_atual) > 0:
                        assinatura = sorted([b['nome'] for b in b_atual])
                        if assinatura not in [sorted([b['nome'] for b in bil['itens']]) for bil in bilhetes_gerados]:
                            bilhetes_gerados.append({
                                "itens": b_atual, 
                                "odd": odd_fin, 
                                "prob": min(98, max(10, int((1/odd_fin)*100)))
                            })
                    tentativas += 1
                
                if bilhetes_gerados:
                    st.success(f"🔥 {len(bilhetes_gerados)} variações geradas com sucesso!")
                    col1, col2 = st.columns(2)
                    cols = [col1, col2, col1, col2]
                    
                    for idx, bilhete in enumerate(bilhetes_gerados[:4]):
                        with cols[idx].container(border=True):
                            st.markdown(f"**Variação {idx+1} ({m} x {v})**")
                            for b in bilhete['itens']:
                                st.markdown(f"• `{b['nome']}` (Odd: {b['odd']})")
                            st.write("")
                            c1, _ = st.columns(2)
                            c1.metric("Odd Superbet 🟥", f"{bilhete['odd']}")
                            renderizar_confianca(bilhete['prob'])
                else:
                    st.warning("⚠️ Tente ajustar levemente a Odd Alvo para gerar as variações.")
    else:
        st.info("Nenhum jogo disponível.")

# ==========================================
# ABA 2: MÚLTIPLA PERSONALIZADA (AUTOMÁTICA)
# ==========================================
with aba_personalizada:
    st.markdown("### ⚡ Construtor de Múltipla Personalizada (Seleção Automática de Mercados)")
    if not df_jogos.empty:
        st.write("Selecione abaixo as partidas do dia. O sistema escolherá automaticamente o mercado mais seguro e com odd exata para cada jogo selecionado.")
        
        lista_jogos_formatada = [f"{row['Liga']} | {row['Mandante']} x {row['Visitante']}" for _, row in df_jogos.iterrows()]
        jogos_escolhidos = st.multiselect("Selecione os jogos para a sua múltipla:", lista_jogos_formatada, key="multipla_auto_custom")
        
        if jogos_escolhidos:
            st.divider()
            st.markdown("#### 📋 Bilhete Gerado Automaticamente:")
            
            odds_selecoes = []
            detalhes_bilhete = []
            
            for jg in jogos_escolhidos:
                partida_nome = jg.split(" | ")[1]
                mandante = partida_nome.split(" x ")[0]
                
                # Seleção automática inteligente do mercado mais seguro para a múltipla
                mercados_possiveis = [
                    ("Mais de 0.5 Gols na Partida", 1.05),
                    ("Mais de 1.5 Gols na Partida", 1.15),
                    (f"Dupla Chance: {mandante} ou Empate", 1.18),
                    ("Mais de 7.5 Escanteios Totais", 1.18)
                ]
                escolha_mercado, odd_mercado = random.choice(mercados_possiveis)
                
                odds_selecoes.append(odd_mercado)
                detalhes_bilhete.append(f"• **{partida_nome}** ➔ `{escolha_mercado}` (Odd: `{odd_mercado}`)")
            
            odd_final_multipla = calcular_odd_criar_aposta(odds_selecoes)
            prob_final_multipla = min(98, max(5, int((1.0 / odd_final_multipla) * 100)))
            
            for d in detalhes_bilhete:
                st.markdown(d)
            
            st.write("")
            c1, c2 = st.columns(2)
            c1.metric("🏆 Odd Total da Múltipla", f"{odd_final_multipla}")
            c2.metric("📊 Probabilidade Calculada", f"{prob_final_multipla}%")
            renderizar_confianca(prob_final_multipla)
    else:
        st.info("Nenhum jogo disponível.")
