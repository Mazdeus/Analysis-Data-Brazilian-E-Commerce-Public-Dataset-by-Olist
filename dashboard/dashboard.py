# 1. Import Library
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style = "dark")

# 2. Menyiapkan Dataframe
# Menyiapkan helper function

# Untuk order dan revenue harian
def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule = "D", on = 'order_purchase_timestamp_x').agg({
        "order_id" : "nunique",
        "payment_value" : "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns = {
        "order_id" : "order_count",
        "payment_value" : "revenue"
    }, inplace = True)

    return daily_orders_df

# Menjumlahkan order kategori produk
def create_sum_order_category_df(df):
    sum_order_category_df = all_df.groupby(by = "product_category_name_english").order_id.nunique().sort_values(ascending = False).reset_index()
    sum_order_category_df.rename(columns = {
        "order_id" : "order_count",
        "product_category_name_english" : "category"
    }, inplace = True)

    return sum_order_category_df


# Menyiapkan demografi pelanggan
def create_bystate_df(df):
    bycity_df = all_df.groupby(by = "customer_state").customer_unique_id.nunique().reset_index()

    bycity_df.rename(columns = {
        "customer_unique_id" : "customer_count",
        "customer_state" : "state"
    }, inplace = True)

    return bycity_df

# Load berkas all_data.csv
all_df = pd.read_csv("all_data.csv")

# Mengurutkan dataframe berdasarkan order_purchase_timestamp_x
datetime_columns = ["order_purchase_timestamp_x"]
all_df.sort_values(by = "order_purchase_timestamp_x", inplace = True)
all_df.reset_index(inplace = True)

for col in datetime_columns:
    all_df[col] = pd.to_datetime(all_df[col])


# 3. Membuat Komponen Filter
# Widget date input dan logo
min_date = all_df["order_purchase_timestamp_x"].min()
max_date = all_df["order_purchase_timestamp_x"].max()

with st.sidebar:
    # Menambahkan logo
    st.image("logo_olist_store.png", width=200)

    for i in range(10):
        st.write("")

    # Mengambil start date dan end date dari date input
    start_date, end_date = st.date_input(
        label = "Rentang Waktu",
        min_value = min_date,
        max_value = max_date,
        value = [min_date, max_date]
    )

main_df = all_df[(all_df["order_purchase_timestamp_x"] >= str(start_date)) & (all_df["order_purchase_timestamp_x"] <= str(end_date))]

# Memanggil helper function
daily_orders_df = create_daily_orders_df(main_df)
sum_order_category_df = create_sum_order_category_df(main_df)
bystate_df = create_bystate_df(main_df)

# 4. Melengkapi Dashboard
st.header("Brazilian E-Commerce Dashboard :sparkles:")

# menampilkan tiga informasi terkait daily orders, yaitu jumlah order harian serta total order dan revenue dalam range waktu tertentu. 
st.subheader('Daily Orders')

col1, col2 = st.columns(2)

with col1:
    total_orders = daily_orders_df["order_count"].sum()
    st.metric("Total Orders", value = total_orders)

with col2:
    total_revenue = format_currency(daily_orders_df.revenue.sum(), "BRL", locale = "pt_BR")
    st.metric("Total Revenue", value = total_revenue)

fig, ax = plt.subplots(figsize = (16, 8))
ax.plot(
    daily_orders_df["order_purchase_timestamp_x"],
    daily_orders_df["order_count"],
    marker = "o",
    linewidth = 2,
    color = "#90CAF9"
)

ax.tick_params(axis = 'y', labelsize = 20)
ax.tick_params(axis = 'x', labelsize = 15)

st.pyplot(fig)

# Informasi penjualan kategori produk
st.subheader("Best and Worst Selling Categories")

fig, ax = plt.subplots(nrows = 1, ncols = 2, figsize=(35, 15))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(y = "category", x = "order_count", data = sum_order_category_df.head(5), palette = colors, ax = ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize = 30)
ax[0].set_title("Best Selling Categories", loc = "center",fontsize = 50)
ax[0].tick_params(axis = 'y', labelsize = 35)
ax[0].tick_params(axis = 'x', labelsize = 30)

sns.barplot(y = "category", x = "order_count", data = sum_order_category_df.sort_values(by = "order_count", ascending = True).head(5), palette = colors, ax = ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize = 30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Selling Categories", loc = "center", fontsize = 50)
ax[1].tick_params(axis = 'y', labelsize = 35)
ax[1].tick_params(axis = 'x', labelsize = 30)

st.pyplot(fig)

# Demografi Pelanggan berdasarkan State
st.subheader("Customer Demographics by State")

fig, ax = plt.subplots(figsize = (20, 10))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    x = "customer_count",
    y = "state",
    data = bystate_df.sort_values(by = "customer_count", ascending = False),
    palette = colors,
    ax = ax
)

ax.set_title("Number of Customer by States", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)
