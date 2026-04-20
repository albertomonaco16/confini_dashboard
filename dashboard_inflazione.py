import streamlit as st
import plotly.graph_objects as go
import base64
import os

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Confini – Il costo di non investire",
    page_icon="💸",
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
GRAY      = "#8A9AB5"

# ─── FORMATO NUMERI ITALIANO ─────────────────────────────────────────────────
def fmt(n, decimali=2):
    s = f"{n:,.{decimali}f}"
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
  .kpi-card.bad  {{ border-left-color: {RED_LOSS}; }}
  .kpi-card.gray {{ border-left-color: {GRAY}; }}
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
  .kpi-value.bad  {{ color: {RED_LOSS}; }}
  .kpi-value.gray {{ color: {GRAY}; }}
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
    logo_html  = f'<img src="data:image/png;base64,{logo_b64}" style="height:60px;">'
    logo_white = f'<img src="data:image/png;base64,{logo_b64}" style="height:48px;filter:brightness(0) invert(1);">'
else:
    logo_html  = f'<span style="font-family:Playfair Display,serif;font-size:1.8rem;font-weight:700;color:{NAVY};">Confini</span>'
    logo_white = f'<span style="font-family:Playfair Display,serif;font-size:1.5rem;font-weight:700;color:{WHITE};">Confini</span>'

st.markdown(f"""
<div style="padding:16px 0 10px 0;">{logo_html}</div>
<hr style="border:none;border-top:2px solid {BRIGHT};margin:0 0 28px 0;">
""", unsafe_allow_html=True)


# ─── PARAMETRI ───────────────────────────────────────────────────────────────
with st.expander("⚙️ Parametri simulazione", expanded=True):
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        capitale = st.slider("Capitale iniziale (€)", 10_000, 500_000, 100_000, step=5_000, format="€%d")
    with col_s2:
        anni = st.slider("Orizzonte temporale (anni)", 5, 40, 20)
    with col_s3:
        inflazione = st.slider("Inflazione annua stimata (%)", 1.0, 6.0, 2.5, step=0.25) / 100
    with col_s4:
        rend_etf = st.slider("Rendimento lordo ETF annuo (%)", 3.0, 12.0, 6.5, step=0.25) / 100

    col_s5, col_s6, _, __ = st.columns(4)
    with col_s5:
        costo_etf = st.slider("Costo medio ETF (%)", 0.05, 0.5, 0.2, step=0.05) / 100
    with col_s6:
        tasso_conto = st.slider("Rendimento conto corrente (%)", 0.0, 2.0, 0.0, step=0.1) / 100

    st.caption("I dati sono puramente simulativi e non costituiscono consulenza finanziaria.")


# ─── CALCOLI ─────────────────────────────────────────────────────────────────
mesi = anni * 12
r_etf_netto = (rend_etf - costo_etf) / 12

# ETF: crescita nominale
def simula_etf():
    saldo = capitale
    storia = [saldo]
    for _ in range(mesi):
        saldo = saldo * (1 + r_etf_netto)
        storia.append(round(saldo, 2))
    return storia

# Conto corrente: nominalmente fermo (o con minimo rendimento)
def simula_conto():
    saldo = capitale
    storia = [saldo]
    r_mensile = tasso_conto / 12
    for _ in range(mesi):
        saldo = saldo * (1 + r_mensile)
        storia.append(round(saldo, 2))
    return storia

# Potere d'acquisto del conto corrente: eroso dall'inflazione
def simula_potere_acquisto():
    saldo = capitale
    storia = [saldo]
    r_mensile = (tasso_conto - inflazione) / 12
    for _ in range(mesi):
        saldo = saldo * (1 + r_mensile)
        storia.append(round(saldo, 2))
    return storia

# ETF in termini reali (al netto inflazione)
def simula_etf_reale():
    saldo = capitale
    storia = [saldo]
    r_mensile = (rend_etf - costo_etf - inflazione) / 12
    for _ in range(mesi):
        saldo = saldo * (1 + r_mensile)
        storia.append(round(saldo, 2))
    return storia

storia_etf            = simula_etf()
storia_conto          = simula_conto()
storia_potere         = simula_potere_acquisto()
storia_etf_reale      = simula_etf_reale()

finale_etf            = storia_etf[-1]
finale_conto          = storia_conto[-1]
finale_potere         = storia_potere[-1]
finale_etf_reale      = storia_etf_reale[-1]

# Potere perso = capitale iniziale - potere d'acquisto finale del conto
potere_perso          = round(capitale - finale_potere, 2)
perc_potere_perso     = round((potere_perso / capitale) * 100, 2)
guadagno_etf_reale    = round(finale_etf_reale - capitale, 2)
vantaggio_etf_vs_conto = round(finale_etf - finale_conto, 2)

