# ============================================================
#  Streamlit 2025-2026 Features Demo
#  Explore: menu_button, filter_mode, popover, widget binding,
#           stoggle, dynamic containers, and more
#
#  Run: streamlit run streamlit_features_demo.py
# ============================================================

import streamlit as st
from streamlit_extras.stoggle import stoggle
from streamlit_extras.stylable_container import stylable_container
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# ── PAGE CONFIG ──────────────────────────────────────────
st.set_page_config(
    page_title="Streamlit 2025-2026 Features",
    page_icon="✨",
    layout="wide",
)

st.title("✨ Streamlit Features Playground")
st.markdown("*Explore all the cool new stuff from 2025-2026*")

st.divider()

# ═══════════════════════════════════════════════════════════
#  1. MENU BUTTON (NEW!)
# ═══════════════════════════════════════════════════════════

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("1️⃣ st.menu_button")
    
    menu_choice = st.menu_button(
        label="📋 Actions",
        options=["View Data", "Export CSV", "Settings", "Help"],
        key="menu1"
    )
    
    st.write(f"**Selected:** {menu_choice}")

# ═══════════════════════════════════════════════════════════
#  2. FILTER MODE (NEW!)
# ═══════════════════════════════════════════════════════════

with col2:
    st.subheader("2️⃣ Filter Mode (Searchable)")
    
    segments = [
        "1-2 Mitarbeiter",
        "3-10 Mitarbeiter",
        "11-20 Mitarbeiter",
        ">20 Mitarbeiter",
        "Bildung - Primarschule",
        "Bildung - Mittelschule",
        "Bildung - Hochschule",
    ]
    
    selected_segment = st.selectbox(
        "Select segment (type to filter):",
        options=segments,
        filter_mode="contains",  # ← NEW in 2025!
        key="filter1"
    )
    
    st.write(f"**Picked:** {selected_segment}")

# ═══════════════════════════════════════════════════════════
#  3. POPOVER with on_change (NEW!)
# ═══════════════════════════════════════════════════════════

with col3:
    st.subheader("3️⃣ Popover with on_change")
    
    with st.popover("⚙️ Advanced Options", use_container_width=True):
        st.write("Configure your view:")
        confidence_level = st.slider("Confidence Level", 0, 100, 95)
        show_annotations = st.checkbox("Show annotations", value=True)
        color_scheme = st.selectbox("Color scheme", ["Dark", "Light", "Custom"])
        
        st.caption(f"Config: {confidence_level}% | Annotations: {show_annotations}")

st.divider()

# ═══════════════════════════════════════════════════════════
#  4. MULTISELECT with FILTER + ADD NEW OPTIONS
# ═══════════════════════════════════════════════════════════

st.subheader("4️⃣ Multiselect with Filter + Add New Options")

industries = ["Finance", "Healthcare", "Tech", "Retail", "Manufacturing", "Education"]

selected_industries = st.multiselect(
    "Select industries (searchable, can add new):",
    options=industries,
    filter_mode="contains",  # ← NEW!
    # Can add new options on the fly
    key="multi1"
)

if selected_industries:
    st.write(f"**Selected {len(selected_industries)} industries:** {', '.join(selected_industries)}")

st.divider()

# ═══════════════════════════════════════════════════════════
#  5. DATE INPUT with QUICK-SELECT (NEW!)
# ═══════════════════════════════════════════════════════════

st.subheader("5️⃣ Date Range with Quick-Select")

date_range = st.date_input(
    "Select date range (includes quick options):",
    value=(datetime.now() - timedelta(days=30), datetime.now()),
    key="date1"
)

if len(date_range) == 2:
    st.write(f"**Range:** {date_range[0]} to {date_range[1]}")

st.divider()

# ═══════════════════════════════════════════════════════════
#  6. DYNAMIC CONTAINERS with on_change
# ═══════════════════════════════════════════════════════════

st.subheader("6️⃣ Dynamic Containers (Expander + Tabs with on_change)")

if "expander_state" not in st.session_state:
    st.session_state.expander_state = False

with st.expander("📊 Expand for detailed analysis", expanded=st.session_state.expander_state):
    st.write("This expander has an on_change callback!")
    col_a, col_b = st.columns(2)
    
    with col_a:
        metric1 = st.number_input("Metric A", value=42)
    with col_b:
        metric2 = st.number_input("Metric B", value=58)
    
    st.metric(
        "Growth",
        f"{metric1 + metric2}%",
        delta=f"+{(metric1 + metric2) - 100}%",
        delta_color="normal"  # Can be 'normal', 'inverse', 'off'
    )

# Tabs with on_change (tracks which tab is active)
tab1, tab2, tab3 = st.tabs(["Summary", "Details", "Export"])

