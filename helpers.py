import HandleMeta
import pandas as pd

def set_background(hex_color="#f4f0e4"):
    return f"""
<style>
.stApp {{
    background-color: {hex_color};
}}
</style>
"""

def set_subtle_title(st, variable, text):
    st.markdown(f'<div class="section-title">{variable} · {text}</div>', unsafe_allow_html=True)
    

def set_sample_size(st, n=None, df=None, col=None, meta=None):
    if n is None:
        # Berechne n wie in create_stacked_bar
        col_labels = HandleMeta.get_value_labels(meta, col)
        
        if col_labels != {}:
            
            # Echte Skalen-Codes (SPSS-Sentinels raus)
            scale = {k: v for k, v in col_labels.items() if k < 99999990}
            
            # Total berechnen
            counts = [int((df[col] == k).sum()) for k in scale.keys()]
            n = sum(counts)
        else:
            n = df[col].notna().sum()                          # nur System-Missings raus
            n = df.loc[df[col] < 99999990, col].notna().sum() # auch SPSS-Sentinels raus

        
    """Zeigt die Stichprobengröße unten rechts an"""
    st.markdown(f'<div class="sample-size">N = {n}</div>', unsafe_allow_html=True)


def hex_to_rgba(hex_code: str, alpha = 1.0) -> str:
    hex_code = hex_code.lstrip("#")

    if len(hex_code) == 3:
        hex_code = "".join(c * 2 for c in hex_code)

    if len(hex_code) == 8:
        r, g, b = (int(hex_code[i:i+2], 16) for i in (0, 2, 4))
        alpha = int(hex_code[6:8], 16) / 255
    elif len(hex_code) == 6:
        r, g, b = (int(hex_code[i:i+2], 16) for i in (0, 2, 4))
    else:
        raise ValueError(f"Ungültiger Hex-Code: {hex_code}")

    return f"rgba({r},{g},{b},{alpha})"


def clean_plot_array(df, cols, drop_sentinels=True, clean_item_value_labels=None,
                     drop_na=True, drop_codes=None):
    single = isinstance(cols, str)
    cols = [cols] if single else list(cols)
    plot_df = df[cols].copy()

    if drop_na:
        plot_df = plot_df.dropna()
    if drop_codes:
        plot_df = plot_df[~plot_df.isin(drop_codes).any(axis=1)]
    if drop_sentinels:
        plot_df = plot_df[(plot_df < 99999990).all(axis=1)]
    if clean_item_value_labels:
        primary = cols[0]
        plot_df = plot_df[plot_df[primary].isin(clean_item_value_labels.keys())]

    return plot_df[cols[0]] if single else plot_df


def clean_value_labels(value_labels, drop_senitels=True, drop_codes = []):
    if drop_senitels:
        value_labels = {k: v for k, v in value_labels.items() if k < 99999990}
    if drop_codes != []:
        value_labels = {k: v for k, v in value_labels.items() if k not in drop_codes}
    return value_labels



def apply_weighting(df, weight_col):
    pass
    