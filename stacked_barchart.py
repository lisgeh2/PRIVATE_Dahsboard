import pandas as pd
import plotly.express as px
import HandleMeta
from colors import C_LIST, GFS_BLUE, CREME_FARBE, FARBEN_4_ABSTUFUNGEN, FARBEN_4, BINAER_VERLAUF, BINAER_VERLAUF_OPPOSITE
import plotly.graph_objects as go
from crunch_label import give_crunch_label
from typing import Literal, Optional, Union
from helpers import clean_value_labels


def create_stacked_bar(
    df: pd.DataFrame,
    meta,
    col: str,
    farben_umkehren: bool = False,
    height: Optional[Union[int, float]] = 150,
    crunch_label_by: Optional[int] = None,
    ):
    
    value_labels = HandleMeta.get_value_labels(meta, col) or {}
    question = HandleMeta.get_column_label(meta, col)

    farb_verlauf = BINAER_VERLAUF
    if farben_umkehren == True:
        farb_verlauf = BINAER_VERLAUF_OPPOSITE

    # Echte Skalen-Codes (SPSS-Sentinels raus)
    value_labels = clean_value_labels(value_labels)
    labels = give_crunch_label(value_labels, crunch_label_by=crunch_label_by)

    counts = [int((df[col] == k).sum()) for k in value_labels.keys()]

    # Prozentsätze berechnen
    total = sum(counts)
    percentages = [count / total * 100 for count in counts]

    # Stacked bar chart mit Plotly Graph Objects
    fig = go.Figure()
    
    labels_list = list(value_labels.values())
    for i, (label, count, percentage) in enumerate(zip(labels_list, counts, percentages)):
        fig.add_trace(go.Bar(
            x=[percentage],
            y=[question],
            name=label,
            orientation='h',
            marker=dict(color=farb_verlauf[len(labels_list)][i]),
            text=f"{percentage:.0f}%",
            textposition="inside",
            textfont=dict(color="white", size=12),
            hovertemplate=f"<b>{label}</b><br>({count} Antworten)<br>{percentage:.1f}%<extra></extra>",
        ))

    fig.update_layout(
        barmode='stack',
        height=height,
        showlegend=True,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=150, t=20, b=0),
        xaxis=dict(
            range=[0, 100],
            showticklabels=False,
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
        ),
    )

    return fig