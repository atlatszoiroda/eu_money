
import streamlit as st
import pandas as pd
import plotly.express as px
from utils_data import read_data

df = read_data()

def get_infoplots(df):


    df['tam_dont_datum'] = pd.to_datetime(df['tam_dont_datum'])
 
    df['year_month'] = df['tam_dont_datum'].dt.to_period('M')
    grouped_df = (
        df[df['tam_dont_datum'].dt.year > 2004]         
        .groupby(['year_month', 'fejlesztesi_program_nev'], as_index=False)
        .agg(
            megitelt_tamogatas=('megitelt_tamogatas', 'sum'),
            number_of_projects=('megitelt_tamogatas', 'count')
        )
        .reset_index()
    )
    grouped_df['megitelt_tamogatas'] = (grouped_df['megitelt_tamogatas'] / 1000000000).round(2)
    grouped_df['year_month'] = grouped_df['year_month'].astype(str)

    fig = px.bar(
        grouped_df,
        x='year_month',
        y='megitelt_tamogatas',
        color='fejlesztesi_program_nev',
        title='Megítélt támogatás havonta fejlesztési programonként',
        labels={'year_month': 'Dátum', 'megitelt_tamogatas': 'Megítélt támogatás (milliárd Ft)', 'fejlesztesi_program_nev': 'Fejlesztési program'},
        barmode='group'
    )

    fig.update_layout(
        barmode='stack',
        plot_bgcolor='white',
        xaxis_title=' ',
        yaxis_title='Megítélt támogatás összege (milliárd Ft)',
        legend_title=' ',
        height=800,
        legend=dict(
            orientation="h",
            yanchor="middle",
            y=1.02, 
            xanchor="center",
            x=0.5, 
            title_font=dict(size=12), 
            font=dict(size=10)

        )
    )


    plot1 = fig
############################################################################xx


    grouped_df= (
        df
        .groupby('fejlesztesi_program_nev', as_index=False)
        .agg(
            megitelt_tamogatas=('megitelt_tamogatas', 'sum'),
            number_of_projects=('megitelt_tamogatas', 'count')
        )    
        .sort_values(by='megitelt_tamogatas', ascending=True)
        .reset_index()
    )

    grouped_df['megitelt_tamogatas'] = (grouped_df['megitelt_tamogatas'] / 1000000000).round(2)


    fig = px.bar(grouped_df, y='fejlesztesi_program_nev', x='megitelt_tamogatas',
                labels={'fejlesztesi_program_nev': 'Fejlesztesi program nev', 'megitelt_tamogatas': 'Megítélt támogatás (milliárd Ft)'},
                title='Megítélt támogatás fejlesztesi programonként', orientation='h' )
 
    fig.update_layout(
        barmode='stack',
        plot_bgcolor='white',
        yaxis_title=' ',
        xaxis_title='Megítélt támogatás (milliárd  Ft)',
        height=600,
        xaxis=dict(
            tickformat=',',  
        )
    )
    fig.update_traces(
    marker=dict(color='#c4c4c4'), 
    text=grouped_df['megitelt_tamogatas'], 
    textposition='inside', 
    texttemplate='%{text:.0f}',
    )
    plot2 = fig
############################################################################xx


    grouped_df= (
        df
        .groupby('megval_regio_nev', as_index=False)
        .agg(
            megitelt_tamogatas=('megitelt_tamogatas', 'sum'),
            number_of_projects=('megitelt_tamogatas', 'count')
        )    
        .sort_values(by='megitelt_tamogatas', ascending=True)
        .reset_index()
    )

    grouped_df['megitelt_tamogatas'] = (grouped_df['megitelt_tamogatas'] / 1000000000).round(2)


    fig = px.bar(grouped_df, y='megval_regio_nev', x='megitelt_tamogatas',
                labels={'megval_regio_nev': 'Régió', 'megitelt_tamogatas': 'Megítélt támogatás (milliárd Ft)'},
                title='Megítélt támogatás régiónként', orientation='h')
  
    fig.update_layout(
        barmode='stack',
        plot_bgcolor='white',
        yaxis_title=' ',
        xaxis_title='Megítélt támogatás (milliárd  Ft)',
        height=500,
        xaxis=dict(
            tickformat=',', 
        )

    )
    fig.update_traces(
    marker=dict(color='#c4c4c4'), 
    text=grouped_df['megitelt_tamogatas'], 
    textposition='inside', 
    texttemplate='%{text:.0f}', 
    )
    plot3 = fig