anni_range = [i / 12 for i in range(mesi + 1)]


# ─── HERO ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="hero-title">Non investire è la scelta più costosa che puoi fare.</div>
  <div class="hero-sub">
    Ogni anno che i tuoi risparmi restano fermi sul conto corrente,<br>
    l'inflazione li erode in silenzio. Il tempo lavora contro di te — o per te.
  </div>
</div>
""", unsafe_allow_html=True)


# ─── KPI ROW ─────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-label">Patrimonio finale<br>ETF (nominale)</div>
      <div class="kpi-value good">€ {fmt(finale_etf)}</div>
      <div class="kpi-sub">Rendimento netto: {fmt((rend_etf - costo_etf)*100)}% annuo</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card gray">
      <div class="kpi-label">Patrimonio finale<br>Conto Corrente</div>
      <div class="kpi-value gray">€ {fmt(finale_conto)}</div>
      <div class="kpi-sub">Rendimento: {fmt(tasso_conto*100)}% annuo</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card bad">
      <div class="kpi-label">Potere d'acquisto perso<br>tenendo i soldi fermi</div>
      <div class="kpi-value bad">− € {fmt(potere_perso)}</div>
      <div class="kpi-sub">{fmt(perc_potere_perso)}% del capitale eroso dall'inflazione</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-card gold">
      <div class="kpi-label">Vantaggio ETF<br>vs Conto Corrente</div>
      <div class="kpi-value gold">€ {fmt(vantaggio_etf_vs_conto)}</div>
      <div class="kpi-sub">In {anni} anni di investimento</div>
    </div>""", unsafe_allow_html=True)


# ─── QUOTE ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="quote-box">
  "Con un'inflazione del {fmt(inflazione*100)}% annuo, in {anni} anni
   i tuoi <strong>€ {fmt(capitale, 0)}</strong> sul conto corrente<br>
   valgono in realtà solo <strong>€ {fmt(finale_potere)}</strong>.
   Hai perso <strong>€ {fmt(potere_perso)}</strong> senza fare nulla."
