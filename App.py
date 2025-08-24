import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Süper Lig Puan Durumu (API)", layout="wide")
st.title("Türkiye Süper Lig – Güncel Puan Durumu (API)")

API_URL = "https://api.teknikzeka.net/tffpuandurumu/api.php"

@st.cache_data(show_spinner=False)
def fetch_standings(force_update=False):
    params = {"update": 1} if force_update else {}
    try:
        resp = requests.get(API_URL, params=params, timeout=10)
        data = resp.json()
        if data.get("status") != "success":
            st.error(f"Hata: {data.get('message', 'Bilinmeyen hata')}")
            return None, None
        return data.get("standings", []), data.get("season", {})
    except Exception as e:
        st.error(f"API isteğinde hata: {e}")
        return None, None

# --- Refresh butonu ---
if st.button("🔄 Yenile"):
    st.cache_data.clear()     # Önbelleği temizle
    st.experimental_rerun()   # Sayfayı baştan yükle

# Varsayılan veri çekme
standings, season = fetch_standings(force_update=True)

if standings is None:
    st.stop()

st.subheader(f"Sezon: {season.get('name', '')} – Güncel Hafta: {season.get('week', '')}")

# Veriyi DataFrame olarak işleme
df = pd.DataFrame([{
    "Sıra": t.get("position"),
    "Takım": t.get("name"),
    "O": t["stats"].get("played"),
    "G": t["stats"].get("won"),
    "B": t["stats"].get("drawn"),
    "M": t["stats"].get("lost"),
    "AG": t["stats"].get("goals_for"),
    "YG": t["stats"].get("goals_against"),
    "AV": t["stats"].get("goal_diff"),
    "Puan": t["stats"].get("points")
} for t in standings])

st.dataframe(df.set_index("Sıra"), use_container_width=True)

st.download_button(
    "CSV olarak indir",
    df.to_csv(index=False).encode("utf-8"),
    file_name="superlig_puan_durumu.csv",
    mime="text/csv"
)
