from colors import FARBEN_4_ABSTUFUNGEN

GLOBAL = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&display=swap');
  @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700;9..144,900&family=DM+Sans:wght@400;500;600&display=swap');
  html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
  .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
  h3 { font-size: 1rem !important; font-weight: 600 !important; }
  .kpi-box {
    background: white; border: 1px solid #e2ddd4;
    padding: 18px 20px; border-radius: 2px; margin-bottom: 4px;
  }
  .kpi-label { font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; color: #7a7269; margin-bottom: 6px; }
  .kpi-value { font-size: 2rem; font-weight: 700; color: #1a1a2e; line-height: 1; margin-bottom: 5px; }
  .kpi-up   { color: #4c7a3a; font-size: 0.76rem; font-weight: 500; }
  .kpi-down { color: #b24d24; font-size: 0.76rem; font-weight: 500; }
  .section-title {
    font-size: 0.68rem; font-weight: 600; letter-spacing: 0.14em;
    text-transform: uppercase; color: #7a7269;
    border-bottom: 1px solid #e2ddd4; padding-bottom: 6px; margin: 8px 0 4px;
  }
  .sample-size {
      font-size: 0.68rem;
      font-weight: 600;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: #7a7269;
      margin-top: 12px;
      display: flex;
      justify-content: flex-end;
  }

:root {
    --bg: #f5ebe0;
    --card: #ffffff;
    --border: #e8dfd2;
    --text: #1a1d24;
    --muted: #6b7280;
    --accent-red: #b24d24;
    --accent-yellow: #c48a2a;
    --accent-blue: "#3c699a";
    --accent-green: #4c7a3a;
}

[class*="st-key-karte"] {
    background-color: white;
    border-radius: 10px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

/* Footer */
footer{padding:40px 0;border-top:1px solid rgba(148,163,184,.12);color:var(--muted)}

.footer-logos {
display: flex;
justify-content: center;
align-items: center;
gap: 2.5rem;
flex-wrap: wrap;
margin-bottom: 0.5rem;
}

.footer-logos img {
height: 70px;
max-width: 140px;
object-fit: contain;
opacity: 0.9;
filter: grayscale(40%);
transition: filter 0.3s ease, transform 0.3s ease, opacity 0.3s ease;
}

.footer-logos img:hover {
opacity: 1;
filter: grayscale(0%);
transform: scale(1.05);
}

.footer-bottom {
display: flex;
justify-content: space-between;
gap: 1rem;
flex-wrap: wrap;
width: 100%;
}




.stat-label {
    font-size: 0.7rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--muted);
    margin: 0 0 0.9rem 0;
}

.stat-number {
    font-family: "Fraunces", serif;
    font-variation-settings: "opsz" 144;
    font-weight: 700;
    font-size: 5.5rem;
    line-height: 0.9;
    letter-spacing: -0.02em;
    margin: 0;
    color: var(--text);
}

.stat-number .percent {
    font-size: 3rem;
    font-weight: 600;
    color: var(--accent-yellow);
    vertical-align: top;
    margin-left: 0.1em;
}

.stat-description {
    margin: 0.4rem 0 0 0;
    font-size: 0.92rem;
    line-height: 1.4;
    opacity: 0.85;
}
</style>
"""