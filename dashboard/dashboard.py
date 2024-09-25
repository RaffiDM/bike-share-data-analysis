import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

day_df = pd.read_csv('../data/day.csv')
hour_df = pd.read_csv('../data/hour.csv')

day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

# sidebar filter
st.sidebar.header('Filter Data')
start_date = st.sidebar.date_input("Start Date", day_df["dteday"].min())
end_date = st.sidebar.date_input("End Date", day_df["dteday"].max())

filtered_day_df = day_df[(day_df["dteday"] >= pd.to_datetime(start_date)) & (day_df["dteday"] <= pd.to_datetime(end_date))]
filtered_hour_df = hour_df[(hour_df["dteday"] >= pd.to_datetime(start_date)) & (hour_df["dteday"] <= pd.to_datetime(end_date))]

# main
st.title('Dashboard Penyewaan Sepeda')

total_penyewaan = filtered_day_df['cnt'].sum()
rata_penyewaan_harian = filtered_day_df['cnt'].mean()

total_kasual = filtered_day_df['casual'].sum()
total_terdaftar = filtered_day_df['registered'].sum()

col1, col2 = st.columns(2)

with col1:
    st.metric('Total Penyewaan Sepeda', total_penyewaan)

with col2:
    st.metric('Rata - Rata Penyewaan Harian', f"{rata_penyewaan_harian:.2f}")

col3, col4 = st.columns(2)

with col3:
    st.metric('Total Pengguna Kasual', total_kasual)

with col4:
    st.metric('Total Pengguna Terdaftar', total_terdaftar)

# 1. Rata-rata penyewaan berdasarkan musim
st.header('Rata - Rata Penyewaan Berdasarkan Musim')
season_avg = filtered_day_df.groupby('season')['cnt'].mean().sort_values(ascending=False)
season_df = pd.DataFrame({
    'Musim': ['Gugur', 'Panas', 'Dingin', 'Semi'], 
    'Rata-Rata Penyewaan': season_avg.values
})

colors = ['gray' if (x != season_avg.max()) else 'orange' for x in season_avg]

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Musim', y='Rata-Rata Penyewaan', data=season_df, palette=colors, ax=ax)

for index, value in enumerate(season_avg):
    ax.text(index, value, f"{value:.2f}", ha='center', va='bottom')

ax.set_title('Rata - Rata Jumlah Sepeda yang Disewa Berdasarkan Musim')
ax.set_xlabel('Musim')
ax.set_ylabel('Rata - Rata Penyewaan Sepeda')
st.pyplot(fig)

# 2. Trend penyewaan berdasarkan jam
st.header('Trend Penyewaan Sepeda Berdasarkan Jam')
hourly_avg = filtered_hour_df.groupby('hr')['cnt'].mean()

fig2, ax2 = plt.subplots(figsize=(10, 6))
hourly_avg.plot(kind='line', marker='o', ax=ax2)
ax2.set_title('Rata - Rata Jumlah Sepeda yang Disewa Berdasarkan Jam')
ax2.set_xlabel('Jam')
ax2.set_ylabel('Rata - Rata Jumlah Peminjaman Sepeda')
ax2.set_xticks(range(24))
ax2.grid(True)
st.pyplot(fig2)

# 3. kasual vs terdaftar
st.header('Perbandingan Penyewaan Sepeda Pengguna Kasual vs Terdaftar')
user_type_avg = filtered_day_df[['casual', 'registered']].mean()
user_type_df = pd.DataFrame({
    'Tipe Pengguna': ['Kasual', 'Terdaftar'],
    'Rata-Rata Penyewaan': user_type_avg.values
})

colors = ['gray' if (x != user_type_avg.max()) else 'orange' for x in user_type_avg]

fig3, ax3 = plt.subplots(figsize=(8,5))
sns.barplot(x='Tipe Pengguna', y='Rata-Rata Penyewaan', data=user_type_df, palette=colors, ax=ax3)

for index, value in enumerate(user_type_avg):
    ax3.text(index, value, f'{value:.2f}', ha='center', va='bottom')

ax3.set_title('Rata-Rata Penyewaan Sepeda: Pengguna Kasual vs Terdaftar')
ax3.set_xlabel('Tipe Pengguna')
ax3.set_ylabel('Rata-Rata Penyewaan Sepeda')
st.pyplot(fig3)

st.caption('Bike Share Dashboard by RaffiDM')

