import streamlit as st
import plotly.graph_objects as go
import base64
import os

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Confini – Indipendenza che vale",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── BRAND COLORS ────────────────────────────────────────────────────────────
NAVY      = "#0D1B4B"
BLUE      = "#1A3A8F"
BRIGHT    = "#2D7DD2"
LIGHT_BG  = "#F4F7FC"
WHITE     = "#FFFFFF"
GOLD      = "#C9A84C"
RED_LOSS  = "#C0392B"

# ─── FORMATO NUMERI ITALIANO ─────────────────────────────────────────────────
def fmt(n, decimali=0):
    """Formatta un numero con separatore migliaia . e decimali ,"""
    if decimali == 0:
        s = f"{n:,.0f}"
    else:
        s = f"{n:,.{decimali}f}"
    # Converti formato anglosassone → italiano: , → X, . → ,, X → .
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return s

# ─── GLOBAL CSS ──────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Sans+3:wght@300;400;600&display=swap');

  html, body, [class*="css"] {{
      font-family: 'Source Sans 3', sans-serif;
      background-color: {LIGHT_BG};
      color: {NAVY};
  }}

  .hero {{
      background: linear-gradient(135deg, {NAVY} 0%, {BLUE} 60%, {BRIGHT} 100%);
      border-radius: 18px;
      padding: 48px 56px 40px 56px;
      margin-bottom: 36px;
      position: relative;
      overflow: hidden;
  }}
  .hero::after {{
      content: '';
      position: absolute;
      top: -60px; right: -60px;
      width: 260px; height: 260px;
      border-radius: 50%;
      background: rgba(45,125,210,0.18);
  }}
  .hero-title {{
      font-family: 'Playfair Display', serif;
      font-size: 2.6rem;
      font-weight: 900;
      color: {WHITE};
      line-height: 1.15;
      margin: 0 0 12px 0;
  }}
  .hero-sub {{
      font-size: 1.15rem;
      color: rgba(255,255,255,0.82);
      font-weight: 300;
      max-width: 680px;
  }}

  .kpi-card {{
      background: {WHITE};
      border-radius: 14px;
      padding: 28px 24px;
      box-shadow: 0 2px 16px rgba(13,27,75,0.08);
      border-left: 5px solid {BRIGHT};
      text-align: center;
  }}
  .kpi-card.bad {{ border-left-color: {RED_LOSS}; }}
  .kpi-card.gold {{ border-left-color: {GOLD}; }}
  .kpi-label {{
      font-size: 0.85rem;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: #7a8aaa;
      margin-bottom: 8px;
  }}
  .kpi-value {{
      font-family: 'Playfair Display', serif;
      font-size: 2.4rem;
      font-weight: 700;
      color: {NAVY};
      line-height: 1;
  }}
  .kpi-value.bad {{ color: {RED_LOSS}; }}
  .kpi-value.good {{ color: {BRIGHT}; }}
  .kpi-value.gold {{ color: {GOLD}; }}
  .kpi-sub {{
      font-size: 0.82rem;
      color: #9aaac0;
      margin-top: 6px;
  }}

  .quote-box {{
      background: linear-gradient(120deg, {NAVY}, {BLUE});
      border-radius: 14px;
      padding: 32px 40px;
      color: {WHITE};
      font-family: 'Playfair Display', serif;
      font-size: 1.35rem;
      font-style: italic;
      line-height: 1.6;
      margin: 28px 0;
      border-left: 6px solid {BRIGHT};
  }}

  .section-title {{
      font-family: 'Playfair Display', serif;
      font-size: 1.6rem;
      font-weight: 700;
      color: {NAVY};
      margin: 36px 0 8px 0;
      border-bottom: 2px solid {BRIGHT};
      padding-bottom: 8px;
  }}

  .footer {{
      text-align: center;
      font-size: 0.78rem;
      color: #aab4cc;
      margin-top: 48px;
      padding-top: 20px;
      border-top: 1px solid #dce4f0;
  }}

  #MainMenu, footer, header {{ visibility: hidden; }}
  .stSlider > div > div {{ accent-color: {BRIGHT}; }}
