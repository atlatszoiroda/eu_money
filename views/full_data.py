import streamlit as st
import pandas as pd
import plotly.express as px

if 'grouped_df' not in st.session_state:
    st.session_state.grouped_df = None    

@st.cache_data(ttl=3600*24)
def read_data():
    df = pd.read_parquet('all_eu_money.parquet')
    df = df.loc[df['megitelt_tamogatas'].notna()]
    df['megitelt_tamogatas'] = df['megitelt_tamogatas'].astype(int)
    df = df.sort_values(by='megitelt_tamogatas', ascending=False)
    df['tam_dont_datum'] = pd.to_datetime(df['tam_dont_datum'], format='%Y.%m.%d').dt.date
    df['megitelt_tamogatas_eve'] = pd.to_datetime(df['tam_dont_datum'], format='%Y.%m.%d').dt.year
    df.reset_index(drop=True, inplace=True)
    return df
df = read_data()

@st.fragment
def show_full_data():
    st.markdown("## Az első 2000 nyertes projekt")
    display_columns = {
        'megitelt_tamogatas': 'Megítélt támogatás (Ft)',
        'palyazo_neve': 'Pályázó neve',
        'projekt_cime': 'Projekt címe',
        'tam_dont_datum': 'Támogatási döntés dátuma',
        'fejlesztesi_program_nev': 'Fejlesztési program neve',
        'forras': 'Forrás',
        'op_kod': 'Operatív program kódja',
        'konstrukcio_nev': 'Konstrukció neve',
        'konstrukcio_kod': 'Konstrukció kódja',
        'megval_regio_nev': 'Megvalósítási régió neve',
        'megval_megye_nev': 'Megvalósítási megye neve',
        'kisterseg_nev': 'Kistérség neve',
        'helyseg_nev': 'Helység neve',
        'jaras_nev': 'Járás neve'
    }
    filtered_df = df[list(display_columns.keys())]
    filtered_df = filtered_df.rename(columns=display_columns)
    st.dataframe(filtered_df.head(2000))
    
    st.markdown("## A teljes adathalmaz letölthető [itt.](https://github.com/misrori/eu_love/raw/refs/heads/main/all_eu_money.xlsx)")

show_full_data()