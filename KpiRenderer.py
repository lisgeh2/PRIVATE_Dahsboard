import streamlit as st
from colors import C_LIST


class KpiRenderer:
    def __init__(self, df, section_title="Kernkennzahlen"):
        self.df = df
        self.call_count = 0
        self.section_title = section_title

    def render_section_title(self):
        st.markdown(
            f'<div class="section-title">{self.section_title}</div>',
            unsafe_allow_html=True,
        )

    def render(self, area, label, value, fazit_text, trend=None):
        arrow = ""
        if trend is None:
            trend = "neutral"
        elif trend == "up":
            arrow = "↑ "
        elif trend == "down":
            arrow = "↓ "
        fazit_text = f"{arrow}{fazit_text}"

        color = C_LIST[self.call_count % len(C_LIST)]
        self.call_count += 1

        area.markdown(
            f"""
<div class="kpi-box" style="border-top:3px solid {color};">
    <div class="kpi-label">{label}</div>
    <div class="kpi-value">{value}</div>
    <div class="kpi-{trend}">{fazit_text}</div>
</div>
""",
            unsafe_allow_html=True,
        )

    def anzahl_befragte(self, area, df, label=None, value=None, fazit_text=None, trend=None):
        for v in [label, fazit_text, trend]:
            if v == None:
                v = ""
        self.render(self, area, "BEFRAGTE", str(len(df)), label, fazit_text, trend)

    def anzahl_befragte_mit_jahr(self, area):
        num_current_year = (self.df["Jahr"] == 1).sum()
        num_last_year = (self.df["Jahr"] == 2).sum()

        if num_current_year > num_last_year:
            trend = "up"
        else:
            trend = "down"

        difference_percent = ((num_current_year / num_last_year) * 100) - 100
        fazit_text = f"Im Vergleich zum Vorjahr: {difference_percent:.1f}%"

        self.render(area, "BEFRAGTE", num_current_year, fazit_text, trend)

    def bearbeitungszeit(self, area, fazit_text, trend):
        total_sek = self.df["DURINT"].median()
        minuten, sekunden = divmod(int(total_sek), 60)

        time_string = f"{minuten} min {sekunden} s"

        self.render(area, "Ø Bearbeitungszeit", time_string, fazit_text, trend)
