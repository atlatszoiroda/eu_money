import streamlit as st
import pandas as pd
from utils_data import read_data


if 'grouped_df' not in st.session_state:
    st.session_state.grouped_df = None    

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
    st.logo(
        'https://atlatszo.hu/wp-content/themes/atlatszo2021/i/atlatszo-logo.svg',
        link="https://atlatszo.hu/",
        size="large")
    # Rádiógomb a megjelenítési mód kiválasztásához
    with st.container(border=False):
        st.markdown('<p style="font-size: 18px;margin-bottom:-5vh">Az alábbi táblázatban az uniós pályázatok adatbázisát lehet böngészni. A <i>részletes szűrés</i> gombra kattintva nyertes pályázó, fejlesztési program, település és megye szerint lehet szűkíteni a találatok számát. A táblázat jobb felső sarkában lévő letöltés (lefele mutató nyíl) gombra kattinva az aktuális nézet adatai letölthetők.<br>A gombokra kattintva válassz megjelenítési módot:</p>', unsafe_allow_html=True)

        display_option = st.radio(' ', ('Top 2000 projekt', 'Részletes szűrés'), horizontal=True)


    if display_option == 'Top 2000 projekt':
        st.markdown("#### Az első 2000 nyertes projekt")

        filtered_df = df[list(display_columns.keys())]
        filtered_df = filtered_df.rename(columns=display_columns)
        filtered_df['Megítélt támogatás (Ft)'] = filtered_df['Megítélt támogatás (Ft)'].apply(lambda x: f"{x:,}".replace(",", " "))

        filtered_df.reset_index(drop=True, inplace=True)
        st.dataframe(filtered_df.head(2000))
    else:
        col1, col2, col3, col4, col5= st.columns([2, 2, 2, 2, 1], vertical_alignment='bottom')
        
        with col1:
            applicant_filter = st.multiselect("Nyertes pályázó", options=df['palyazo_neve'].unique(), placeholder="Válassz a listából!")
        with col2:
            fejlesztesi_filter = st.multiselect("Fejlesztési program", options=df['fejlesztesi_program_nev'].unique(), placeholder="Válassz a listából!")
        with col3:
            city_filter = st.multiselect("Település neve", options=df['helyseg_nev'].unique(), placeholder="Válassz a listából!")
        with col4:
            county_filter = st.multiselect("Megye neve", options=df['megval_megye_nev'].unique(), placeholder="Válassz a listából!")
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
            filtered_df['Megítélt támogatás (Ft)'] = filtered_df['Megítélt támogatás (Ft)'].apply(lambda x: f"{x:,}".replace(",", " "))
            filtered_df.reset_index(drop=True, inplace=True)

            st.dataframe(filtered_df)

    st.markdown("## A teljes adatbázis letölthető [innen](https://github.com/atlatszoiroda/eu_money/raw/refs/heads/main/all_eu_money.xlsx).")

show_full_data()
