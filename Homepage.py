import pandas as pd
import sqlite3
import plotly_express as px
import streamlit as st
from PIL import Image

image=Image.open('chinookschema.png')

st.set_page_config(
    page_title="Main Page"
)

st.title("Chinook Dashboard")
st.sidebar.success("Select a page above .")
st.write("Welcome to Chinook DB music Sales dashboard. This dashboard will show information of music sales data from 2009-2013. This dashboard is made for my SQL queries refresher exercise and display the data in streamlit with plotly chart.")

st.image(image, caption='ChinookDB Schema')

st.write("Chinook is a sample database available for SQLite.It can be created by running a single SQL script. "
        "Chinook database is an alternative to the Northwind database, being ideal for demos and testing ORM tools targeting single and multiple database servers. "
        "This database consists of Customer, Tracks, Invoice, Genre, Artist, Album, Playlist etc."
        )

st.write("The First part of this dashboard shows sales movement each year and top 5 sales by artist, country and genres from 2009 to 2013.")
st.write("The next part is sales dashboard by country which shows music sales info of each country using bar chart and line chart. This dashbaard also shows invoice details of each country.")
st.write("The third part is sales dashboard by artist which shows the sales movement and sales details of each artist.")
st.write("The last part is invoice details with year and country filters.")
