import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
import streamlit as st 
from datetime import datetime
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='dteday').agg({
        "instant_x": "nunique",
        "cnt_x": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "instant_x": "order_count",
        "cnt_x": "sum_customers"
    }, inplace=True)
    
    return daily_orders_df

def create_byweather_df(df):
    weather_df = df.groupby(by="weathersit_desc").cnt_y.sum().reset_index()
    weather_df.rename(columns={
        "cnt_y": "customer_sum"
    }, inplace=True)
    return weather_df

def create_weekday_df(df):
    weekday_df = df.groupby("weekday_x").agg({
        "casual_y": "sum",
        "registered_y": "sum"
    }).reset_index()
    weekday_df.rename(columns={
        "casual_y" : "casual",
        "registered_y": "register"
    }, inplace=True)
    return weekday_df

def create_byseason_df(df):
    byseason_df = df.groupby(by="season_desc").cnt_y.sum().reset_index()
    return byseason_df

def create_rfm_df(df):
    rfm_df = df.groupby(by="mnth_x", as_index=False).agg({
        "dteday": "max", #mengambil tanggal order terakhir
        "instant_x": "nunique",
        "cnt_x": "sum"
    })
    rfm_df.columns = ["mnth_x", "max_order_timestamp", "frequency", "monetary"]
    
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = df["dteday"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days) 
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    
    return rfm_df

data_df = pd.read_csv("all_data(1).csv")

datetime_columns = ["dteday"]
data_df.sort_values(by="dteday", inplace=True)
data_df.reset_index(inplace=True)
 
for column in datetime_columns:
    data_df[column] = pd.to_datetime(data_df[column])

min_date = data_df["dteday"].min()
max_date = data_df["dteday"].max()
 
with st.sidebar:
    st.title('Bike Rental Dashboard')
    st.image("https://st2.depositphotos.com/57698706/50500/v/450/depositphotos_505000244-stock-illustration-orange-bike-in-front-of.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
main_df = data_df[(data_df["dteday"] >= str(start_date)) & 
                (data_df["dteday"] <= str(end_date))]

daily_orders_df = create_daily_orders_df(main_df)
byweather_df = create_byweather_df(main_df)
weekday_df = create_weekday_df(main_df)
byseason_df = create_byseason_df(main_df)
rfm_df = create_rfm_df(main_df)

st.header("Bike Rental Dashboard")
st.subheader("Summary Metrics")

col1, col2 = st.columns(2)
with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total Orders", value=total_orders)
 
with col2:
    total_casual = daily_orders_df.sum_customers.sum()
    st.metric("Total Pelanggan", value=total_casual)

fig, ax = plt.subplots(figsize=(10, 6))
st.header("Tren Total Order dan Pelanggan Harian")

sns.lineplot(
    x="dteday", 
    y="sum_customers", 
    data=daily_orders_df, 
    color="#90CAF9",
    linewidth=1
)

ax.set_title("Jumlah Pelanggan per Hari", fontsize=14)
ax.set_xlabel("Tanggal", fontsize=12)
ax.set_ylabel("Jumlah Pelanggan", fontsize=12)
ax.tick_params(axis="x", rotation=45) 
st.pyplot(fig)

st.header("Penyewaan sepeda selama satu tahun")
month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
data_df['mnth_desc'] = pd.Categorical(data_df['mnth_desc'], categories=month_order, ordered=True)
daily_rentals = data_df.groupby('mnth_desc').agg({'cnt_x': 'sum'}).reset_index()

fig1, ax1 = plt.subplots(figsize=(18, 7))
sns.lineplot(x='mnth_desc', y='cnt_x', data=daily_rentals, ax=ax1, marker='o',linewidth=3, color='skyblue')

ax1.set_title('Total Penyewaan Sepeda per Bulan tahun 2012', fontsize=16)
ax1.set_xlabel(None)
ax1.set_ylabel('Total Penyewaan', fontsize=12)
ax1.set_xticks(daily_rentals['mnth_desc'])
ax1.set_xticklabels(daily_rentals["mnth_desc"],fontsize=15)
ax1.grid(True)

st.pyplot(fig1)

st.subheader("Total Pemakaian Sepeda berdasarkan Cuaca")

fig, ax = plt.subplots(figsize=(18, 7))

sns.barplot(
    y="customer_sum", 
    x="weathersit_desc", 
    data=byweather_df,
    color='skyblue',
    ax=ax
)
ax.set_title("Jumlah penyewaan berdasarkan cuaca", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)

st.subheader('Perbandingan Pengguna Register dan Casual')
fig, ax = plt.subplots(figsize=(10, 5))

weekday_df_melted = weekday_df.melt(id_vars=["weekday_x"], 
                                    value_vars=["casual", "register"],
                                    var_name="User Type", 
                                    value_name="Total Users")

sns.barplot(x="weekday_x", y="Total Users", hue="User Type", 
            data=weekday_df_melted, palette=["skyblue", "lightcoral"], ax=ax)

ax.set_title("Total Pengguna Casual dan Register saat weekday", fontsize=16)
ax.set_xlabel("Weekday", fontsize=12)
ax.set_ylabel("Total Users", fontsize=12)

st.pyplot(fig)

st.subheader("Total Pemakaian Sepeda berdasarkan Musim")

fig, ax = plt.subplots(figsize=(10, 5))

sns.barplot(
    y="cnt_y", 
    x="season_desc", 
    data=byseason_df,
    color="#00BFFF",
    ax=ax
)
ax.set_title("Jumlah penyewaan sepeda berdasarkan musim", loc="center", fontsize=13)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
st.pyplot(fig)

st.subheader("Best Customer Based on RFM Parameters")
 
col1, col2, col3 = st.columns(3)
 
with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)
 
with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)
 
with col3:
    avg_frequency = format_currency(rfm_df.monetary.mean(), "AUD", locale='es_CO') 
    st.metric("Average Monetary", value=avg_frequency)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(45, 15))
colors = ["#00BFFF", "#00BFFF", "#00BFFF", "#00BFFF", "#00BFFF", "#00BFFF", "#00BFFF", "#00BFFF","#00BFFF", "#00BFFF","#00BFFF"]

# Grafik Recency
sns.barplot(x="mnth_x", y="recency", data=rfm_df, palette=colors, ax=ax[0])

ax[0].set_title("Recency Penyewaan per Bulan", fontsize=40)
ax[0].set_xlabel("Bulan", fontsize=25)
ax[0].set_ylabel(None)

# Grafik Frequency
sns.barplot(x="mnth_x", y="frequency", data=rfm_df, palette=colors, ax=ax[1])
ax[1].set_title("Frequency Penyewaan per Bulan", fontsize=40)
ax[1].set_xlabel("Bulan", fontsize=25)
ax[1].set_ylabel(None)

# Grafik Monetary
sns.barplot(x="mnth_x", y="monetary", data=rfm_df, palette=colors, ax=ax[2])
ax[2].set_title("Monetary Penyewaan per Bulan", fontsize=40)
ax[2].set_xlabel("Bulan", fontsize=25)
ax[2].set_ylabel(None)

st.pyplot(fig)

for i, col in enumerate(["recency", "frequency", "monetary"]):
    for index, value in enumerate(rfm_df[col]):
        ax[i].text(index, value + 1, str(value), ha="center", fontsize=12)

plt.tight_layout()
plt.show()
