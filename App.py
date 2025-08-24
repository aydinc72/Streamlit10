import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

@st.cache_data(ttl=600)
def fetch_from_tff():
    url = 'https://www.tff.org/default.aspx?pageID=198'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    table = soup.select_one('table.s-table')
    if not table:
        st.error("Puan durumu tablosu bulunamadı!")
        return None
    headers = [th.get_text(strip=True) for th in table.find_all('th')]
    rows = []
    for tr in table.find_all('tr')[1:]:
        cols = [td.get_text(strip=True) for td in tr.find_all('td')]
        if cols:
            rows.append(cols)
    df = pd.DataFrame(rows, columns=headers)
    return df

def main():
    st.title("Süper Lig – Güncel Puan Durumu (TFF'den)")
    df = fetch_from_tff()
    if df is not None:
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()
