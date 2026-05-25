import pyreadstat
import re
from collections import defaultdict

from HandleMeta import get_value_labels, get_column_label, get_group_label_and_single_label

df, meta = pyreadstat.read_sav("fertig_all_waves_UV.sav")


var_labels = meta.column_names_to_labels   # {var: "full label"}
val_labels = meta.variable_value_labels    # {var: {code: "label"}}

group_col_list = ["PN5_1", "PN5_2", "PN5_3", "PN5_4", "PN5_5"]
group_label, single_labels_dict = get_group_label_and_single_label(meta, group_col_list)
print(group_label)
print(single_labels_dict)