</style>
""", unsafe_allow_html=True)


# ─── LOGO ────────────────────────────────────────────────────────────────────
logo_path = os.path.join(os.path.dirname(__file__), "logo-orizz-confini.png")
if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode()
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height:60px;">'
    logo_white = f'<img src="data:image/png;base64,{logo_b64}" style="height:48px;filter:brightness(0) invert(1);">'
else:
    logo_html  = f'<span style="font-family:Playfair Display,serif;font-size:1.8rem;font-weight:700;color:{NAVY};">Confini</span>'
    logo_white = f'<span style="font-family:Playfair Display,serif;font-size:1.5rem;font-weight:700;color:{WHITE};">Confini</span>'

st.markdown(f"""
<div style="padding:16px 0 10px 0;">{logo_html}</div>
<hr style="border:none;border-top:2px solid {BRIGHT};margin:0 0 28px 0;">
""", unsafe_allow_html=True)


# ─── PARAMETRI – collassabili ────────────────────────────────────────────────
with st.expander("⚙️ Parametri simulazione", expanded=True):
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        capitale = st.slider("Capitale iniziale (€)", 10_000, 500_000, 100_000, step=5_000, format="€%d")
    with col_s2:
        versamento = st.slider("Versamento mensile (€)", 0, 5_000, 500, step=100, format="€%d")
    with col_s3:
        anni = st.slider("Orizzonte temporale (anni)", 5, 40, 20)
    with col_s4:
        rendimento_lordo = st.slider("Rendimento lordo annuo (%)", 3.0, 10.0, 6.5, step=0.25) / 100

    col_s5, col_s6, _, __ = st.columns(4)
    with col_s5:
        costo_banca = st.slider("Costo annuo fondi bancari (%)", 1.5, 4.0, 2.5, step=0.25) / 100
    with col_s6:
        costo_indip = st.slider("Costo consulenza indipendente (%)", 0.1, 1.0, 0.5, step=0.1) / 100

    st.caption("I dati sono puramente simulativi e non costituiscono consulenza finanziaria.")


# ─── CALCOLI ─────────────────────────────────────────────────────────────────
mesi = anni * 12
r_indip = (rendimento_lordo - costo_indip) / 12
r_banca  = (rendimento_lordo - costo_banca) / 12

def simula(r_mensile):
    saldo = capitale
    storia = [saldo]
    for _ in range(mesi):
        saldo = saldo * (1 + r_mensile) + versamento
        storia.append(saldo)
    return storia

storia_indip = simula(r_indip)
storia_banca  = simula(r_banca)

finale_indip = storia_indip[-1]
finale_banca  = storia_banca[-1]
differenza    = finale_indip - finale_banca
perc_erosione = (differenza / finale_indip) * 100

anni_range = [i / 12 for i in range(mesi + 1)]


# ─── HERO ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="hero-title">Il costo nascosto delle banche.</div>
  <div class="hero-sub">
    Ogni anno, i fondi bancari erodono il tuo patrimonio con commissioni elevate.<br>
    La consulenza indipendente è il modo migliore per investire il tuo capitale.
  </div>
</div>
""", unsafe_allow_html=True)


# ─── KPI ROW ─────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-label">Patrimonio finale<br>Consulenza Indipendente</div>
      <div class="kpi-value good">€ {fmt(finale_indip)}</div>
      <div class="kpi-sub">Costo annuo: {fmt(costo_indip*100, 1)}%</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card bad">
      <div class="kpi-label">Patrimonio finale<br>Fondi Bancari</div>
      <div class="kpi-value bad">€ {fmt(finale_banca)}</div>
      <div class="kpi-sub">Costo annuo: {fmt(costo_banca*100, 1)}%</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card gold">
      <div class="kpi-label">Denaro perso in commissioni</div>
      <div class="kpi-value gold">€ {fmt(differenza)}</div>
      <div class="kpi-sub">In {anni} anni di investimento</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-card bad">
      <div class="kpi-label">Patrimonio eroso dai costi</div>
      <div class="kpi-value bad">{fmt(perc_erosione, 1)}%</div>
      <div class="kpi-sub">Del tuo potenziale finale</div>
    </div>""", unsafe_allow_html=True)


# ─── QUOTE ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="quote-box">
  "La differenza tra il 2,5% e lo 0,5% di costo annuo non sembra molta.<br>
   Ma su {anni} anni, quella differenza vale <strong>€ {fmt(differenza)}</strong> — denaro tuo,<br>
   che stai regalando alla banca ogni giorno senza saperlo."
</div>
""", unsafe_allow_html=True)


