import pandas as pd
import plotly.express as px
import HandleMeta
from colors import C_LIST, GFS_BLUE, CREME_FARBE, FARBEN_4_ABSTUFUNGEN, FARBEN_4, BINAER_VERLAUF, BINAER_VERLAUF_OPPOSITE
import plotly.graph_objects as go
from crunch_label import give_crunch_label
from typing import Literal, Optional, Union
from helpers import clean_value_labels


