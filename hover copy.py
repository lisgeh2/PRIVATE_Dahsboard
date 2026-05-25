import streamlit as st
import pandas as pd
import numpy as np

# Custom CSS to style the tabs to match the image
st.markdown("""
    <style>
    /* Hide default Streamlit padding adjustments if needed */
    .stTabs [data-baseweb="tab-list"] {
        gap: 32px;
        border-bottom: 2px solid #e0e0e0;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent;
        border-radius: 0;
        padding: 0 4px;
        font-size: 22px;
        font-weight: 400;
        color: #333333;
    }

    /* Active tab text color (red/coral) */
    .stTabs [aria-selected="true"] {
        color: #3c699a !important;
        background-color: transparent !important;
    }

    /* Active tab underline */
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #3c699a;
        height: 3px;
    }

    /* Remove default tab border */
    .stTabs [data-baseweb="tab-border"] {
        background-color: #3c699a;
        height: 1px;
    }
    </style>
""", unsafe_allow_html=True)

# Sample data
df = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D', 'E'],
    'Value': np.random.randint(10, 100, 5)
})

# Create tabs
tab1, tab2 = st.tabs(["Chart", "Dataframe"])

with tab1:
    st.bar_chart(df.set_index('Category'))

with tab2:
    st.dataframe(df, use_container_width=True)