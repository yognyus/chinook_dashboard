import pandas as pd
import sqlite3
import plotly_express as px
import streamlit as st

#DB Connection------------------------------------
conn=sqlite3.connect("data_input/chinook.db")
#-------------------------------------------------

#Streamlit Config---------------------------------
st.set_page_config(
    page_title="Sales Personnel",
    layout='wide'
)

st.title(":person_with_blond_hair: Sales Personnel Performance")

st.write('Below are sales personnel performance each year.')
#-------------------------------------------------

#Main Data----------------------------------------
slp_sum=pd.read_sql_query(sql= """SELECT genres.Name as 'Genres',
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

slp_sum['Year']=slp_sum['Date'].dt.year
slp_sum['Year']=slp_sum['Year'].astype('category')
slp_sum['Country']=slp_sum['Country'].astype('category')
slp_sum['Genres']=slp_sum['Genres'].astype('category')
slp_sum['Artist']=slp_sum['Artist'].astype('category')
slp_sum['SalesPerson']=slp_sum['SalesPerson'].astype('category')
#-------------------------------------------------




