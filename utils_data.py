import pandas as pd
import streamlit as st
import geopandas

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

@st.cache_data(ttl=3600*24)
def read_geojsons():
    regio = geopandas.read_file("map_data/regio.geojson")
    megye = geopandas.read_file("map_data/megye.geojson")
    kisterseg = geopandas.read_file("map_data/kisterseg.geojson")
    varos = geopandas.read_file("map_data/varos.geojson")
    return regio, megye, kisterseg, varos