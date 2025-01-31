import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.preprocessing import MinMaxScaler


def create_casual_customer_count():
    casual_customer_df = day_df.groupby("casual").cnt.sum().sort_values(ascending=False).reset_index()
    return casual_customer_df

def create_registered_customer_count():
    registered_customer_df = day_df.groupby("registered").cnt.sum().sort_values(ascending=False).reset_index()
    return registered_customer_df

day_df = pd.read_csv("day_df.csv")
day_df["dteday"] = pd.to_datetime(day_df["dteday"])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://storage.googleapis.com/kaggle-datasets-images/130897/312329/20c79bcd928e6d481fca7d5dc9fa3ca4/dataset-cover.jpg?t=2019-05-24-07-06-55")
    
    # Mengambil start_date & end_date dari date_input
    selected_date = st.date_input(
        label='Pilih Tanggal', 
        min_value=min_date,
        max_value=max_date,
        value=[min_date]
    )

    if isinstance(selected_date, tuple):
        selected_date = selected_date[0]  # Menghindari tuple
    selected_date = pd.Timestamp(selected_date)

# Memfilter data berdasarkan tanggal yang dipilih
main_df = day_df[day_df["dteday"] == pd.Timestamp(selected_date)]

# Menampilkan data yang sesuai
st.write(f"Data untuk tanggal: {selected_date}")
# st.dataframe(main_df)

casual_customer_count = create_casual_customer_count(main_df)
registered_customer_count = create_registered_customer_count(main_df)

st.header('Bike Sharing Dashboard')
