import streamlit as st
import requests
import pandas as pd

@st.cache_data(ttl=300)
def fetch_standings(update=False):
    url = 'https://api.teknikzeka.net/tffpuandurumu/api.php'
    if update:
        url += '?update=1'
    resp = requests.get(url)
    data = resp.json()
    if data.get('status') != 'success':
        st.error(f"Hata: {data.get('message', 'Bilinmeyen hata')}")
        return None
    return data

def prepare_dataframe(data):
    standings = data['standings']
    rows = []
    for team in standings:
        s = team['stats']
        rows.append({
            'Sıra': team['position'],
            'Takım': team['name'],
            'O': s['played'],
            'G': s['won'],
            'B': s['drawn'],
            'M': s['lost'],
            'A': s['goals_for'],
            'Y': s['goals_against'],
            'Av': s['goal_diff'],
            'Puan': s['points']
        })
    df = pd.DataFrame(rows)
    return df.sort_values('Sıra').set_index('Sıra')

def main():
    st.title("Türkiye Süper Lig – Güncel Puan Durumu")
    st.markdown("**Veri kaynağı:** Teknik Zeka Net API (güncel JSON verisi)")

    if st.button("Zorla Güncelle (API'den taze veriyi çek)"):
        data = fetch_standings(update=True)
    else:
        data = fetch_standings()

    if not data:
        return

    st.write(f"**Sezon:** {data['season']['name']}")
    st.write(f"**Son güncelleme:** {data['last_updated']}")

    df = prepare_dataframe(data)
    st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()