# ─── GRAFICO PRINCIPALE ───────────────────────────────────────────────────────
st.markdown(f'<div class="section-title">📈 Crescita del patrimonio nel tempo</div>', unsafe_allow_html=True)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=anni_range + anni_range[::-1],
    y=storia_indip + storia_banca[::-1],
    fill='toself',
    fillcolor='rgba(45,125,210,0.10)',
    line=dict(color='rgba(0,0,0,0)'),
    showlegend=False,
    hoverinfo='skip',
    name='Differenza'
))

fig.add_trace(go.Scatter(
    x=anni_range,
    y=storia_banca,
    mode='lines',
    name='Fondi Bancari',
    line=dict(color=RED_LOSS, width=3, dash='dash'),
))

fig.add_trace(go.Scatter(
    x=anni_range,
    y=storia_indip,
    mode='lines',
    name='Consulenza Indipendente',
    line=dict(color=BRIGHT, width=4),
))

capitale_curve = [capitale + versamento * m for m in range(mesi + 1)]
fig.add_trace(go.Scatter(
    x=anni_range,
    y=capitale_curve,
    mode='lines',
    name='Capitale versato',
    line=dict(color='#aab4cc', width=2, dash='dot'),
))

# Annotation: sfondo bianco, testo navy, senza bordo
fig.add_annotation(
    x=anni, y=(finale_indip + finale_banca) / 2,
    text=f"<b>€ {fmt(differenza)}<br>persi in costi</b>",
    showarrow=True,
    arrowhead=2,
    arrowcolor=BRIGHT,
    font=dict(color=NAVY, size=14, family='Source Sans 3'),
    bgcolor=WHITE,
    borderwidth=0,
    borderpad=10,
    ax=70, ay=0,
)

fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Source Sans 3', color=NAVY),
    legend=dict(
        orientation='v',
        yanchor='middle', y=0.5,
        xanchor='left', x=1.02,
        font=dict(size=13),
        bgcolor='rgba(255,255,255,0.85)',
        borderwidth=0,
        itemwidth=30,
        traceorder='normal',
    ),
    xaxis=dict(
        title='Anni',
        gridcolor='#e8edf5',
        tickfont=dict(size=12),
        showline=True, linecolor='#dce4f0',
    ),
    yaxis=dict(
        title='Patrimonio (€)',
        gridcolor='#e8edf5',
        tickformat='€,.0f',
        tickfont=dict(size=12),
        showline=True, linecolor='#dce4f0',
    ),
    height=520,
    margin=dict(l=20, r=180, t=40, b=20),
    hovermode='x unified',
)

st.plotly_chart(fig, use_container_width=True)


# ─── GRAFICO EROSIONE CUMULATIVA ─────────────────────────────────────────────
st.markdown(f'<div class="section-title">🔥 Commissioni cumulative sottratte al tuo patrimonio</div>', unsafe_allow_html=True)

erosione_cumulativa = [i - b for i, b in zip(storia_indip, storia_banca)]

fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=anni_range,
    y=erosione_cumulativa,
    mode='lines',
    fill='tozeroy',
    fillcolor='rgba(192,57,43,0.15)',
    line=dict(color=RED_LOSS, width=3),
    name='Costo nascosto cumulativo',
))

fig2.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Source Sans 3', color=NAVY),
    xaxis=dict(title='Anni', gridcolor='#e8edf5', showline=True, linecolor='#dce4f0'),
    yaxis=dict(title='€ persi in commissioni', tickformat='€,.0f', gridcolor='#e8edf5', showline=True, linecolor='#dce4f0'),
    height=320,
    margin=dict(l=20, r=20, t=20, b=20),
    showlegend=False,
)