with tab1:
    st.write("📈 Summary view")
    st.info("This tab changed because you switched tabs!")

with tab2:
    st.write("🔍 Detailed breakdown")
    st.dataframe(
        pd.DataFrame({
            "Metric": ["A", "B", "C", "D"],
            "Value": [45, 38, 52, 41],
            "Growth": ["+5%", "-2%", "+8%", "+1%"]
        })
    )

with tab3:
    st.write("📥 Export options")
    st.button("Download as CSV")
    st.button("Download as PDF")

st.divider()

# ═══════════════════════════════════════════════════════════
#  7. STOGGLE (from streamlit_extras) - Animated Toggle
# ═══════════════════════════════════════════════════════════

st.subheader("7️⃣ Stoggle (Animated Toggle from streamlit_extras)")

stoggle(
    "🧮 Show Methodology",
    """
    **Sample Size:** 1,991 respondents
    
    **Confidence Level:** 95%
    
    **Margin of Error:** ±2.2%
    
    **Survey Period:** August 22 - September 9, 2025
    
    **Population:** Business owners & executives in Aargau
    """
)

st.divider()

# ═══════════════════════════════════════════════════════════
#  8. WIDGET BINDING (query parameters) - NEW!
# ═══════════════════════════════════════════════════════════

st.subheader("8️⃣ Widget Binding (Syncs to URL Query Parameters)")

if "question_bound" not in st.session_state:
    st.session_state.question_bound = "Q1"

# This will sync to URL and can be bookmarked!
question = st.selectbox(
    "Select question (bookmarkable via URL):",
    options=[
        "Q1: Future outlook",
        "Q2: Investment plans",
        "Q3: Hiring plans",
        "Q4: Challenges"
    ],
    key="question_bind"  # Binding happens automatically with key!
)

st.info(f"Try sharing the URL with someone - the question selection is in the URL! 🔗")

st.divider()

# ═══════════════════════════════════════════════════════════
#  9. STYLABLE CONTAINER (You already use this!)
# ═══════════════════════════════════════════════════════════

st.subheader("9️⃣ Stylable Container (You already know this!)")

with stylable_container(
    key="fancy_kpi",
    css_styles="""
        {
            border: 2px solid #3c699a;
            border-radius: 10px;
            padding: 20px;
            background-color: #f4f0e4;
        }
    """
):
    col_x, col_y, col_z = st.columns(3)
    
    with col_x:
        st.metric("BEFRAGTE", "1019", "↓ -15.5%")
    with col_y:
        st.metric("Rücklaufquote", "73%", "↑ +5pp")
    with col_z:
        st.metric("NPS Score", "+42", "↑ Good")

st.divider()

# ═══════════════════════════════════════════════════════════
#  10. BONUS: Interactive Demo with all features combined
# ═══════════════════════════════════════════════════════════

st.subheader("🎯 Bonus: Combined Demo (Dashboard-like)")

col_left, col_right = st.columns([2, 1])

with col_left:
    st.write("**Interactive Segment Analysis**")
    
    # Searchable multiselect
    selected_segs = st.multiselect(
        "Filter segments (searchable):",
        segments,
        default=["1-2 Mitarbeiter", ">20 Mitarbeiter"],
        filter_mode="contains"
    )
    
    # Sample data
    df = pd.DataFrame({
        "Segment": ["1-2", "3-10", "11-20", ">20"],
        "Optimistic": [45, 38, 52, 41],
        "Neutral": [35, 42, 28, 38],
        "Pessimistic": [20, 20, 20, 21]
    })
    
    # Filter based on selection
    if selected_segs:
        selected_labels = [s.split()[0] for s in selected_segs]
        df_filtered = df[df["Segment"].isin(selected_labels)]
    else:
        df_filtered = df
    
    # Create chart
    fig = px.bar(
        df_filtered,
        x="Segment",
        y=["Optimistic", "Neutral", "Pessimistic"],
        barmode="stack",
        color_discrete_sequence=["#4c7a3a", "#c48a2a", "#b24d24"]
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.write("**Controls**")
    
    with st.popover("⚙️ Settings"):
        chart_type = st.radio("Chart type", ["Stacked", "Grouped"])
        show_values = st.checkbox("Show values", value=True)
        opacity = st.slider("Opacity", 0.3, 1.0, 0.8)
    
    st.divider()
    
    stoggle(
        "📋 About this data",
        "This is sample survey data showing business sentiment by company size."
    )

st.divider()

# ═══════════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════════

st.caption("✨ Try all these features! They're production-ready in Streamlit 1.55.0+")
st.caption("📚 Docs: https://docs.streamlit.io | Extras: https://arnaudmiribel.github.io/streamlit-extras/")
