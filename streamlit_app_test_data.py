# ============================================================
#  Marktforschungs-Dashboard v2 · Streamlit + Plotly
#  Enthält: Linie, Donut, Stacked Bar, Spider/Radar,
#           Heatmap, Bubble, Sankey, Balken, Zufriedenheit
#
#  Installation:  pip install streamlit plotly pandas
#  Starten:       streamlit run
# ============================================================

import os
from pathlib import Path
import pyreadstat
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import numpy as np
from colors import C_LIST, GFS_BLUE, CREME_FARBE
from global_css import GLOBAL
from header import header
import helpers as h
from KpiRenderer import KpiRenderer
import pickle
import plotly.express as px
from single_barchart import create_barchart
from stacked_barchart import create_stacked_bar
import HandleMeta
from HandleMeta import load_metatable
from environment import IN_GFS
import altair as alt
from pie_chart import create_piechart
from big_number import big_number
from footer import footer
import plotly.express as px
from card_handler import CardHandler
from crunch_label import give_crunch_label
from density_chart import create_density_plot
cards = CardHandler()

if IN_GFS:
    os.chdir(Path(__file__).parent)
    
df, meta = pyreadstat.read_sav("survey.sav")

# Nur wenn man im gfs environment ist, und zugang auf den Hintergrund-Code hat, kann man den metatable laden.
# Wenn man das nicht hat, muss man eine (broken) eigenfunktion verwenden, welche die Labels über meta holt. (siehe HandleMeta)
# Dort kann man auch IN_GFS auf True oder False setzen

if IN_GFS:
    metatable = load_metatable()


# ── SEITEN-KONFIGURATION ────────────────────────────────────
st.set_page_config(
    page_title="gfs-Dashboard",
    page_icon="gfs.png",
    layout="wide",
)

# ── GLOBALES CSS ─────────────────────────────────────────────
st.markdown(GLOBAL, unsafe_allow_html=True)

st.markdown(h.set_background(hex_color=CREME_FARBE[1]), unsafe_allow_html=True)

