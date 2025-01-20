
import streamlit as st
import pandas as pd
import plotly.express as px


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

def get_infoplots(df):

    # Assuming df is your DataFrame
    df['tam_dont_datum'] = pd.to_datetime(df['tam_dont_datum'])
    # Extract year and month
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
    grouped_df['megitelt_tamogatas'] = grouped_df['megitelt_tamogatas'] / 1000000000
    grouped_df['year_month'] = grouped_df['year_month'].astype(str)

    fig = px.bar(
        grouped_df,
        x='year_month',
        y='megitelt_tamogatas',
        color='fejlesztesi_program_nev',
        title='Megitélt támogatás havonta fejlesztési programonként',
        labels={'year_month': 'Év-hónap', 'megitelt_tamogatas': 'Megitélt támogatás', 'fejlesztesi_program_nev': 'Fejlesztési program'},
        barmode='group'
    )

    fig.update_layout(
        barmode='stack',
        plot_bgcolor='white',
        xaxis_title='Év',
        yaxis_title='Megitélt támogatás összege (milliárd Ft)',
        legend_title='',
        height=800,
        legend=dict(
            orientation="h",  # Horizontal orientation
            yanchor="bottom",
            y=1.02,  # Position just above the plot
            xanchor="center",
            x=0.5,  # Centered
            title_font=dict(size=12),  # Adjust title font size
            font=dict(size=10)  # Adjust legend font size
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
    # show it in millárd
    grouped_df['megitelt_tamogatas'] = grouped_df['megitelt_tamogatas'] / 1000000000

    # Adatok ábrázolása Plotlyval
    fig = px.bar(grouped_df, y='fejlesztesi_program_nev', x='megitelt_tamogatas',
                labels={'fejlesztesi_program_nev': 'Fejlesztesi program nev', 'megitelt_tamogatas': 'Megítélt támogatás (milliárd Ft)'},
                title='Megítélt támogatás (milliárd Ft) fejlesztesi programonként', orientation='h' )
    # update the background to white
    fig.update_layout(
        barmode='stack',
        plot_bgcolor='white',
        yaxis_title='Fejlesztési program',
        xaxis_title='Megitélt támogatás (milliárd  Ft)',
        height=600,
        xaxis=dict(
            tickformat=',',  # Ensure numbers are displayed fully with commas
        )
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
    # show it in millárd
    grouped_df['megitelt_tamogatas'] = grouped_df['megitelt_tamogatas'] / 1000000000

    # Adatok ábrázolása Plotlyval
    fig = px.bar(grouped_df, y='megval_regio_nev', x='megitelt_tamogatas',
                labels={'megval_regio_nev': 'Régió', 'megitelt_tamogatas': 'Megítélt támogatás (milliárd Ft)'},
                title='Megítélt támogatás (milliárd Ft) régiónként', orientation='h')
    # update the background to white
    fig.update_layout(
        barmode='stack',
        plot_bgcolor='white',
        yaxis_title='Régió',
        xaxis_title='Megitélt támogatás (milliárd  Ft)',
        xaxis=dict(
            tickformat=',',  # Ensure numbers are displayed fully with commas
        )

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
    # show it in millárd
    grouped_df['megitelt_tamogatas'] = grouped_df['megitelt_tamogatas'] / 1000000000

    # Adatok ábrázolása Plotlyval
    fig = px.bar(grouped_df, y='megval_megye_nev', x='megitelt_tamogatas',
                labels={'megval_megye_nev': 'Megye', 'megitelt_tamogatas': 'Megítélt támogatás (milliárd Ft)'},
                title='Megítélt támogatás (milliárd Ft) megyénként', orientation='h')
    # update the background to white
    fig.update_layout(
        barmode='stack',
        plot_bgcolor='white',
        yaxis_title='Megye',
        xaxis_title='Megitélt támogatás (milliárd  Ft)',
        xaxis=dict(
            tickformat=',',  # Ensure numbers are displayed fully with commas
        )
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
    # show it in millárd
    grouped_df['megitelt_tamogatas'] = grouped_df['megitelt_tamogatas'] / 1000000000

    # Adatok ábrázolása Plotlyval
    fig = px.bar(grouped_df, x='palyazo_neve', y='megitelt_tamogatas',
                labels={'palyazo_neve': 'Pályázó neve', 'megitelt_tamogatas': 'Megítélt támogatás (milliárd Ft)'},
                title='Top 50 pályázó ')
    # update the background to white
    fig.update_layout(
        barmode='stack',
        plot_bgcolor='white',
        xaxis_title='Pályázó',
        yaxis_title='Megitélt támogatás (milliárd  Ft)',
        xaxis=dict(
            tickangle=-45,
            tickformat=','
        ),
        height=1300
    )
    plot5 = fig
############################################################################xx

    return plot1, plot2, plot3, plot4, plot5



@st.fragment
def show_basic_info():

    megiteles_eve_plot, fejlesztesi_program_nev_plot, megval_regio_nev_plot, megval_megye_nev_plot, palyazo_neve_plot = get_infoplots(df)

    # Összegző gondolat
    total_projects = df['id_palyazat'].nunique()
    total_funding = df['megitelt_tamogatas'].sum() / 1e9
    formatted_funding = f"{total_funding:,.2f}".replace(",", " ").replace(".", ",")
    formatted_projects = f"{total_projects:,.0f}".replace(",", " ")

    st.markdown(f"# Összesen {formatted_funding} milliárd Ft EU-s támogatás érkezett Magyarországra.")
    st.markdown(f"# {formatted_projects} projekt kapott támogatást.")
    
    #st.markdown(f"# Összesen {total_funding:,.2f} milliárd Ft EU-s támogatás érkezett Magyarországra.  {total_projects:,.0f} projekt kapott támogatást.")
    #st.markdown(f"# Összesen {total_funding:,.2f} milliárd Ft EU-s támogatás érkezett Magyarországra.\n {total_projects:,.0f} projekt kapott támogatást.".replace(",", " ").replace(".", ","))

    # Plot elrendezés
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
