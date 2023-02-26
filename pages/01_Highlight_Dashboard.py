import pandas as pd
import sqlite3
import plotly_express as px
import streamlit as st

#DB Connection------------------------------------
conn=sqlite3.connect("data_input/chinook.db")
#-------------------------------------------------

#Streamlit Config---------------------------------
st.set_page_config(
    page_title="Highlight Page",
    layout='wide'
)

st.title(":triangular_flag_on_post: Highlight Dashboard")

st.write('Below are sales metric for every year and three charts which highlight Sales by Artist, Country and Genre.')
#-------------------------------------------------

#Main Data----------------------------------------
genr_art_sum=pd.read_sql_query(sql= """SELECT genres.Name as 'Genres',
                                artists.Name as 'Artist',
                                invoices.InvoiceDate as 'Date',
                                invoice_items.UnitPrice as 'Total',
                                invoices.BillingCountry as 'Country',
                                employees.LastName as 'SalesPerson',
                                tracks.Name as 'Song'
                                FROM invoices
                                LEFT JOIN invoice_items ON invoices.InvoiceId=invoice_items.InvoiceId
                                LEFT JOIN tracks ON invoice_items.TrackId=tracks.TrackId
                                LEFT JOIN genres ON tracks.GenreId=genres.GenreId
                                LEFT JOIN albums ON tracks.AlbumId=albums.AlbumId
                                LEFT JOIN artists ON albums.ArtistId=artists.ArtistId
                                LEFT JOIN customers on invoices.CustomerId=customers.CustomerId
                                LEFT JOIN employees on customers.SupportRepId=employees.EmployeeId
                                """,
                         con=conn,
                         parse_dates='Date'
                        )

genr_art_sum['Year']=genr_art_sum['Date'].dt.year
genr_art_sum['Year']=genr_art_sum['Year'].astype('category')
genr_art_sum['Country']=genr_art_sum['Country'].astype('category')
genr_art_sum['Genres']=genr_art_sum['Genres'].astype('category')
genr_art_sum['Artist']=genr_art_sum['Artist'].astype('category')
genr_art_sum['SalesPerson']=genr_art_sum['SalesPerson'].astype('category')

yearly=pd.crosstab(index=genr_art_sum['Year'],
                    columns='Total',
                    values=genr_art_sum['Total'],
                    aggfunc='sum'
                    )

y_2009=yearly.xs(key=2009,axis=0)
y_2010=yearly.xs(key=2010,axis=0)
y_2011=yearly.xs(key=2011,axis=0)
y_2012=yearly.xs(key=2012,axis=0)
y_2013=yearly.xs(key=2013,axis=0)

#-------------------------------------------------


#Metric----------------------------------------

col1,col2,col3,col4,col5,col6,=st.columns(6)

with col1:
    st.metric('2009',f'US${int(y_2009):,}')

with col2:
    st.metric('2010',f'US${int(y_2010):,}',(int(y_2010)-int(y_2009)))

with col3:
    st.metric('2011',f'US${int(y_2011):,}',(int(y_2011)-int(y_2010)))

with col4:
    st.metric('2012',f'US${int(y_2012):,}',(int(y_2012)-int(y_2011)))

with col5:
    st.metric('2013',f'US${int(y_2013):,}',(int(y_2013)-int(y_2012)))

with col6:
    st.metric('Total',f'US${(int(y_2009)+int(y_2010)+int(y_2011)+int(y_2012)+int(y_2013)):,}')


options=st.multiselect('You can select the years you want to include or exclude.',
                            genr_art_sum['Year'].unique(),
                            default=[2009,2010,2011,2012,2013]
)

genr_art_sum=genr_art_sum[genr_art_sum['Year'].isin(options)]

#Data Chart---------------------------------------
grp_5_a=genr_art_sum.groupby('Artist').sum(numeric_only=True).sort_values(by='Total', ascending=True).tail(5)

grp_5_c=genr_art_sum.groupby('Country').sum(numeric_only=True).sort_values(by='Total', ascending=True).tail(5)

grp_5_e=genr_art_sum.groupby('Genres').sum(numeric_only=True).sort_values(by='Total', ascending=True).tail(5)

grp_5_s=genr_art_sum.groupby('SalesPerson').sum(numeric_only=True).sort_values(by='Total', ascending=True).tail(3)

#-------------------------------------------------

#Artist Charts------------------------------------
grp_5_a_bar=px.bar(
    grp_5_a,
    orientation='h',
    template='ggplot2'
    )

grp_5_a_bar.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(showgrid=False)),
    autosize=True,
    width=500,
    height=350,
    showlegend=False,
    
)

grp_5_a_bar.update_xaxes(visible=False)

#-------------------------------------------------

#Country Charts-----------------------------------
grp_5_c_bar=px.bar(
    grp_5_c,
    orientation='h',
    template='ggplot2'
    )

grp_5_c_bar.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(showgrid=False)),
    autosize=True,
    width=500,
    height=350,
    showlegend=False
)

grp_5_c_bar.update_xaxes(visible=False)

#-------------------------------------------------

#Genres Charts------------------------------------
grp_5_e_bar=px.bar(
    grp_5_e,
    orientation='h',
    template='ggplot2'
    )

grp_5_e_bar.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(showgrid=False)),
    autosize=True,
    width=500,
    height=350,
    showlegend=False
)

grp_5_e_bar.update_xaxes(visible=False)

#-------------------------------------------------

#Genres Charts------------------------------------
grp_5_e_bar=px.bar(
    grp_5_e,
    orientation='h',
    template='ggplot2'
    )

grp_5_e_bar.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(showgrid=False)),
    autosize=True,
    width=500,
    height=350,
    showlegend=False
)

grp_5_e_bar.update_xaxes(visible=False)

#-------------------------------------------------

#Genres Charts------------------------------------
grp_5_s_bar=px.bar(
    grp_5_s,
    orientation='h',
    template='ggplot2'
    )

grp_5_s_bar.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(showgrid=False)),
    autosize=True,
    width=500,
    height=350,
    showlegend=False
)

grp_5_s_bar.update_xaxes(visible=False)

#-------------------------------------------------

#Bar Charts---------------------------------------
col1,col2,col3=st.columns(3)

with col1:
    st.subheader('Top 5 Sales by Artist')
    st.plotly_chart(grp_5_a_bar)

with col2:
    st.subheader('Top 5 Sales by Country')
    st.plotly_chart(grp_5_c_bar)

with col3:
    st.subheader('Top 5 Sales by Genres')
    st.plotly_chart(grp_5_e_bar)

#-------------------------------------------------

s_peacock=grp_5_s.xs(key='Peacock',axis=0)
s_park=grp_5_s.xs(key='Park',axis=0)
s_johnson=grp_5_s.xs(key='Johnson',axis=0)

#2nd Bar Charts-----------------------------------
st.markdown("### Sales Person Performance")

col1,col2,col3=st.columns(3)

with col1:
    st.metric('Peacock',f'US${int(s_peacock):,}')

with col2:
    st.metric('Park',f'US${int(s_park):,}')

with col3:
    st.metric('Johnson',f'US${int(s_johnson):,}')

#-------------------------------------------------

st.markdown("---")

