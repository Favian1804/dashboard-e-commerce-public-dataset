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
st.markdown("Analisis harga, review, dan customer behavior (RFM sederhana)")

# ==============================
# LOAD DATA
# ==============================
BASE_DIR = os.path.dirname(__file__)
csv_path = os.path.join(BASE_DIR, "main_data.csv")

df = pd.read_csv(csv_path)

# ==============================
# VALIDASI KOLOM (ANTI ERROR)
# ==============================
required_cols = ["product_category_name", "review_score", "price"]

for col in required_cols:
    if col not in df.columns:
        st.error(f"Kolom '{col}' tidak ditemukan di dataset!")
        st.stop()

# ==============================
# SIDEBAR FILTER
# ==============================
st.sidebar.header("🔎 Filter Data")

category = st.sidebar.selectbox(
    "Pilih Kategori Produk",
    ["All"] + sorted(df["product_category_name"].dropna().unique())
)

review_filter = st.sidebar.slider(
    "Filter Review Score",
    1, 5, (1, 5)
)

# ==============================
# APPLY FILTER
# ==============================
filtered = df.copy()

if category != "All":
    filtered = filtered[filtered["product_category_name"] == category]

filtered = filtered[
    (filtered["review_score"] >= review_filter[0]) &
    (filtered["review_score"] <= review_filter[1])
]

# ==============================
# KPI SECTION
# ==============================
st.subheader("📌 Ringkasan KPI")

col1, col2, col3 = st.columns(3)

col1.metric("Total Transaksi", len(filtered))
col2.metric("Rata-rata Harga", round(filtered["price"].mean(), 2))
col3.metric("Rata-rata Review", round(filtered["review_score"].mean(), 2))

# ==============================
# VISUALISASI 1
# ==============================
st.subheader("📊 Harga vs Review")

fig1, ax1 = plt.subplots()
sns.scatterplot(data=filtered, x="price", y="review_score", ax=ax1)
ax1.set_title("Harga vs Review Score")
st.pyplot(fig1)

# ==============================
# VISUALISASI 2
# ==============================
st.subheader("⭐ Distribusi Review")

fig2, ax2 = plt.subplots()
sns.countplot(data=filtered, x="review_score", ax=ax2)
ax2.set_title("Distribusi Review Score")
st.pyplot(fig2)

# ==============================
# VISUALISASI 3
# ==============================
st.subheader("📉 Kategori dengan Review Terendah")

cat_review = (
    filtered.groupby("product_category_name")["review_score"]
    .mean()
    .sort_values()
    .head(10)
)

fig3, ax3 = plt.subplots(figsize=(8, 5))
cat_review.plot(kind="barh", ax=ax3)
ax3.set_title("Top 10 Kategori Review Terendah")
st.pyplot(fig3)

# ==============================
# INSIGHT
# ==============================
st.subheader("💡 Insight Bisnis")

st.markdown("""
- Harga tidak selalu menentukan rating produk.
- Review rendah mengindikasikan masalah kualitas atau pengiriman.
- Beberapa kategori memiliki performa buruk dan perlu evaluasi.
- Filter interaktif membantu analisis lebih spesifik per segmen.
""")
