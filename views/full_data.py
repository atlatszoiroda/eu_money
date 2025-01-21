import streamlit as st
import pandas as pd

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


@st.fragment
def show_full_data():
    # Rádiógomb a megjelenítési mód kiválasztásához
    with st.container(border=True):
        st.markdown("#### Válassz megjelenítési módot:")
        display_option = st.radio(
            "",
            ('Top 2000 projekt', 'Szűrés'), horizontal=True
        )

    if display_option == 'Top 2000 projekt':
        st.markdown("## Az első 2000 nyertes projekt")

        filtered_df = df[list(display_columns.keys())]
        filtered_df = filtered_df.rename(columns=display_columns)
        filtered_df.reset_index(drop=True, inplace=True)
        st.dataframe(filtered_df.head(2000))
    else:
        col1, col2, col3, col4, col5 = st.columns(5, vertical_alignment='center')
        
        with col1:
            applicant_filter = st.multiselect("Nyertes pályázó", options=df['palyazo_neve'].unique())
        with col2:
            fejlesztesi_filter = st.multiselect("Fejlesztési program", options=df['fejlesztesi_program_nev'].unique())
        with col3:
            city_filter = st.multiselect("Település neve", options=df['helyseg_nev'].unique())
        with col4:
            county_filter = st.multiselect("Megye neve", options=df['megval_megye_nev'].unique())
        with col5:
            filter_button = st.button("Szűrés")
        
        if filter_button:
            
            if not applicant_filter and not city_filter and not county_filter and not fejlesztesi_filter:
                st.warning("Legalább egy szűrőfeltételt meg kell adni!")
                return
            
            
            filtered_df = df.copy()
            
            if applicant_filter:
                filtered_df = filtered_df[filtered_df['palyazo_neve'].isin(applicant_filter)]
            if fejlesztesi_filter:
                filtered_df = filtered_df[filtered_df['fejlesztesi_program_nev'].isin(fejlesztesi_filter)]
            if city_filter:
                filtered_df = filtered_df[filtered_df['helyseg_nev'].isin(city_filter)]
            if county_filter:
                filtered_df = filtered_df[filtered_df['megval_megye_nev'].isin(county_filter)]
            
            filtered_df = filtered_df[list(display_columns.keys())]
            filtered_df = filtered_df.rename(columns=display_columns)
            filtered_df.reset_index(drop=True, inplace=True)

            st.dataframe(filtered_df)

    st.markdown("## A teljes adathalmaz letölthető [itt.](https://github.com/misrori/eu_love/raw/refs/heads/main/all_eu_money.xlsx)")

show_full_data()
