import pandas as pd
import plotly.express as px
import HandleMeta
from colors import C_LIST, C, BINAER_VERLAUF, BINAER_VERLAUF_OPPOSITE
from crunch_label import give_crunch_label
from typing import Literal, Optional, Union
from helpers import clean_plot_array, clean_value_labels

def create_barchart(
    df: pd.DataFrame,
    meta,
    col: Union[str, list[str]],
    current_break: Optional[str] = None,
    color: str = "blau",
    color_gradient: Optional[Literal["categories", "continuous"]] = None,
    horizontal: bool = False,
    farben_umkehren: bool = False,
    height: Optional[Union[int, float]] = 450,
    crunch_label_by: Optional[int] = None,
    ):
    _validate_inputs(df, col, current_break, color)


    global FARB_VERLAUF
    FARB_VERLAUF = BINAER_VERLAUF_OPPOSITE if farben_umkehren else BINAER_VERLAUF

    if isinstance(col, list):
        fig = return_multi_question_means_fig(df, meta, col, color, color_gradient, horizontal, crunch_label_by=crunch_label_by)
    else:
        value_labels = HandleMeta.get_value_labels(meta, col) or {}
        value_labels = clean_value_labels(value_labels)

        question = HandleMeta.get_column_label(meta, col)

        break_labels = HandleMeta.get_value_labels(meta, current_break) or {}
        break_labels = clean_value_labels(break_labels)
        break_labels = give_crunch_label(break_labels, crunch_label_by=crunch_label_by)

        if crunch_label_by:
            value_labels = give_crunch_label(value_labels, crunch_label_by=crunch_label_by)

        if current_break == "tz" or current_break is None:
            fig = return_aggregate_percent_fig(df, col, value_labels, color_gradient, horizontal, color)
        else:
            fig = return_break_values_fig(df, col, current_break, value_labels, break_labels, question, color, color_gradient, horizontal)

    fig.update_layout(
        height=height,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=20),
    )
    return fig


def return_aggregate_percent_fig(df, col, value_labels, color_gradient, horizontal, color):
    plot_df = clean_plot_array(df, [col], drop_na=True, clean_item_value_labels=value_labels)
    aggregated_series = plot_df[col].value_counts()
    aggregated_series = aggregated_series.reindex(value_labels.keys(), fill_value=0)
    total = aggregated_series.sum()
    pct = (aggregated_series / total * 100).round(1) if total > 0 else aggregated_series.astype(float)

    labels = [str(value_labels[k]) for k in aggregated_series.index]
    values = pct.values
    texts = [f"{p:.1f}%" for p in values]

    return _finalize_aggregate_fig(
        labels, values, texts, color, color_gradient, horizontal,
        axis_title="Anteil", axis_suffix=" %",
        col=col, value_labels=value_labels,
    )


def _finalize_aggregate_fig(labels, values, texts, color, color_gradient, horizontal,
                            axis_title, axis_suffix="", col=None, value_labels=None):
    fig = give_bar_fig(
        color, color_gradient, horizontal, aggregated=True,
        labels=labels, values=values, texts=texts,
        col=col, value_labels=value_labels,
    )
    fig.update_layout(coloraxis_showscale=False)
    if horizontal:
        fig.update_yaxes(type="category", categoryorder="array", categoryarray=labels)
        fig.update_xaxes(title=axis_title, ticksuffix=axis_suffix)
    else:
        fig.update_xaxes(type="category", categoryorder="array", categoryarray=labels)
        fig.update_yaxes(title=axis_title, ticksuffix=axis_suffix)
    return fig

