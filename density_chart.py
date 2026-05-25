import pandas as pd
import numpy as np
from scipy import stats
import HandleMeta
from colors import GFS_BLUE, FARBEN_4_ABSTUFUNGEN
import plotly.graph_objects as go
from typing import Optional, Union
from helpers import hex_to_rgba, clean_plot_array, clean_value_labels


def create_density_plot(
    df: pd.DataFrame,
    meta,
    col: str,
    height: Optional[Union[int, float]] = 200,
    color = "blau",
    show_mean: bool = True,
    show_median: bool = False,
    smoothness: float = 0.3,
    ):

    question = HandleMeta.get_column_label(meta, col)

    # Echte Werte (SPSS-Sentinels und NaNs raus)
    
    plot_df = clean_plot_array(df, col)


    fig = go.Figure()

    if len(plot_df) < 2 or plot_df.nunique() < 2:
        # Nicht genug Variation für KDE -> leere Figur mit Hinweis
        fig.update_layout(
            height=height,
            annotations=[dict(
                text="Nicht genügend Daten für Dichteplot",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(color="gray", size=12),
            )],
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        return fig

    # KDE berechnen
    n_points = 200
    kde = stats.gaussian_kde(plot_df, bw_method=smoothness)
    pad = (plot_df.max() - plot_df.min()) * 0.05
    x_range = np.linspace(plot_df.min() - pad, plot_df.max() + pad, n_points)
    y_density = kde(x_range)

    fill_color = hex_to_rgba(FARBEN_4_ABSTUFUNGEN[color]["sehr_hell"])
    line_css = hex_to_rgba(FARBEN_4_ABSTUFUNGEN[color]["dunkel"])

    # Dichtekurve mit Füllung
    fig.add_trace(go.Scatter(
        x=x_range,
        y=y_density,
        mode="lines",
        fill="tozeroy",
        line=dict(color=line_css, width=2),
        fillcolor=fill_color,
        name=question,
        hovertemplate="<b>Wert:</b> %{x:.2f}<br><b>Dichte:</b> %{y:.4f}<extra></extra>",
    ))

    # Optionale Referenzlinien
    if show_mean:
        mean_val = float(plot_df.mean())
        fig.add_vline(
            x=mean_val,
            line_dash="dash",
            line_color="gray",
            annotation_text=f"Ø {mean_val:.1f}",
            annotation_position="top",
            annotation_font=dict(size=11, color="gray"),
        )

    if show_median:
        median_val = float(plot_df.median())
        fig.add_vline(
            x=median_val,
            line_dash="dot",
            line_color="gray",
            annotation_text=f"Md {median_val:.1f}",
            annotation_position="top",
            annotation_font=dict(size=11, color="gray"),
        )

    fig.update_layout(
        height=height,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=30, b=30),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor="lightgray",
            ticks="outside",
            tickfont=dict(size=11),
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
        ),
    )

    return fig