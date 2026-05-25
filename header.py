from html import escape
from colors import C, GFS_BLUE, FARBEN_4_ABSTUFUNGEN
import base64


def header(title=None, subtitle=None, year=None, window=None, icon = None):
    title = escape(title or "Untitled Dashboard")
    subtitle = escape(subtitle or "")
    year = escape(str(year or "2026"))
    window = escape(window or "Marktforschung")

    if icon is None: 
      with open("gfs.png", "rb") as f:
          gfs_b64 = base64.b64encode(f.read()).decode("utf-8")
    else:
      with open(icon, "rb") as f:
        gfs_b64 = base64.b64encode(f.read()).decode("utf-8")

    subtitle_block = f"""
<div style="
  font-size: 0.80rem;
  letter-spacing: 0.08em;
  color: #7a7269;
  margin-bottom: 6px;
  font-weight: 600;
"><br>
  {subtitle}
</div>
""" if subtitle else ""

    return f"""
<div style="
background: #ffffff;
border: 0px solid {FARBEN_4_ABSTUFUNGEN["blau"]["sehr_dunkel"]};
border-radius: 2px;
padding: 34px 56px 28px 56px;
margin-bottom: 22px;
box-shadow: 0 10px 30px rgba(80, 60, 40, 0.20);
">

<!-- Horizontale Zeile: Text links, Logo rechts -->
<div style="
display: flex;
flex-direction: row;
align-items: center;
gap: 20px;
">

<!-- Linke Spalte: Badge + Titel + Subtitle -->
<div style="
flex: 1 1 auto;
min-width: 0;
display: flex;
flex-direction: column;
align-items: flex-start;
">

<div style="
display: inline-flex;
align-items: center;
gap: 8px;
font-size: 0.72rem;
font-weight: 700;
letter-spacing: 0.12em;
text-transform: uppercase;
color: {GFS_BLUE[0]};
background: {GFS_BLUE[9]};
padding: 7px 12px;
border-radius: 999px;
margin-bottom: 14px;
width: fit-content;
">
<span>{window}</span>
<span style="opacity: 0.45;">•</span>
<span>Schweiz {year}</span>
</div>

<div style="
font-size: 2.5rem;
font-weight: 700;
color: {C['dunkel']};
line-height: 1.08;
letter-spacing: 0.02em;
margin: 0;
">
{title}
</div>

{subtitle_block}

</div>

<!-- Rechte Spalte: Logo -->
<div style="
flex: 0 0 auto;
display: flex;
align-items: center;
">
<img src="data:image/png;base64,{gfs_b64}" alt="GFS" style="
max-height: 110px;
width: auto;
display: block;
object-fit: contain;
border-radius: 12px;
">
</div>


</div>
"""