def return_break_values_fig(df, col, current_break, value_labels, break_labels,
                            question, color, color_gradient, horizontal):
    # First pass: filter on `col` → put `col` first
    plot_df = clean_plot_array(df, [col, current_break], clean_item_value_labels=value_labels)
    if break_labels:
        plot_df = clean_plot_array(plot_df, [current_break, col], clean_item_value_labels=break_labels)

    mean_df = (
        plot_df.groupby(current_break, as_index=False)[col].mean()
        .sort_values(by=col, ascending=False)
    )
    if break_labels:
        mean_df[current_break] = mean_df[current_break].map(break_labels).fillna(mean_df[current_break])

    aggregated = False
    fig = give_bar_fig(
        color, color_gradient, horizontal, aggregated,
        mean_df=mean_df, current_break=current_break, col=col, question=question, value_labels=value_labels,
    )
    return fig


def handle_horizontal(x, y, horizontal):
    if not horizontal:
        orientation = "v"
        return x, y, orientation
    else:
        temp = x
        x = y
        y = temp
        orientation = "h"
        return x, y, orientation


def handle_color(color, color_gradient, values, num_categories):
    # Default Fallback
    color_continuous_scale = None
    color_discrete_sequence = [C[color]]
    color_arg = None
    marker = None
    showlegend = False

    if color_gradient == "continuous":
        color_continuous_scale = "Blues"
        color_discrete_sequence = None
        color_arg = values
        marker = None
        showlegend = False
    elif color_gradient == "categories":
        color_continuous_scale = None
        color_discrete_sequence = None
        color_arg = None
        showlegend = True  # ✅ KEIN KOMMA
        marker = dict(color=FARB_VERLAUF[num_categories])

    return color_discrete_sequence, color_continuous_scale, color_arg, marker, showlegend  # ✅ Kein Komma nach showlegend


def give_bar_fig(color, color_gradient, horizontal, aggregated,
                 mean_df=None, labels=None, values=None, texts=None,
                 current_break=None, col=None, question=None, value_labels=None,):

    if aggregated:
        data = None
        x = labels
        y = values
        text = texts
        px_labels = None
        color_values = values
        num_categories = len(labels)
    else:
        data = mean_df
        x = current_break
        y = col
        text = mean_df[col].round(2)
        px_labels = {col: question, current_break: ""}
        color_values = mean_df[col].values
        num_categories = len(mean_df)

    color_discrete_sequence, color_continuous_scale, color_arg, marker, showlegend = handle_color(color, color_gradient, color_values, num_categories)
    x, y, orientation = handle_horizontal(x, y, horizontal)

    fig = px.bar(
        data,
        x=x,
        y=y,
        text=text,
        labels=px_labels,
        color_discrete_sequence=color_discrete_sequence,
        color=color_arg,
        color_continuous_scale=color_continuous_scale,
        orientation=orientation,
    )
    if marker is not None:
        fig.update_traces(marker=marker)
    fig.update_layout(showlegend=showlegend)

    return fig


def return_multi_question_means_fig(df, meta, cols, color, color_gradient, horizontal, crunch_label_by = None,
                                    decimals=2):
    group_label, single_labels = HandleMeta.get_group_label_and_single_labels(meta, cols)

    rows = []
    for col in cols:
        clean = clean_plot_array(df, [col], drop_na=True)
        mean = clean[col].mean()
        if pd.notna(mean):
            col_label = single_labels[col].strip(" :–-")
            col_label = give_crunch_label(col_label, crunch_label_by=crunch_label_by)
            rows.append((col_label, mean))

    rows.sort(key=lambda r: r[1], reverse=not horizontal)

    labels = [r[0] for r in rows]
    values = [round(r[1], decimals) for r in rows]
    texts  = [f"{v:.{decimals}f}" for v in values]

    fig = _finalize_aggregate_fig(
        labels, values, texts, color, color_gradient, horizontal,
        axis_title="Mittelwert",
    )
    return fig


def _validate_inputs(df, col, current_break, color):
    if col != "tz" and type(col)==str:
        assert col in df.columns, f"col '{col}' is not a column in df"
    elif type(col)==list:
        for c in col:
            assert c in df.columns, f"col '{c}' is not a column in df"
    if current_break != "tz":
        assert current_break is None or current_break in df.columns, \
            f"current_break '{current_break}' is not a column in df"
    assert color in C, f"color must be one of {C}"