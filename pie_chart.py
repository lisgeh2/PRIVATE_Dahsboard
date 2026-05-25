import pandas as pd
import plotly.express as px
import HandleMeta
from colors import C_LIST
from crunch_label import give_crunch_label
from typing import Literal, Optional, Union
from helpers import clean_value_labels


def create_piechart(
    df: pd.DataFrame,
    meta,
    col: str,
    hole: float = 0.4,
    height: Optional[Union[int, float]] = 200,
    crunch_label_by: Optional[int] = None,
    ):
    
    value_labels = HandleMeta.get_value_labels(meta, col) or {}
    value_labels = clean_value_labels(value_labels)

    labels_list = list(value_labels.values())
    counts = [int((df[col] == k).sum()) for k in value_labels.keys()]
    labels_list = give_crunch_label(labels_list, crunch_label_by=crunch_label_by)


    fig = px.pie(
        names=labels_list,
        values=counts,
        hole=hole,  # auf 0.5 setzen für Donut
        color_discrete_sequence=C_LIST,   # <-- hier kommen die Farben rein

    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
    )

    fig.update_layout(
        height=height,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=5, r=20, t=0, b=0),
    )
    return fig