for anno_check in range(5, anni + 1, 5):
    idx = anno_check * 12
    if idx < len(erosione_cumulativa):
        fig2.add_annotation(
            x=anno_check,
            y=erosione_cumulativa[idx],
            text=f"<b>€ {fmt(erosione_cumulativa[idx])}</b>",
            showarrow=True, arrowhead=1, arrowcolor=RED_LOSS,
            font=dict(color=RED_LOSS, size=11),
            ax=0, ay=-30,
            bgcolor='rgba(255,255,255,0.85)',
            bordercolor=RED_LOSS,
            borderpad=4,
        )

st.plotly_chart(fig2, use_container_width=True)


# ─── PERCHÉ INDIPENDENTE ──────────────────────────────────────────────────────
st.markdown(f'<div class="section-title">⚖️ Perché la consulenza indipendente è diversa</div>', unsafe_allow_html=True)


cards = [
    ("🚫", "Assenza di conflitti d'interesse", f"Il consulente indipendente <b>non guadagna commissioni</b> sui prodotti che ti consiglia. Il suo unico compenso viene da te. Il suo interesse coincide con il tuo.", BRIGHT),
    ("📉", "Costi ridotti e più profitti per te", f"I fondi bancari applicano spesso il <b>2-3% annuo</b> tra gestione, distribuzione e performance fee. Un consulente indipendente ti raccomanderà strumenti efficienti direttamente acquistabili sul mercato con costi 10 volte inferiori.", RED_LOSS),
    ("🔍", "Professionalità e garanzie", f"Il consulente indipendente è un professionista iscritto all'Albo allo stesso modo dei consulenti bancari ed il servizio ha le stesse regole e tutele di legge.", GOLD),
    ("🔒", "Massima Sicurezza e Tranquillità", f"Il consulente indipendente <b>non ha accesso ai tuoi conti</b> e non fa alcuna operazione per conto tuo. I tuoi soldi rimangono sempre nella tua esclusiva disponibilità presso la tua banca.", NAVY),
]

row1 = st.columns(2)
row2 = st.columns(2)
cols = [row1[0], row1[1], row2[0], row2[1]]

for col, (icon, title, desc, color) in zip(cols, cards):
    with col:
        st.markdown(f"""
        <div style="background:{WHITE};border-radius:14px;padding:28px 22px;box-shadow:0 2px 16px rgba(13,27,75,0.07);height:100%;border-top:4px solid {color};margin-bottom:16px;">
          <div style="font-size:2rem;margin-bottom:12px;">{icon}</div>
          <div style="font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:{NAVY};margin-bottom:10px;">{title}</div>
          <div style="font-size:0.9rem;color:#4a5a7a;line-height:1.6;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)


# ─── CHIUSURA EMOTIVA ─────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg,{NAVY},{BLUE});border-radius:16px;padding:40px 48px;margin-top:40px;color:{WHITE};text-align:center;">
  <div style="font-family:'Playfair Display',serif;font-size:1.9rem;font-weight:700;margin-bottom:16px;">
    Non è una questione di rendimenti.<br>È una questione di a chi appartiene il tuo denaro.
  </div>
  <div style="font-size:1.05rem;color:rgba(255,255,255,0.8);max-width:640px;margin:0 auto;line-height:1.7;">
    Con la consulenza indipendente, ogni euro di commissione risparmiata rimane nel tuo patrimonio, 
    si capitalizza, cresce. Nel lungo periodo, questa è la differenza che conta davvero.
  </div>
  <div style="margin-top:28px;display:flex;justify-content:center;">
    {logo_white}
  </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div class="footer">
  I dati e le proiezioni mostrate sono puramente simulativi con finalità illustrative. 
  Non costituiscono consulenza finanziaria, offerta di investimento o promozione di prodotti finanziari. 
  Rendimenti passati non garantiscono risultati futuri. © Confini
</div>
""", unsafe_allow_html=True)