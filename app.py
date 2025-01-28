import streamlit as st


st.set_page_config( layout="wide", page_title="Uniós támogatások - Átlátszó",page_icon="📊",)
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600&display=swap');
        
        body {
            font-family: 'Montserrat', sans-serif!important;
        }

        .markdown-text {
            font-family: 'Montserrat', sans-serif!important;
        }

        .stMarkdown, .stWrite, .stText {
            font-family: 'Montserrat', sans-serif !important;
        }

        h1, h2, h3, h4, h5, h6, p, div {
            font-family: 'Montserrat', sans-serif!important;
}
h1{font-size:2.1vw!important
    
}
        .plotly .main-svg text {
            font-family: 'Montserrat', sans-serif !important;
        }

        .plotly .main-svg .tick text {
            font-family: 'Montserrat', sans-serif !important;
        }

        .plotly .main-svg .xaxis-title text,
        .plotly .main-svg .yaxis-title text {
            font-family: 'Montserrat', sans-serif !important;
        }



    </style>
    """, unsafe_allow_html=True)

# --- INTRO ---
about_page = st.Page(
    "views/intro.py",
    title="Alap elemzés",
    icon=":material/trending_up:",
    default=True,
)

# --- STOCK ---
adat_page = st.Page(
    "views/full_data.py",
    title="Teljes adat",
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
        "Főoldal": [about_page],
        "Részletes adatok": [adat_page, group_page],
        "Térkép": [my_map],
    }
)


# --- SHARED ON ALL PAGES ---
st.logo(
    'https://atlatszo.hu/wp-content/themes/atlatszo2021/i/atlatszo-logo.svg',
    link="https://atlatszo.hu/",
    size="large")



st.sidebar.markdown("""
    <a href="https://atlatszo.hu/tamogatom/" target="_blank">
        <button class="tamgomb" style="background-color: #ff2932; color: white; border: none; padding: 8px 14px; font-size: 14px; cursor: pointer; transition: background-color 0.3s ease;font-family:Montserrat">
            Támogasd a munkánkat!
        </button>
    </a>
    <style>
        .tamgomb:hover {
            background-color: black !important;
        }
    </style>
    """, unsafe_allow_html=True)


# --- RUN NAVIGATION ---
pg.run()
