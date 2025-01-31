import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


def create_casual_customer_count(df):
    casual_customer_df = (df.groupby("casual")["cnt"].sum().reset_index().rename(columns={"cnt": "total_count"}))
    return casual_customer_df

def create_registered_customer_count(df):
    registered_customer_df = (df.groupby("registered")["cnt"].sum().reset_index().rename(columns={"cnt": "total_count"}))
    return registered_customer_df

def calculate_totals(df):
    total_casual = df["casual"].sum()
    total_registered = df["registered"].sum()
    return total_casual, total_registered

file_path = "dashboard/day_df.csv"
day_df = pd.read_csv(file_path)
day_df["dteday"] = pd.to_datetime(day_df["dteday"])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    st.image("https://storage.googleapis.com/kaggle-datasets-images/130897/312329/20c79bcd928e6d481fca7d5dc9fa3ca4/dataset-cover.jpg?t=2019-05-24-07-06-55")
    
    unique_dates = day_df["dteday"].dt.date.unique()
    selected_date = st.selectbox("Pilih Tanggal:", unique_dates)

main_df = day_df[day_df["dteday"] == pd.Timestamp(selected_date)]

casual_customer_count = create_casual_customer_count(main_df)
registered_customer_count = create_registered_customer_count(main_df)
total_casual, total_registered = calculate_totals(day_df)

st.header('Bike Sharing Dashboard')
st.write(f"Data untuk tanggal: {selected_date}")

# Menampilkan jumlah pengguna per-hari
col1, col2 = st.columns(2)
with col1:
    casual_customer = casual_customer_count.total_count.sum()
    st.metric("Total Casual Customer", value=casual_customer_count["casual"].sum())

with col2:
    registered_customer = registered_customer_count.total_count.sum() 
    st.metric("Total Registered Customer", value=registered_customer_count["total_count"].sum())

# Menampilkan grafik total pengguna keseluruhan
st.subheader("Visualisasi Jumlah Pengguna")
data = pd.DataFrame(
    {
        "User Type": ["Casual", "Registered"],
        "Total Rentals": [total_casual, total_registered],
    }
)

fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(
    x="User Type",
    y="Total Rentals",
    data=data,
    ax=ax,
    width=0.5,
)

ax.set_xlabel("Tipe Pengguna", fontsize=10)
ax.set_ylabel("Total Penyewaan", fontsize=10)
ax.bar_label(ax.containers[0], fmt='%d')
st.pyplot(fig)

# Menampilkan pengaruh suhu terhadap penyewaan sepeda
st.subheader("Pengaruh Suhu Terhadap Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(
    data=day_df,
    x="temp_actual", 
    y="cnt",
    alpha=0.5,
    ax=ax
)

ax.set_xlabel("Suhu (°C)", fontsize=10)
ax.set_ylabel("Jumlah Penyewaan Sepeda", fontsize=10)
ax.grid(True)
st.pyplot(fig)

total_rent_perday = day_df.groupby('workingday')['cnt'].sum().reset_index()
total_rent_perday['workingday'] = total_rent_perday['workingday'].replace({1: "Hari Kerja", 0: "Hari Non-Kerja"})

# Menampilkan perbandingan penyewa pada hari kerja vs non-kerja
st.subheader("Perbedaan Penyewa pada Hari Kerja vs Non-Kerja")
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(
    data=total_rent_perday,
    x="workingday", 
    y="cnt",
    ax=ax
)

ax.set_xlabel("Jenis Hari", fontsize=10)
ax.set_ylabel("Total Sepeda yang Disewa", fontsize=10)
ax.bar_label(ax.containers[0], fmt='%d')
st.pyplot(fig)

# Menampilkan pengaruh musim terhadap penyewaan sepeda
st.subheader("Pengaruh Musim Terhadap Penyewaan Sepeda")
total_rent_per_weather = day_df.groupby('season')['cnt'].sum().reset_index()
total_rent_per_weather['season'] = total_rent_per_weather['season'].replace({1: 'Semi', 2: 'Panas', 3:'Gugur', 4: 'Dingin'})

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(
    data=total_rent_per_weather,
    x="season", 
    y="cnt",
    ax=ax
)

ax.set_xlabel("Musim", fontsize=10)
ax.set_ylabel("Total Sepeda yang Disewa", fontsize=10)
ax.bar_label(ax.containers[0], fmt='%d') 
st.pyplot(fig)