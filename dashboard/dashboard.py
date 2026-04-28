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
@st.cache_data
def load_data():
    df = pd.read_csv('main_data.csv')
    return df

df = load_data()

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
# RFM ANALYSIS
# ========================
st.subheader("👥 RFM Analysis")

df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

rfm = df.groupby('customer_id').agg({
    'order_purchase_timestamp': lambda x: (df['order_purchase_timestamp'].max() - x.max()).days,
    'order_id': 'count',
    'price': 'sum'
}).reset_index()

rfm.columns = ['customer_id', 'Recency', 'Frequency', 'Monetary']

# Scoring
rfm['R_score'] = pd.qcut(rfm['Recency'], 4, labels=[4,3,2,1])
rfm['F_score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1,2,3,4])
rfm['M_score'] = pd.qcut(rfm['Monetary'], 4, labels=[1,2,3,4])

rfm['R_score'] = rfm['R_score'].astype(int)
rfm['F_score'] = rfm['F_score'].astype(int)
rfm['M_score'] = rfm['M_score'].astype(int)

def segment(row):
    if row['R_score'] == 4 and row['F_score'] == 4:
        return 'Best Customers'
    elif row['R_score'] >= 3 and row['F_score'] >= 3:
        return 'Loyal Customers'
    else:
        return 'At Risk'

rfm['segment'] = rfm.apply(segment, axis=1)

segment_count = rfm['segment'].value_counts()

fig3, ax3 = plt.subplots()
segment_count.plot(kind='bar', ax=ax3)
ax3.set_ylabel("Jumlah Customer")
st.pyplot(fig3)

# ========================
# RAW DATA
# ========================
st.subheader("📄 Data Sample")
st.dataframe(df.head(100))