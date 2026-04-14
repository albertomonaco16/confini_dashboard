import streamlit as st
import plotly.graph_objects as go
import base64
import os

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Confini – Immobili vs Mercati Finanziari",
    page_icon="🏠",
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
TERRACOTTA = "#C47B3A"   # colore immobiliare / mattone

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
  .kpi-card.imm  {{ border-left-color: {TERRACOTTA}; }}
  .kpi-card.gold {{ border-left-color: {GOLD}; }}
  .kpi-card.red  {{ border-left-color: {RED_LOSS}; }}
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
  .kpi-value.imm  {{ color: {TERRACOTTA}; }}
  .kpi-value.good {{ color: {BRIGHT}; }}
  .kpi-value.gold {{ color: {GOLD}; }}
  .kpi-value.red  {{ color: {RED_LOSS}; }}
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


# ─── PARAMETRI ────────────────────────────────────────────────────────────────
with st.expander("⚙️ Parametri simulazione", expanded=True):
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        capitale = st.slider("Capitale disponibile (€)", 50_000, 1_000_000, 200_000, step=10_000, format="€%d")
    with col_s2:
        anni = st.slider("Orizzonte temporale (anni)", 5, 40, 20)
    with col_s3:
        versamento = st.slider("Risparmio mensile aggiuntivo (€)", 0, 5_000, 500, step=100, format="€%d")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    col_s4, col_s5, col_s6, col_s7 = st.columns(4)
    with col_s4:
        rend_etf = st.slider("Rendimento ETF annuo (%)", 3.0, 12.0, 7.0, step=0.25) / 100
    with col_s5:
        costo_etf = st.slider("Costo medio ETF (%)", 0.05, 0.5, 0.2, step=0.05) / 100
    with col_s6:
        apprezzamento_imm = st.slider("Apprezzamento immobile annuo (%)", 0.5, 5.0, 1.5, step=0.25) / 100
    with col_s7:
        rendita_lorda = st.slider("Rendita lorda da affitto annua (%)", 1.0, 6.0, 3.0, step=0.25) / 100

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    col_s8, col_s9, col_s10, _ = st.columns(4)
    with col_s8:
        spese_imm = st.slider("Spese annue immobile (% valore)", 0.5, 3.0, 1.5, step=0.25) / 100
    with col_s9:
        tassazione_affitto = st.slider("Tassazione rendita affitto (%)", 10.0, 30.0, 21.0, step=1.0) / 100
    with col_s10:
        costi_acquisto = st.slider("Costi acquisto immobile (% una tantum)", 5.0, 15.0, 9.0, step=0.5) / 100

    st.caption("I dati sono puramente simulativi e non costituiscono consulenza finanziaria.")


# ─── CALCOLI ─────────────────────────────────────────────────────────────────
mesi = anni * 12

# ── ETF ──
r_etf_netto = (rend_etf - costo_etf) / 12

def simula_etf(r_mensile):
    saldo = capitale
    storia = [saldo]
    for _ in range(mesi):
        saldo = saldo * (1 + r_mensile) + versamento
        storia.append(saldo)
    return storia

storia_etf = simula_etf(r_etf_netto)
finale_etf = round(storia_etf[-1], 2)

# ── IMMOBILE ──
# Capitale effettivamente investito nell'immobile (dopo costi acquisto)
capitale_imm = capitale * (1 - costi_acquisto)

# Rendita netta annua = rendita lorda - tassazione - spese
rendita_netta_annua_perc = rendita_lorda * (1 - tassazione_affitto) - spese_imm

# Simulazione anno per anno
def simula_immobile():
    valore = capitale_imm
    storia_val   = [capitale]        # valore immobile (iniziamo dal capitale lordo per confronto)
    storia_tot   = [capitale]        # valore + rendite cumulate reinvestite
    cassa = 0
    valore_confronto = capitale      # partiamo dallo stesso capitale per confronto equo

    storia = [valore_confronto]
    rendita_cum = 0

    for anno in range(anni):
        # Apprezzamento
        valore_confronto = valore_confronto * (1 + apprezzamento_imm)
        # Rendita netta dell'anno (calcolata sul valore di inizio anno)
        rendita_anno = valore_confronto * rendita_netta_annua_perc
        rendita_cum += rendita_anno
        # Versamenti mensili non possono essere investiti nell'immobile:
        # li accumuliamo separatamente senza rendimento (liquidità ferma)
        rendita_cum += versamento * 12
        storia.append(round(valore_confronto + rendita_cum, 2))

    return storia

storia_imm = simula_immobile()

# Allinea lunghezze per il grafico (immobile è annuale, ETF mensile)
anni_range_etf = [i / 12 for i in range(mesi + 1)]
anni_range_imm = list(range(anni + 1))

finale_imm = round(storia_imm[-1], 2)

diff = round(finale_etf - finale_imm, 2)
perc_diff = round((diff / finale_etf) * 100, 2)

