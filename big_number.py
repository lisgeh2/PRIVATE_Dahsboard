from colors import C_LIST, GFS_BLUE, CREME_FARBE, FARBEN_4_ABSTUFUNGEN, FARBEN_4


def big_number(area, column, column_text, number, text, color="rot", add_percent=True, height = None):
    farben = FARBEN_4_ABSTUFUNGEN[color]
    if height:
        height = str(height)+"px"

    cls = f"stat-card accent-{color}"

    if add_percent:
        if type(add_percent)==str:
            area.html(
                f'<div class="{cls}">'
                f'<div class="section-title">{column} · {column_text}</div>'
                f'<p class="stat-number">{number}<span class="percent">{add_percent}</span></p>'
                f'<p class="stat-description">{text}</p>'
                '</div>'
            )
        else:         
            area.html(
                f'<div class="{cls}">'
                f'<div class="section-title">{column} · {column_text}</div>'
                f'<p class="stat-number">{number}<span class="percent">%</span></p>'
                f'<p class="stat-description">{text}</p>'
                '</div>'
            )
    else:
        area.html(
            f'<div class="{cls}">'
            f'<div class="section-title">{column} · {column_text}</div>'
            f'<p class="stat-number">{number}</p>'
            f'<p class="stat-description">{text}</p>'
            '</div>'
        )

    height_css = ""
    flex_css = ""
    
    if height is not None:
        height_css = f"height: {height};"
        flex_css = """display: flex;
        flex-direction: column;
        justify-content: space-between;"""

    area.html(f"""<style>
    .stat-card.accent-{color} {{
        --card:   #FFFFFF;
        --border: {farben['sehr_dunkel']};
        --accent: {farben['sehr_dunkel']};
        --text:   {farben['dunkel']};
        --muted:  {farben['hell']};

        background: var(--card);
        border: 5px solid var(--border);
        border-radius: 8px;
        padding: 1.75rem 2rem;
        position: relative;
        overflow: hidden;
        font-family: "DM Sans", -apple-system, sans-serif;
        color: var(--text);
        {height_css};
        {flex_css};
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15),
                    0 2px 4px rgba(0, 0, 0, 0.13);
    }}
    .stat-card.accent-{color}::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        background: var(--accent);
    }}
    .stat-card.accent-{color} .stat-label       {{ color: var(--muted); }}
    .stat-card.accent-{color} .stat-description {{ color: var(--muted); }}
    .stat-card.accent-{color} .percent          {{ color: var(--muted); }}
    .stat-card.accent-{color} .stat-number {{ text-align: center; }}
    </style>""")