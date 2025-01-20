import streamlit as st


st.set_page_config( layout="wide", page_title="EU-s projektek - Átlátszó",page_icon="📊",)


# --- INTRO ---
about_page = st.Page(
    "views/intro.py",
    title="Alap elemzés",
    icon=":material/account_circle:",
    default=True,
)

# --- STOCK ---
adat_page = st.Page(
    "views/full_data.py",
    title="Teljes Adat",
    icon=":material/trending_up:",
)

# --- elemzse ---
group_page = st.Page(
    "views/data_watch.py",
    title="Elemzés",
    icon=":material/trending_up:",
)



# maps
my_map = st.Page(
    "views/map.py",
    title="Térképes elemzés",
    icon=":material/trending_up:",
)




# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Info": [about_page],
        "Adat": [adat_page, group_page],
        "Térkép": [my_map],
    }
)


# --- SHARED ON ALL PAGES ---
st.logo(
    'https://atlatszo.hu/wp-content/themes/atlatszo2021/i/atlatszo-logo.svg',
    link="https://atlatszo.hu/",
    size="large")

st.sidebar.markdown("[Támogatom a munkátokat!](https://atlatszo.hu/tamogatom/)")


# --- RUN NAVIGATION ---
pg.run()