</div>
""", unsafe_allow_html=True)


# ─── GRAFICO PRINCIPALE ───────────────────────────────────────────────────────
st.markdown(f'<div class="section-title">📈 Crescita del patrimonio nel tempo</div>', unsafe_allow_html=True)

fig = go.Figure()

# Area tra ETF e potere d'acquisto conto
fig.add_trace(go.Scatter(
    x=anni_range + anni_range[::-1],
    y=storia_etf + storia_potere[::-1],
    fill='toself',
    fillcolor='rgba(45,125,210,0.07)',
    line=dict(color='rgba(0,0,0,0)'),
    showlegend=False,
    hoverinfo='skip',
))

# Potere d'acquisto conto corrente (reale)
fig.add_trace(go.Scatter(
    x=anni_range,
    y=storia_potere,
    mode='lines',
    name='Potere d\'acquisto conto corrente',
    line=dict(color=RED_LOSS, width=3, dash='dash'),
))

# Conto corrente nominale
fig.add_trace(go.Scatter(
    x=anni_range,
    y=storia_conto,
    mode='lines',
    name='Conto corrente (nominale)',
    line=dict(color=GRAY, width=2, dash='dot'),
))

# ETF nominale
fig.add_trace(go.Scatter(
    x=anni_range,
    y=storia_etf,
    mode='lines',
    name='ETF – Consulenza Indipendente',
    line=dict(color=BRIGHT, width=4),
))

# Linea capitale iniziale
fig.add_trace(go.Scatter(
    x=anni_range,
    y=[capitale] * len(anni_range),
    mode='lines',
    name='Capitale iniziale',
    line=dict(color='#c0cce0', width=1.5, dash='dot'),
))

# Annotation vantaggio ETF vs conto nominale
anno_label = anni * 0.70
idx_label  = int(anno_label * 12)
y_center   = (storia_etf[idx_label] + storia_conto[idx_label]) / 2

fig.add_annotation(
    x=anno_label,
    y=y_center,
    text=f"<b>€ {fmt(vantaggio_etf_vs_conto)}<br>in più con ETF</b>",
    showarrow=False,
    font=dict(color=NAVY, size=15, family='Source Sans 3'),
    bgcolor='rgba(255,255,255,0.88)',
    borderwidth=0,
    borderpad=12,
    align='center',
)

fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Source Sans 3', color=NAVY),
    legend=dict(
        orientation='v',
        yanchor='middle', y=0.5,
        xanchor='left', x=1.02,
        font=dict(size=12),
        bgcolor='rgba(255,255,255,0.9)',
        borderwidth=0,
        itemwidth=30,
        traceorder='normal',
    ),
    xaxis=dict(
        title='Anni',
        gridcolor='#e8edf5',
        tickfont=dict(size=12),
        showline=True, linecolor='#dce4f0',
        range=[0, anni],
    ),
    yaxis=dict(
        title='Patrimonio (€)',
        gridcolor='#e8edf5',
        tickformat='€,.0f',
        tickfont=dict(size=12),
        showline=True, linecolor='#dce4f0',
    ),
    height=520,
    margin=dict(l=20, r=220, t=40, b=20),
    hovermode='x unified',
)

st.plotly_chart(fig, use_container_width=True)


# ─── GRAFICO EROSIONE POTERE D'ACQUISTO ──────────────────────────────────────
st.markdown(f'<div class="section-title">🔥 Potere d\'acquisto perso ogni anno tenendo i soldi fermi</div>', unsafe_allow_html=True)

erosione = [round(capitale - p, 2) for p in storia_potere]

fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=anni_range,
    y=erosione,
    mode='lines',
    fill='tozeroy',
    fillcolor='rgba(192,57,43,0.12)',
    line=dict(color=RED_LOSS, width=3),
    name='Potere d\'acquisto eroso',
))

fig2.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Source Sans 3', color=NAVY),
    xaxis=dict(title='Anni', gridcolor='#e8edf5', showline=True, linecolor='#dce4f0'),
    yaxis=dict(title='€ di potere d\'acquisto perso', tickformat='€,.0f', gridcolor='#e8edf5', showline=True, linecolor='#dce4f0'),
    height=300,
    margin=dict(l=20, r=20, t=20, b=20),
    showlegend=False,
)

for anno_check in range(5, anni + 1, 5):
    idx = anno_check * 12
    if idx < len(erosione):
        fig2.add_annotation(
            x=anno_check,
            y=erosione[idx],
            text=f"<b>− € {fmt(erosione[idx])}</b>",
            showarrow=True, arrowhead=1, arrowcolor=RED_LOSS,
            font=dict(color=RED_LOSS, size=11),
            ax=0, ay=-30,
            bgcolor='rgba(255,255,255,0.85)',
            borderwidth=0,
            borderpad=4,
        )

st.plotly_chart(fig2, use_container_width=True)


# ─── CARD CONCETTI ────────────────────────────────────────────────────────────
st.markdown(f'<div class="section-title">💡 Perché non fare nulla è una scelta sbagliata</div>', unsafe_allow_html=True)

cards = [
    ("📉", "L'inflazione è una tassa silenziosa", f"Con un'inflazione media del {fmt(inflazione*100)}% annuo, il tuo denaro perde potere d'acquisto ogni giorno. In {anni} anni, <b>€ {fmt(capitale, 0)}</b> sul conto valgono come <b>€ {fmt(finale_potere)}</b> di oggi.", RED_LOSS),
    ("⏳", "Il tempo è il tuo alleato — o il tuo nemico", f"La capitalizzazione composta funziona in entrambe le direzioni: <b>fa crescere</b> il capitale investito, ma <b>erode</b> quello fermo. Ogni anno di attesa ha un costo reale e misurabile.", NAVY),
    ("🟦", "Gli ETF battono l'inflazione nel lungo periodo", f"Storicamente, i mercati finanziari hanno reso il <b>6–8% annuo lordo</b> nel lungo periodo, ben al di sopra dell'inflazione. Con la consulenza indipendente accedi a questi strumenti a costi minimi.", BRIGHT),
    ("🏦", "Il conto corrente non è un investimento", f"Tenere i soldi in banca dà l'<b>illusione della sicurezza</b>. Il saldo nominale non cambia, ma il suo valore reale diminuisce ogni anno. La vera sicurezza è preservare e far crescere il potere d'acquisto.", GOLD),
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


# ─── CHIUSURA ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg,{NAVY},{BLUE});border-radius:16px;padding:40px 48px;margin-top:40px;color:{WHITE};text-align:center;">
  <div style="font-family:'Playfair Display',serif;font-size:1.9rem;font-weight:700;margin-bottom:16px;">
    Ogni giorno che aspetti ha un prezzo.<br>Il prezzo si chiama inflazione.
  </div>
  <div style="font-size:1.05rem;color:rgba(255,255,255,0.8);max-width:640px;margin:0 auto;line-height:1.7;">
    Investire non è speculare. È proteggere il valore del tuo lavoro nel tempo.<br>
    Con la consulenza indipendente lo fai in modo trasparente, efficiente e senza conflitti d'interesse.
  </div>
  <div style="margin-top:28px;display:flex;justify-content:center;">
    {logo_white}
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="footer">
  I dati e le proiezioni mostrate sono puramente simulativi con finalità illustrative.
  Non costituiscono consulenza finanziaria, offerta di investimento o promozione di prodotti finanziari.
  Rendimenti passati non garantiscono risultati futuri. © Confini
</div>
""", unsafe_allow_html=True)