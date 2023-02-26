import pandas as pd
import sqlite3
import plotly_express as px
import streamlit as st

#DB Connection------------------------------------
conn=sqlite3.connect("data_input/chinook.db")
#-------------------------------------------------

#Invoice Master Query & Modification--------------
inv_master=pd.read_sql_query(sql= """SELECT * FROM invoices""",
                             con=conn,
                             parse_dates='InvoiceDate')

inv_master['Year']=inv_master['InvoiceDate'].dt.year
inv_master['Year']=inv_master['Year'].astype('category')
inv_master['BillingCountry']=inv_master['BillingCountry'].astype('category')
inv_master['CustomerId']=inv_master['CustomerId'].astype('category')
#-------------------------------------------------

#Page Config------------------------------------
st.set_page_config(page_title='Music Sales by Country',
                    layout='wide')
#-------------------------------------------------

#Sales by Year------------------------------------

st.title(':world_map: Sales Dashboard')

col1,col2,col3,col4,col5=st.columns(5)

with col1:
    country=st.selectbox(
    'Select a Country:',
    options=inv_master['BillingCountry'].unique()
    )

#-------------------------------------------------


#Sales by Year------------------------------------

grp_yr_c=pd.crosstab(index=inv_master['Year'],
                    columns=inv_master['BillingCountry'],
                    values=inv_master['Total'],
                    aggfunc='sum'
                    )
grp_yr_c_sel=grp_yr_c.xs(key=country, axis=1)
tot_grp_yr_c_sel=int(grp_yr_c_sel.sum())
y_avg=len(inv_master['Year'].unique())

inv_master_c=inv_master[(inv_master['BillingCountry']==country)]

inv_count=len(inv_master_c['InvoiceId'].unique())

cust_count=len(inv_master_c['CustomerId'].unique())

with col2:
    st.subheader(f'Total Sales in {country}')
    st.subheader(f"US ${tot_grp_yr_c_sel:,}")

with col3:
    st.subheader('Sales/Year')
    st.subheader(f"US ${(tot_grp_yr_c_sel/y_avg):,}")

with col4:
    st.subheader('Number of Invoices')
    st.subheader(inv_count)

with col5:
    st.subheader('Number of Customers')
    st.subheader(cust_count)

st.markdown("---")

#Sales by Year & Country & Genre & Artist---------
grp_c_y=pd.crosstab(
    index=inv_master['Year'],
    columns=inv_master['BillingCountry'],
    values=inv_master['Total'],
    aggfunc='sum'
)

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


grp_c_genr=pd.crosstab(
    index=genr_art_sum['Country'],
    columns=genr_art_sum['Genres'],
    values=genr_art_sum['Total'],
    aggfunc='sum'
)

grp_c_art=pd.crosstab(
    index=genr_art_sum['Country'],
    columns=genr_art_sum['Artist'],
    values=genr_art_sum['Total'],
    aggfunc='sum'
)

#-------------------------------------------------

grp_c_y_sel=grp_c_y.xs(key=country,axis=1)
grp_genr_sel=grp_c_genr.xs(key=country,axis=0).sort_values().tail(5)
grp_art_sel=grp_c_art.xs(key=country,axis=0).sort_values().tail(5)

#-------------------------------------------------
country_line=px.line(
    grp_c_y_sel,
    markers=True,
    template='ggplot2'
    )

country_line.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(showgrid=False)),
    autosize=True,
    width=500,
    height=350,
    showlegend=False
)

country_line.update_traces(
    marker=dict(size=20)
    )

country_line.update_yaxes(visible=False)

#-------------------------------------------------
genre_line=px.bar(
    grp_genr_sel,
    orientation='h',
    template='ggplot2'
    )

genre_line.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(showgrid=False)),
    autosize=True,
    width=500,
    height=350,
    showlegend=False
)

genre_line.update_xaxes(visible=False)

#-------------------------------------------------
artist_line=px.bar(
    grp_art_sel,
    orientation='h',
    template='ggplot2'
    )

artist_line.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(showgrid=False)),
    autosize=True,
    width=500,
    height=350,
    showlegend=False
)

artist_line.update_xaxes(visible=False)

#-------------------------------------------------

col1,col2,col3=st.columns(3)

with col1:
    st.subheader('Sales in 'f"{country}")
    st.plotly_chart(country_line)

with col2:
    st.subheader('Top 5 Genre in 'f"{country}")
    st.plotly_chart(genre_line)

with col3:
    st.subheader('Top 5 Artist in 'f"{country}")
    st.plotly_chart(artist_line)

st.markdown("---")


st.subheader('Invoice Detail for 'f"{country}")

inv_master_f=inv_master[inv_master['BillingCountry']==country]

st.table(inv_master_c)