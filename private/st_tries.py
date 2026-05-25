import streamlit as st
import pandas as pd

# Seitenkonfiguration
st.set_page_config(page_title="Personen Filter", layout="wide")

st.title("👥 Personen Filter mit Slider")
st.write("Nutze den Slider, um Personen nach Alter zu filtern")

# Beispieldaten
data = {
    "Name": ["Alice", "Bob", "Charlie", "Diana", "Eva", "Frank", "Grace", "Henry", "Iris", "Jack"],
    "Alter": [25, 32, 28, 45, 19, 56, 38, 42, 29, 51],
    "Stadt": ["Zürich", "Bern", "Genf", "Winterthur", "Bern", "Zürich", "Luzern", "Basel", "Genf", "Winterthur"],
    "Beruf": ["Entwickler", "Designer", "Manager", "Arzt", "Student", "Lehrer", "Ingenieur", "Anwalt", "Analyst", "Entrepreneur"]
}

df = pd.DataFrame(data)

# Sidebar für Filter
st.sidebar.header("🎛️ Filter")

# Slider für Altersbereich
min_age, max_age = st.sidebar.slider(
    "Altersbereich wählen",
    min_value=int(df["Alter"].min()),
    max_value=int(df["Alter"].max()),
    value=(int(df["Alter"].min()), int(df["Alter"].max())),
    step=1,
    help="Nur Personen in diesem Altersbereich werden angezeigt"
)

# Optional: Filter nach Stadt
selected_cities = st.sidebar.multiselect(
    "Städte filtern (optional)",
    options=df["Stadt"].unique(),
    default=df["Stadt"].unique(),
    help="Leer lassen für alle Städte"
)

# Filter anwenden
filtered_df = df[
    (df["Alter"] >= min_age) & 
    (df["Alter"] <= max_age) &
    (df["Stadt"].isin(selected_cities))
].reset_index(drop=True)

# Statistiken in Spalten anzeigen
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Alle Personen", len(df))
with col2:
    st.metric("Gefilterte Personen", len(filtered_df))
with col3:
    st.metric("Durchschnittsalter", f"{filtered_df['Alter'].mean():.1f}" if len(filtered_df) > 0 else "—")
with col4:
    excluded = len(df) - len(filtered_df)
    st.metric("Ausgeschlossene", excluded)

# Trennlinie
st.divider()

# Gefilterte Tabelle anzeigen
if len(filtered_df) > 0:
    st.subheader("📋 Ergebnisse")
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Name": st.column_config.TextColumn("Name", width="small"),
            "Alter": st.column_config.NumberColumn("Alter", width="small"),
            "Stadt": st.column_config.TextColumn("Stadt", width="small"),
            "Beruf": st.column_config.TextColumn("Beruf")
        }
    )
    
    # Download-Button für gefilterte Daten
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Gefilterte Daten als CSV herunterladen",
        data=csv,
        file_name="personen_gefiltert.csv",
        mime="text/csv"
    )
else:
    st.warning("⚠️ Keine Personen mit den gewählten Filtern gefunden.")

# Ausgeschlossene Personen anzeigen
st.divider()
st.subheader("🚫 Ausgeschlossene Personen")
excluded_df = df[
    ~((df["Alter"] >= min_age) & 
      (df["Alter"] <= max_age) &
      (df["Stadt"].isin(selected_cities)))
].reset_index(drop=True)

if len(excluded_df) > 0:
    st.dataframe(
        excluded_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Name": st.column_config.TextColumn("Name", width="small"),
            "Alter": st.column_config.NumberColumn("Alter", width="small"),
            "Stadt": st.column_config.TextColumn("Stadt", width="small"),
            "Beruf": st.column_config.TextColumn("Beruf")
        }
    )
else:
    st.success("✅ Niemand ausgeschlossen - alle Personen sind sichtbar!")