# Rendimento medio annuo immobile (CAGR totale)
cagr_imm = round(((finale_imm / capitale) ** (1 / anni) - 1) * 100, 2)
cagr_etf = round(((finale_etf / capitale) ** (1 / anni) - 1) * 100, 2)


# ─── HERO ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="hero-title">Il mattone non è più l'investimento sicuro che pensi.</div>
  <div class="hero-sub">
    Bassa liquidità, costi nascosti, tassazione elevata e rendimenti reali deludenti.<br>
    I mercati finanziari, con la consulenza indipendente, fanno molto di meglio.
  </div>
</div>
""", unsafe_allow_html=True)


# ─── KPI ROW ─────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-label">Patrimonio finale<br>ETF (Consulenza Indipendente)</div>
      <div class="kpi-value good">€ {fmt(finale_etf)}</div>
      <div class="kpi-sub">CAGR stimato: {fmt(cagr_etf)}% annuo</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card imm">
      <div class="kpi-label">Patrimonio finale<br>Investimento Immobiliare</div>
      <div class="kpi-value imm">€ {fmt(finale_imm)}</div>
      <div class="kpi-sub">CAGR stimato: {fmt(cagr_imm)}% annuo</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card gold">
      <div class="kpi-label">Vantaggio ETF su {anni} anni</div>
      <div class="kpi-value gold">€ {fmt(diff)}</div>
      <div class="kpi-sub">In più rispetto all'immobile</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-card red">
      <div class="kpi-label">Potenziale non sfruttato</div>
      <div class="kpi-value red">{fmt(perc_diff)}%</div>
      <div class="kpi-sub">Del patrimonio finale lasciato sul tavolo</div>
    </div>""", unsafe_allow_html=True)


# ─── QUOTE ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="quote-box">
  "Con {fmt(capitale, 0)} € investiti oggi, in {anni} anni il mercato finanziario ti dà
  <strong>€ {fmt(finale_etf)}</strong>.<br>
   L'immobile ti dà <strong>€ {fmt(finale_imm)}</strong>.<br>
   La differenza è <strong>€ {fmt(diff)}</strong> — e non include i grattacapi da proprietario."
</div>
""", unsafe_allow_html=True)


# ─── GRAFICO PRINCIPALE ───────────────────────────────────────────────────────
st.markdown(f'<div class="section-title">📈 Crescita del patrimonio nel tempo</div>', unsafe_allow_html=True)

fig = go.Figure()

# Area tra le due curve
fig.add_trace(go.Scatter(
    x=anni_range_etf + anni_range_etf[::-1],
    y=storia_etf + [storia_imm[min(int(x), anni)] for x in anni_range_etf[::-1]],
    fill='toself',
    fillcolor='rgba(45,125,210,0.08)',
    line=dict(color='rgba(0,0,0,0)'),
    showlegend=False,
    hoverinfo='skip',
))

# Linea immobile (annuale)
fig.add_trace(go.Scatter(
    x=anni_range_imm,
    y=storia_imm,
    mode='lines+markers',
    name='Immobile',
    line=dict(color=TERRACOTTA, width=3, dash='dash'),
    marker=dict(size=6, color=TERRACOTTA),
))

# Linea ETF
fig.add_trace(go.Scatter(
    x=anni_range_etf,
    y=storia_etf,
    mode='lines',
    name='ETF Indipendente',
    line=dict(color=BRIGHT, width=4),
))

# Capitale versato
capitale_curve = [capitale + versamento * m for m in range(mesi + 1)]
fig.add_trace(go.Scatter(
    x=anni_range_etf,
    y=capitale_curve,
    mode='lines',
    name='Capitale versato',
    line=dict(color='#aab4cc', width=2, dash='dot'),
))

# Annotation differenza finale
fig.add_annotation(
    x=anni, y=(finale_etf + finale_imm) / 2,
    text=f"<b>€ {fmt(diff)}<br>in più con ETF</b>",
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
    ),
    yaxis=dict(
        title='Patrimonio (€)',
        gridcolor='#e8edf5',
        tickformat='€,.0f',
        tickfont=dict(size=12),
        showline=True, linecolor='#dce4f0',
    ),
    height=520,
    margin=dict(l=20, r=200, t=40, b=20),
    hovermode='x unified',
)

st.plotly_chart(fig, use_container_width=True)



# ─── PERCHÉ NON L'IMMOBILE ───────────────────────────────────────────────────
st.markdown(f'<div class="section-title">🏠 Perché l\'immobile delude nel lungo periodo</div>', unsafe_allow_html=True)

cards = [
    ("💸", "Costi nascosti che erodono il rendimento", f"Imposte di acquisto, notaio, agenzia, manutenzione, IMU, tassazione sugli affitti: i costi reali di un immobile si avvicinano spesso al <b>2-3% annuo</b> del suo valore, azzerando parte della rendita.", TERRACOTTA),
    ("🔒", "Capitale illiquido e non frazionabile", f"Con un immobile <b>immobilizzi tutto il capitale</b> in un unico asset. Non puoi disinvestire parzialmente, non puoi ribilanciare, non puoi reagire ai cambiamenti della vita senza vendere tutto.", RED_LOSS),
    ("📉", "Apprezzamento reale deludente", f"Al netto dell'inflazione, il valore reale degli immobili italiani è cresciuto in media meno dell'<b>1% annuo</b> nell'ultimo ventennio. I mercati finanziari hanno reso storicamente il <b>7-10% annuo</b>.", NAVY),
    ("⚡", "ETF: semplicità, liquidità, diversificazione", f"Con gli ETF investi in <b>migliaia di aziende nel mondo</b> con un solo strumento, costi minimi, nessuna burocrazia e liquidità immediata. Puoi vendere in secondi, non in mesi.", BRIGHT),
]

row1 = st.columns(2)
row2 = st.columns(2)
cols_cards = [row1[0], row1[1], row2[0], row2[1]]

for col, (icon, title, desc, color) in zip(cols_cards, cards):
    with col:
        st.markdown(f"""
        <div style="background:{WHITE};border-radius:14px;padding:28px 22px;box-shadow:0 2px 16px rgba(13,27,75,0.07);height:100%;border-top:4px solid {color};margin-bottom:16px;">
          <div style="font-size:2rem;margin-bottom:12px;">{icon}</div>
          <div style="font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:{NAVY};margin-bottom:10px;">{title}</div>
          <div style="font-size:0.9rem;color:#4a5a7a;line-height:1.6;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)


