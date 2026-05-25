# ============================================================
#  SEGMENT COMPARISON SLIDER
#  Side-by-side segment comparison with smooth blending
# ============================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_extras.stoggle import stoggle
import numpy as np

st.set_page_config(page_title="Segment Comparison", layout="wide")

st.title("🔄 Segment Comparison Slider")
st.markdown("*Compare any two segments side-by-side with smooth blending*")

# ── Sample data ──────────────────────────────────────────
segments_data = {
    "1-2 Mitarbeiter": {
        "response_1": [6.6, 7.7, 20.9, 20.7, 44.0],
        "response_2": [15, 35, 26, 45],
        "nps": 28,
        "sample_size": 312
    },
    "3-10 Mitarbeiter": {
        "response_1": [10, 15, 25, 30, 20],
        "response_2": [20, 30, 25, 25],
        "nps": 35,
        "sample_size": 450
    },
    "11-20 Mitarbeiter": {
        "response_1": [8, 12, 22, 28, 30],
        "response_2": [18, 32, 24, 26],
        "nps": 42,
        "sample_size": 380
    },
    ">20 Mitarbeiter": {
        "response_1": [5, 10, 18, 35, 32],
        "response_2": [12, 38, 28, 22],
        "nps": 52,
        "sample_size": 520
    },
}

response_options = [
    "Zukunftsaussichten",
    "Investitionspläne",
    "Einstellungspläne",
    "Herausforderungen"
]

# ── CONTROLS ─────────────────────────────────────────────

col_controls_1, col_controls_2, col_controls_3 = st.columns(3)

with col_controls_1:
    segment_a = st.selectbox(
        "Segment A (Links):",
        options=list(segments_data.keys()),
        index=0,
        filter_mode="contains"
    )

with col_controls_2:
    segment_b = st.selectbox(
        "Segment B (Rechts):",
        options=list(segments_data.keys()),
        index=3,
        filter_mode="contains"
    )

with col_controls_3:
    # SLIDER: Blend between segment A and B
    blend = st.slider(
        "Segment A ← → Segment B",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.01,
        key="blend_slider"
    )
    
    # Visual indicator
    if blend < 0.33:
        st.write("👈 Leaning A")
    elif blend > 0.67:
        st.write("👉 Leaning B")
    else:
        st.write("⚖️ Balanced")

st.divider()

# ── SIDE-BY-SIDE COMPARISON ──────────────────────────────

col_a, col_b = st.columns(2)

# Get data
data_a = segments_data[segment_a]
data_b = segments_data[segment_b]

# ── LEFT SIDE: Segment A ─────────────────────────────────

with col_a:
    st.subheader(f"📊 {segment_a}")
    
    # KPIs
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    
    with kpi_col1:
        st.metric("NPS Score", data_a["nps"], delta=f"vs {segment_b}: {data_a['nps'] - data_b['nps']:+d}")
    
    with kpi_col2:
        st.metric("Sample Size", data_a["sample_size"])
    
    with kpi_col3:
        avg_response = np.mean(data_a["response_2"])
        st.metric("Avg Response", f"{avg_response:.1f}")
    
    # Chart for Segment A
    fig_a = go.Figure(data=[
        go.Bar(
            x=["Sehr schlecht", "Schlecht", "Neutral", "Gut", "Sehr gut"],
            y=data_a["response_1"],
            marker_color="#3c699a",
            name=segment_a,
            text=data_a["response_1"],
            textposition="auto"
        )
    ])
    
    fig_a.update_layout(
        title=f"Zukunftsaussichten - {segment_a}",
        xaxis_title="",
        yaxis_title="Anteil (%)",
        height=400,
        showlegend=False,
        hovermode="x unified"
    )
    
    st.plotly_chart(fig_a, use_container_width=True)

# ── RIGHT SIDE: Segment B ────────────────────────────────

with col_b:
    st.subheader(f"📊 {segment_b}")
    
    # KPIs
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    
    with kpi_col1:
        st.metric("NPS Score", data_b["nps"], delta=f"vs {segment_a}: {data_b['nps'] - data_a['nps']:+d}")
    
    with kpi_col2:
        st.metric("Sample Size", data_b["sample_size"])
    
    with kpi_col3:
        avg_response = np.mean(data_b["response_2"])
        st.metric("Avg Response", f"{avg_response:.1f}")
    
    # Chart for Segment B
    fig_b = go.Figure(data=[
        go.Bar(
            x=["Sehr schlecht", "Schlecht", "Neutral", "Gut", "Sehr gut"],
            y=data_b["response_1"],
            marker_color="#b24d24",
            name=segment_b,
            text=data_b["response_1"],
            textposition="auto"
        )
    ])
    
    fig_b.update_layout(
        title=f"Zukunftsaussichten - {segment_b}",
        xaxis_title="",
        yaxis_title="Anteil (%)",
        height=400,
        showlegend=False,
        hovermode="x unified"
    )
    
    st.plotly_chart(fig_b, use_container_width=True)

st.divider()

# ── BLENDED VISUALIZATION ────────────────────────────────
# The slider blends the opacity between the two segments

st.subheader("🎨 Blended View (Move slider above)")

# Create blended data
blended_data_a = [x * (1 - blend) for x in data_a["response_1"]]
blended_data_b = [x * blend for x in data_b["response_1"]]

fig_blended = go.Figure(data=[
    go.Bar(
        x=["Sehr schlecht", "Schlecht", "Neutral", "Gut", "Sehr gut"],
        y=blended_data_a,
        marker_color=f"rgba(60, 105, 154, {(1-blend):.2f})",
        name=segment_a,
        text=[f"{x:.1f}%" for x in blended_data_a],
        textposition="inside"
    ),
    go.Bar(
        x=["Sehr schlecht", "Schlecht", "Neutral", "Gut", "Sehr gut"],
        y=blended_data_b,
        marker_color=f"rgba(178, 77, 36, {blend:.2f})",
        name=segment_b,
        text=[f"{x:.1f}%" for x in blended_data_b],
        textposition="inside"
    )
])

fig_blended.update_layout(
    barmode="stack",
    title="Blended Comparison (Slider-based weighting)",
    xaxis_title="",
    yaxis_title="Weighted Response (%)",
    height=450,
    hovermode="x unified"
)

st.plotly_chart(fig_blended, use_container_width=True)

st.divider()

# ── METHODOLOGY ──────────────────────────────────────────

stoggle(
    "📋 Methodology & Notes",
    f"""
    **Survey Details:**
    - Total respondents: {sum([data['sample_size'] for data in segments_data.values()])}
    - Survey period: August 22 - September 9, 2025
    - Population: Business owners & executives in Aargau
    
    **Comparison:**
    - **{segment_a}:** {data_a['sample_size']} respondents
    - **{segment_b}:** {data_b['sample_size']} respondents
    
    **Slider Effect:**
    The slider blends between the two segments' responses.
    At 0.5 (center), both segments are equally weighted.
    """,
)

st.caption("💡 Tip: The blend slider lets you visually compare how weighted combinations differ!")
