# card_handler.py
from contextlib import contextmanager
import streamlit as st


class CardHandler:
    """Erzeugt automatisch eindeutige Keys und rendert Titel/Subtitle."""

    def __init__(self, prefix: str = "karte"):
        self.prefix = prefix
        self._counter = 0

    @contextmanager
    def card(self, title: str | None = None, subtitle: str | None = None, key: str | None = None):
        self._counter += 1
        container_key = key or f"{self.prefix}_{self._counter}"

        with st.container(key=container_key):
            if title:
                st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
            if subtitle:
                st.subheader(subtitle)
            yield container_key   # ← Wert yielden, damit `as cid` funktioniert