# ── HEADER ──────────────────────────────────────────────────
st.markdown(
    header(
        title="TEST DATA ON HEALTH",
        subtitle="Zentrale Kennzahlen, Verhaltensmuster und Trends auf einen Blick. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.",
        year=2026,
        window="Marktforschungs-Dashboard",
    ),
    unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  KPI-KARTEN
# ══════════════════════════════════════════════════════════
kpi = KpiRenderer(df)
kpi.render_section_title()

k1, k2, k3, k4 = st.columns(4)

# kpi.anzahl_befragte_mit_jahr(k1)

# kpi.render(k1, "Stichprobengrösse", "1019", "+5 % Gegenüber dem letzten Jahr", "up")
# kpi.render(k2, "Methode", "MIXED", "10% weniger CATI als letztes Jahr (50/50)", "down")
# kpi.bearbeitungszeit(k3, "überdurschnittliche Zeit", "up")
# kpi.render(k4, "Befragungszeitraum", "18 Tage", "von 3. - 21.  November", "down")

st.divider()
# ══════════════════
# ══════════════════════════════════════════════════════════
#  GFS1_1 · MITTELWERTE NACH JAHR
# ══════════════════════════════════════════════════════════


b1, b2 = st.columns([1.5, 2.5])

with b1:
    with st.container(key="karte2"):
        h.set_subtle_title(st, "source", "Mittelwerte nach Break")
        st.subheader(HandleMeta.get_column_label(meta, "source"))

        break_options = {
            "Kein Break": "tz",
            "Geschlecht": "sex",
            "Alter": "agegp3",
            "Geheirated": "marital",
            "Kinder": "child",
            "Bildung": "educ",
            "Raucher": "smoke"
        }

        selected_break_label = st.selectbox(
            "Break auswählen",
            list(break_options.keys())
        )
        current_break = break_options[selected_break_label]

        fig = create_barchart(df, meta, "source", current_break, horizontal=False, color_gradient="categories", height=335)
        st.plotly_chart(fig, use_container_width=True)
        h.set_sample_size(st, col="source", meta=meta, df=df)


# ── PieChart ──────────────────────────────────────────────────

b2_1, b2_2 = b2.columns([2, 1])

with b2_2:
    with st.container(key="karte5"):
        h.set_subtle_title(st, "Stichprobenzusammensetzung", "Piechart")
        # p2_1, p2_2, p2_3 = st.columns(3)
        st.text("Geschlecht")
        fig = create_piechart(df, meta, "sex", height=120)
        st.plotly_chart(fig, use_container_width=True)
        st.text("Bildung")
        fig = create_piechart(df, meta, "edu", height=120)
        st.plotly_chart(fig, use_container_width=True)
        st.text("Alter")
        fig = create_piechart(df, meta, "agegp3", height=120)
        st.plotly_chart(fig, use_container_width=True)


# ── Another chart ──────────────────────────────────────────────────
b2_11, b2_22 = b2_1.columns([1, 1])


big_number(b2_11, "educrec", "Kommunikation der Gemeinde", "22", "... sind nicht oder überhaupt nicht zufrieden", color="grün", add_percent=True, height=280)
big_number(b2_22, "educrec", "Kommunikation der Gemeinde", "39", "... nutzen Social Media-Kanäle nicht", color="gelb", add_percent=True, height=280)

fig = create_barchart(df, meta, "educrec", "tz", color="gelb", horizontal=True)

# b2_1.plotly_chart(fig, use_container_width=True)


# ── Big Number Card ──────────────────────────────────────────────────
n2_1, n2_2 = b2.columns([1, 1])


# ── Stacked Bar Chart ──────────────────────────────────────────────────


with b2_1.container(key="karte6"):
    h.set_subtle_title(st, "educrec", "Stacked Barchart")
    st.subheader(HandleMeta.get_column_label(meta, "educrec"))
    fig = create_stacked_bar(df, meta, "educrec", height=140)
    st.plotly_chart(fig, use_container_width=True)
    h.set_sample_size(st, col="educrec", meta=meta, df=df)


# ──  Bar With Slider ──────────────────────────────────────────────────

h1, h2 = st.columns([1, 1])

with h1.container(key="karte8"):
    h.set_subtle_title(st, "toptim", "Stacked Barchart")
    st.subheader(HandleMeta.get_column_label(meta, "toptim"))
    min_age, max_age = st.slider(
        "Gemeindegrösse wählen",
        min_value=int(df["age"].min()),
        max_value=int(df["age"].max()),
        value=(int(df["age"].min()), int(df["age"].max())),
        step=1,
        help="Nur Personen in diesee Gemeindegrösse werden angezeigt"
    )

    filtered_df = df[
        (df["age"] >= min_age) &
        (df["age"] <= max_age)
    ].reset_index(drop=True)

    fig = create_density_plot(filtered_df, meta, "toptim", color = "gelb")
    st.plotly_chart(fig, use_container_width=True)
    h.set_sample_size(st, col="toptim", meta=meta, df=filtered_df)


with h2.container(key="karte9"):
    h.set_subtle_title(st, "source", "Different Charts")
    tab1, tab2, tab3 = st.tabs(["Bar Chart", "Stacked Bar Chart", "Pie Chart"])
    with tab1:
        fig = create_barchart(df, meta, "source", current_break=None, horizontal=False, color_gradient="categories", height=200, crunch_label_by=10)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        fig = create_stacked_bar(df, meta, "source", height=200, crunch_label_by=10)
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        fig = create_piechart(df, meta, "smoke", height=200)
        st.plotly_chart(fig, use_container_width=True)

    h.set_sample_size(st, col="smoke", meta=meta, df=df)


with h2.container(key="karte10"):
    h.set_subtle_title(st, "source", "Different Charts")
    st.subheader("Falls Sie die folgenden Kommunikationskanäle Ihrer Gemeinde bzw. Stadt nutzen: Wie zufrieden sind Sie damit?")
    tab1, tab2, tab3, tab4 = st.tabs(["Webseite", "Social Media-Kanäle", "Mitteilungsblatt/Gemeindeblatt", "Newsletter per E-Mail"])
    with tab1:
        st.subheader("Webseite der Gemeinde/Stadt")
        fig = create_barchart(df, meta, "source", color_gradient="categories", height=260, crunch_label_by=10)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Social Media-Kanäle der Gemeinde/Stadt")
        fig = create_barchart(df, meta, "source", color_gradient="categories", height=260, crunch_label_by=11)
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("Mitteilungsblatt/Gemeindeblatt")
        fig = create_barchart(df, meta, "source", color_gradient="categories", height=260, crunch_label_by=12)
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.subheader("Newsletter per E-Mail")
        fig = create_barchart(df, meta, "source", color_gradient="categories", height=260, crunch_label_by=13)
        st.plotly_chart(fig, use_container_width=True)

    h.set_sample_size(st, col="source", meta=meta, df=df)

# ── FOOTER ──────────────────────────────────────────────────

st.divider()

st.html(footer(
    logos=["gfs.png", "uni.png", "kmu.png"]
))
st.caption("gfs-Demo-Dashboard · Daten nicht akkurat · Erstellt von Lisa Gehrig · 22.04.2026")