############################################################################xx

    grouped_df= (
        df
        .groupby('megval_megye_nev', as_index=False)
        .agg(
            megitelt_tamogatas=('megitelt_tamogatas', 'sum'),
            number_of_projects=('megitelt_tamogatas', 'count')
        )    
        .sort_values(by='megitelt_tamogatas', ascending=True)
        .reset_index()
    )

    grouped_df['megitelt_tamogatas'] = (grouped_df['megitelt_tamogatas'] / 1000000000).round(2)


    fig = px.bar(grouped_df, y='megval_megye_nev', x='megitelt_tamogatas',
                labels={'megval_megye_nev': 'Megye', 'megitelt_tamogatas': 'Megítélt támogatás (milliárd Ft)'},
                title='Megítélt támogatás megyénként', orientation='h')
 
    fig.update_layout(
        barmode='stack',
        plot_bgcolor='white',
        yaxis_title=' ',
        xaxis_title='Megítélt támogatás (milliárd  Ft)',
        height=500,
        xaxis=dict(
            tickformat=',', 
        )
    )

    fig.update_traces(
    marker=dict(color='#c4c4c4'),
    text=grouped_df['megitelt_tamogatas'],
    textposition='outside', 
    texttemplate='%{text:.0f}',
    textfont=dict(size=10),
    )

    plot4 = fig
############################################################################xx

    grouped_df= (
        df
        .groupby('palyazo_neve', as_index=False)
        .agg(
            megitelt_tamogatas=('megitelt_tamogatas', 'sum'),
            number_of_projects=('megitelt_tamogatas', 'count')
        )    
        .sort_values(by='megitelt_tamogatas', ascending=False)
        .head(50)
        .reset_index()
    )

    grouped_df['megitelt_tamogatas'] = (grouped_df['megitelt_tamogatas'] / 1000000000).round(2)




    fig = px.bar(grouped_df, y='palyazo_neve', x='megitelt_tamogatas',
                labels={'palyazo_neve': 'Pályázó neve', 'megitelt_tamogatas': 'Megítélt támogatás (milliárd Ft)'},
                title='Top 50 pályázó ')

    fig.update_layout(
        barmode='stack',
        plot_bgcolor='white',
        yaxis_title=' ',
        xaxis_title='Megítélt támogatás (milliárd  Ft)',
        xaxis=dict(
            tickangle=0,
            tickformat=','
        ),
        height=1300,
        yaxis=dict(
        autorange='reversed' 
    )
    )

    fig.update_traces(
    marker=dict(color='#c4c4c4'),
    text=grouped_df['megitelt_tamogatas'],
    textposition='inside',
    texttemplate='%{text:.0f}',
    textangle=0,
    )
    plot5 = fig
############################################################################xx

    return plot1, plot2, plot3, plot4, plot5



@st.fragment
def show_basic_info():

    megiteles_eve_plot, fejlesztesi_program_nev_plot, megval_regio_nev_plot, megval_megye_nev_plot, palyazo_neve_plot = get_infoplots(df)


    total_projects = df['id_palyazat'].nunique()
    total_funding = df['megitelt_tamogatas'].sum() / 1e9
    formatted_funding = f"{total_funding:,.2f}".replace(",", " ").replace(".", ",")
    formatted_projects = f"{total_projects:,.0f}".replace(",", " ")

    st.markdown(f"## 2005 óta összesen {formatted_funding} milliárd Ft EU-s támogatás érkezett Magyarországra. Ezt az összeget {formatted_projects} projekt kapta.")
    st.markdown("<p style='font-size: 18px'>A <a href='https://www.palyazat.gov.hu/eredmenyek/tamogatott-projektek?program=Széchenyi+terv+plusz' target='_blank'>palyazat.gov.hu</a> oldalon található adatok alapján naponta frissül az oldal.<br>Az alábbi diagramokon bemutatjuk a megítélt támogatásokat évek, fejlesztési programok, területi egységek és legtöbbet nyert pályázók szerint.<br>A bal oldali menüsávban további oldalakon lehet böngészni a teljes adatbázist.<br>Az alkalmazást a legjobb felhasználói élmény érdekében számítógépes webböngészőben érdemes használni.</p>", unsafe_allow_html=True)

    

    with st.container(border=True):
        st.plotly_chart(megiteles_eve_plot)

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):

            st.plotly_chart(megval_regio_nev_plot)
    with col2:
        with st.container(border=True):
            st.plotly_chart(megval_megye_nev_plot)

    with st.container(border=True):
        st.plotly_chart(fejlesztesi_program_nev_plot)
    with st.container(border=True):
        st.plotly_chart(palyazo_neve_plot)

show_basic_info()
