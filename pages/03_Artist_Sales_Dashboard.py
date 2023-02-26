import pandas as pd
import sqlite3
import plotly_express as px
import streamlit as st

#DB Connection------------------------------------
conn=sqlite3.connect("data_input/chinook.db")
#-------------------------------------------------

#Page Config------------------------------------
st.set_page_config(
    page_title="Music Sales by Artist",
    layout="wide"
)

st.title(":male-singer: Artist Sales Dashboard")

#-------------------------------------------------

#Main Data----------------------------------------
genr_art_sum=pd.read_sql_query(sql= """SELECT genres.Name as 'Genres',
                                artists.Name as 'Artist',
                                albums.Title AS 'Album',
                                invoices.InvoiceDate as 'Date',
                                invoice_items.UnitPrice as 'Total',
                                invoices.BillingCountry as 'Country'
                                FROM invoices
                                LEFT JOIN invoice_items ON invoices.InvoiceId=invoice_items.InvoiceId
                                LEFT JOIN tracks ON invoice_items.TrackId=tracks.TrackId
                                LEFT JOIN genres ON tracks.GenreId=genres.GenreId
                                LEFT JOIN albums ON tracks.AlbumId=albums.AlbumId
                                LEFT JOIN artists ON albums.ArtistId=artists.ArtistId
                                """,
                         con=conn,
                         parse_dates='Date'
                        )

genr_art_sum['Year']=genr_art_sum['Date'].dt.year
genr_art_sum['Year']=genr_art_sum['Year'].astype('category')
genr_art_sum['Country']=genr_art_sum['Country'].astype('category')
genr_art_sum['Genres']=genr_art_sum['Genres'].astype('category')
genr_art_sum['Artist']=genr_art_sum['Artist'].astype('category')
genr_art_sum['Album']=genr_art_sum['Album'].astype('category')
#-------------------------------------------------

#First 3 Col Data---------------------------------
col1,col2,col3=st.columns(3)
with col1:
    artist=st.selectbox(
    'Select an Artist:',
    options=genr_art_sum['Artist'].unique()
    )

grp_yr_a=pd.crosstab(index=genr_art_sum['Year'],
                    columns=genr_art_sum['Artist'],
                    values=genr_art_sum['Total'],
                    aggfunc='sum')

grp_yr_a_sel=grp_yr_a.xs(key=artist, axis=1)
tot_grp_yr_a_sel=int(grp_yr_a_sel.sum())

y_avg=len(genr_art_sum['Year'].unique())

with col2:
    st.subheader(f'Total Sales of {artist}')
    st.subheader(f"US ${tot_grp_yr_a_sel:,}")

with col3:
    st.subheader(f'Average Sales per Year of {artist}')
    st.subheader(f"US ${(tot_grp_yr_a_sel/y_avg):,}")

st.markdown("---")

#-------------------------------------------------

#Sales by Year & Country & Genre & Artist---------
grp_a_y=pd.crosstab(
    index=genr_art_sum['Year'],
    columns=genr_art_sum['Artist'],
    values=genr_art_sum['Total'],
    aggfunc='sum'
)

grp_a_c=pd.crosstab(
    index=genr_art_sum['Country'],
    columns=genr_art_sum['Artist'],
    values=genr_art_sum['Total'],
    aggfunc='count'
)

grp_a_a=pd.crosstab(
    index=genr_art_sum['Album'],
    columns=genr_art_sum['Artist'],
    values=genr_art_sum['Total'],
    aggfunc='count'
)


#Summarizing Data---------------------------------
grp_a_y_sel=grp_a_y.xs(key=artist,axis=1)
grp_a_c_sel=grp_a_c.xs(key=artist,axis=1).sort_values().tail(5)
grp_a_a_sel=grp_a_a.xs(key=artist,axis=1).sort_values().tail(5)

#-------------------------------------------------

#Year Line Chart----------------------------------
art_line=px.line(
    grp_a_y_sel,
    markers=True,
    template='ggplot2'
    )

art_line.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(showgrid=False)),
    autosize=True,
    width=500,
    height=350,
    showlegend=False
)

art_line.update_traces(
    marker=dict(size=20)
    )

art_line.update_yaxes(visible=False)
#-------------------------------------------------

#Country Chart----------------------------------
country_bar=px.bar(
    grp_a_c_sel,
    orientation='h',
    template='ggplot2'
    )

country_bar.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(showgrid=False)),
    autosize=True,
    width=500,
    height=350,
    showlegend=False
)

country_bar.update_xaxes(visible=False)
#-------------------------------------------------

#Album Chart----------------------------------
album_bar=px.bar(
    grp_a_a_sel,
    orientation='h',
    template='ggplot2'
    )

album_bar.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(showgrid=False)),
    autosize=True,
    width=500,
    height=350,
    showlegend=False
)

album_bar.update_xaxes(visible=False)
#-------------------------------------------------

#Second 3 Col Data--------------------------------

col1,col2,col3=st.columns(3)

with col1:
    st.subheader(f"{artist}"' Sales')
    st.plotly_chart(art_line)

with col2:
    st.subheader('Top 5 'f"{artist}"' Listener Country')
    st.plotly_chart(country_bar)

with col3:
    st.subheader('Top 5 'f"{artist}" ' Albums')
    st.plotly_chart(album_bar)

st.markdown("---")

#-------------------------------------------------