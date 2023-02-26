import pandas as pd
import sqlite3
import plotly_express as px
import streamlit as st

#DB Connection------------------------------------
conn=sqlite3.connect("data_input/chinook.db")
#-------------------------------------------------

#Page Config------------------------------------
st.set_page_config(page_title='Music Sales by Country',
                    layout='wide')
#-------------------------------------------------

st.title(":eyeglasses: Invoice Detail")

st.write("Below are invoice details in long format which can be filtered by year, country and artist.")

#Invoice Master Query & Modification--------------
inv_master=pd.read_sql_query(sql= """SELECT * FROM invoices""",
                             con=conn,
                             parse_dates='InvoiceDate')

inv_master['Year']=inv_master['InvoiceDate'].dt.year
inv_master['Year']=inv_master['Year'].astype('category')
inv_master['BillingCountry']=inv_master['BillingCountry'].astype('category')
inv_master['CustomerId']=inv_master['CustomerId'].astype('category')

all_country=inv_master['BillingCountry'].unique().tolist()

#-------------------------------------------------

#Invoice Detail Query & Modification--------------
inv_detail=pd.read_sql_query(sql= """SELECT 
                                invoices.InvoiceId as 'Invoice-ID',
                                invoices.CustomerId as 'Customer-ID',
                                tracks.Name as 'Tracks',
                                artists.Name as 'Artist',
                                albums.Title AS 'Album',
                                genres.Name as 'Genres',
                                invoice_items.UnitPrice as 'Total',
                                invoices.InvoiceDate as 'Date',
                                invoices.BillingAddress as 'Address',
                                invoices.BillingCountry as 'Country',
                                invoices.BillingCity as 'City'
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

inv_detail['Year']=inv_detail['Date'].dt.year
inv_detail['Year']=inv_detail['Year'].astype('category')
inv_detail['Country']=inv_detail['Country'].astype('category')
inv_detail['Genres']=inv_detail['Genres'].astype('category')
inv_detail['Artist']=inv_detail['Artist'].astype('category')
inv_detail['Album']=inv_detail['Album'].astype('category')

all_artist=inv_detail['Artist'].unique().tolist()

#-------------------------------------------------

col1,col2,col3=st.columns(3)

with col1:
       
       opt_year=st.multiselect('You can select the years you want to include or exclude.',
                        inv_detail['Year'].unique(),
                        default=[2009,2010,2011,2012,2013]
                            )

with col2:
       opt_country=st.multiselect('Choose the countries you want to see.',
                        inv_detail['Country'].unique(),
                        default=['USA','Canada' ]
                            )
       
       all_c=st.checkbox('Select All Country')
       
       if all_c:
              opt_country=all_country


# with col3:
#        opt_artist=st.multiselect('Pick artists you want to view.',
#                         inv_detail['Artist'].unique(),
#                         default=['Iron Maiden','U2','Metallica','Led Zeppelin','Lost']
#                             )
       
#        all_art=st.checkbox('Select All Artist')
       
#        if all_art:
#               opt_artist=all_artist

inv_master_f=inv_master[inv_master['Year'].isin(opt_year) & 
              inv_master['BillingCountry'].isin(opt_country)
              ]

st.dataframe(inv_master_f)

st.markdown("### Invoice Details based on filter selection above.")

col1,col2=st.columns([1,5])

with col1:
       inv_id=st.selectbox(
       'Select Invoice-ID:',
       options=inv_master_f['InvoiceId'].unique()
       )
       
       inv_detail_f=inv_detail[inv_detail['Invoice-ID']==inv_id]

       inv_det_art=pd.crosstab(
              index=inv_detail_f['Artist'],
              columns='Total',
              values=inv_detail_f['Total'],
              aggfunc='sum'
       )

       inv_det_art=inv_det_art[inv_det_art['Total']!=0]

       total=sum(inv_det_art['Total'])

       st.table(inv_det_art)

       st.metric('Total',f'US${(total):,.2f}')

with col2:
       st.dataframe(inv_detail_f)