# ─── TABELLA COMPARATIVA ─────────────────────────────────────────────────────
st.markdown(f'<div class="section-title">⚖️ Confronto diretto</div>', unsafe_allow_html=True)

st.markdown("""
<table style="width:100%;border-collapse:collapse;font-family:'Source Sans 3',sans-serif;font-size:0.95rem;border-radius:12px;overflow:hidden;box-shadow:0 2px 16px rgba(13,27,75,0.07);">
  <thead>
    <tr style="background:#0D1B4B;color:#FFFFFF;">
      <th style="padding:14px 16px;text-align:left;">Caratteristica</th>
      <th style="padding:14px 16px;text-align:center;">🟦 ETF</th>
      <th style="padding:14px 16px;text-align:center;">🏠 Immobile</th>
    </tr>
  </thead>
  <tbody>
    <tr style="background:#FFFFFF;">
      <td style="padding:12px 16px;color:#4a5a7a;">Rendimento storico annuo</td>
      <td style="padding:12px 16px;color:#2D7DD2;font-weight:700;text-align:center;">7 – 10%</td>
      <td style="padding:12px 16px;color:#C47B3A;font-weight:700;text-align:center;">1 – 3%</td>
    </tr>
    <tr style="background:#F8FAFD;">
      <td style="padding:12px 16px;color:#4a5a7a;">Liquidità</td>
      <td style="padding:12px 16px;color:#2D7DD2;font-weight:700;text-align:center;">Immediata</td>
      <td style="padding:12px 16px;color:#C47B3A;font-weight:700;text-align:center;">Mesi / anni</td>
    </tr>
    <tr style="background:#FFFFFF;">
      <td style="padding:12px 16px;color:#4a5a7a;">Diversificazione</td>
      <td style="padding:12px 16px;color:#2D7DD2;font-weight:700;text-align:center;">Globale</td>
      <td style="padding:12px 16px;color:#C47B3A;font-weight:700;text-align:center;">Un solo asset</td>
    </tr>
    <tr style="background:#F8FAFD;">
      <td style="padding:12px 16px;color:#4a5a7a;">Costi di gestione</td>
      <td style="padding:12px 16px;color:#2D7DD2;font-weight:700;text-align:center;">~ 0,20%</td>
      <td style="padding:12px 16px;color:#C47B3A;font-weight:700;text-align:center;">~ 2 – 3%</td>
    </tr>
    <tr style="background:#FFFFFF;">
      <td style="padding:12px 16px;color:#4a5a7a;">Burocrazia</td>
      <td style="padding:12px 16px;color:#2D7DD2;font-weight:700;text-align:center;">Zero</td>
      <td style="padding:12px 16px;color:#C47B3A;font-weight:700;text-align:center;">Alta</td>
    </tr>
  </tbody>
</table>
""", unsafe_allow_html=True)


# ─── CHIUSURA EMOTIVA ─────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg,{NAVY},{BLUE});border-radius:16px;padding:40px 48px;margin-top:40px;color:{WHITE};text-align:center;">
  <div style="font-family:'Playfair Display',serif;font-size:1.9rem;font-weight:700;margin-bottom:16px;">
    Il mattone dà sicurezza psicologica.<br>I mercati finanziari danno risultati reali.
  </div>
  <div style="font-size:1.05rem;color:rgba(255,255,255,0.8);max-width:680px;margin:0 auto;line-height:1.7;">
    Non si tratta di demonizzare gli immobili. Si tratta di fare scelte consapevoli.<br>
    Con la consulenza indipendente hai accesso agli stessi strumenti dei grandi investitori
    istituzionali, a costi minimi, con la massima trasparenza.
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