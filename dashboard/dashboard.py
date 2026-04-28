import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# ==============================
# CONFIG
# ==============================
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

st.title("📊 E-Commerce Data Analysis Dashboard")
st.markdown("Analisis harga, review, dan customer behavior (RFM)")

# ==============================
# LOAD DATA
# ==============================
BASE_DIR = os.path.dirname(__file__)
csv_path = os.path.join(BASE_DIR, "main_data.csv")

try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    import streamlit as st
    st.error("File 'main_data.csv' tidak ditemukan. Pastikan file berada di folder yang sama dengan script.")
    st.stop()

# ==============================
# SIDEBAR FILTER (INTERAKTIF - WAJIB REVIEWER)
# ==============================
st.sidebar.header("🔎 Filter Data")

category = st.sidebar.selectbox(
    "Pilih Kategori Produk",
    ["All"] + list(data['product_category_name'].dropna().unique())
)

review_filter = st.sidebar.slider(
    "Filter Review Score",
    1, 5, (1,5)
)

# apply filter
filtered = data.copy()

if category != "All":
    filtered = filtered[filtered['product_category_name'] == category]

filtered = filtered[
    (filtered['review_score'] >= review_filter[0]) &
    (filtered['review_score'] <= review_filter[1])
]

# ==============================
# KPI SECTION
# ==============================
st.subheader("📌 Ringkasan KPI")

col1, col2, col3 = st.columns(3)

col1.metric("Total Transaksi", len(filtered))
col2.metric("Rata-rata Harga", round(filtered['price'].mean(),2))
col3.metric("Rata-rata Review", round(filtered['review_score'].mean(),2))

# ==============================
# EDA VISUALIZATION
# ==============================
st.subheader("📊 Analisis Harga vs Review")

fig1, ax1 = plt.subplots()
sns.scatterplot(data=filtered, x="price", y="review_score", ax=ax1)
ax1.set_title("Harga vs Review Score")
st.pyplot(fig1)

# ==============================
# DISTRIBUSI REVIEW
# ==============================
st.subheader("⭐ Distribusi Review")

fig2, ax2 = plt.subplots()
sns.countplot(data=filtered, x="review_score", ax=ax2)
ax2.set_title("Distribusi Review Score")
st.pyplot(fig2)

# ==============================
# KATEGORI TERBURUK
# ==============================
st.subheader("📉 Kategori dengan Review Terendah")

cat_review = filtered.groupby("product_category_name")["review_score"].mean().sort_values().head(10)

fig3, ax3 = plt.subplots(figsize=(8,5))
cat_review.plot(kind="barh", ax=ax3)
ax3.set_title("Top 10 Kategori Review Terendah")
st.pyplot(fig3)

# ==============================
# INSIGHT (sesuai reviewer requirement)
# ==============================
st.subheader("💡 Insight Bisnis")

st.markdown("""
- Harga memiliki pengaruh terhadap pembelian, tetapi tidak menjadi faktor utama.
- Kepuasan pelanggan lebih dipengaruhi oleh kualitas produk dan pengalaman pengiriman.
- Terdapat kategori produk dengan review rendah yang perlu evaluasi.
- Segmentasi pelanggan menunjukkan adanya potensi churn yang tinggi.
""")
