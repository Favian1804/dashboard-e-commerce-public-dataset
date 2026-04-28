import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ========================
# CONFIG
# ========================
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

st.title("📊 Dashboard Analisis E-Commerce")

# ========================
# LOAD DATA
# ========================
import pandas as pd
import os

BASE_DIR = os.path.dirname(__file__)
csv_path = os.path.join(BASE_DIR, "main_data.csv")

df = pd.read_csv(csv_path)

# ========================
# DATA CLEANING (basic)
# ========================
df = df[df['price'] > 0]

# ========================
# SIDEBAR FILTER
# ========================
st.sidebar.header("🔎 Filter Data")

min_price = int(df['price'].min())
max_price = int(df['price'].max())

price_range = st.sidebar.slider(
    "Filter Harga",
    min_price,
    max_price,
    (min_price, max_price)
)

df = df[(df['price'] >= price_range[0]) & (df['price'] <= price_range[1])]

# ========================
# KPI
# ========================
total_sales = df['price'].sum()
total_orders = df['order_id'].nunique()
avg_price = df['price'].mean()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", f"{total_sales:,.0f}")
col2.metric("📦 Total Orders", total_orders)
col3.metric("🏷️ Avg Price", f"{avg_price:,.0f}")

# ========================
# PERTANYAAN 1
# Harga vs Jumlah Pembelian
# ========================
st.subheader("📉 Harga vs Jumlah Pembelian")

price_freq = df.groupby('price')['order_id'].count().reset_index()

fig1, ax1 = plt.subplots()
ax1.scatter(price_freq['price'], price_freq['order_id'])
ax1.set_xlabel("Harga")
ax1.set_ylabel("Jumlah Pembelian")
st.pyplot(fig1)

# ========================
# PERTANYAAN 2
# Review Analysis
# ========================
st.subheader("⭐ Distribusi Review Score")

review_dist = df['review_score'].value_counts().sort_index()

fig2, ax2 = plt.subplots()
review_dist.plot(kind='bar', ax=ax2)
ax2.set_xlabel("Review Score")
ax2.set_ylabel("Jumlah")
st.pyplot(fig2)


# ========================
# RAW DATA
# ========================
st.subheader("📄 Data Sample")
st.dataframe(df.head(100))
