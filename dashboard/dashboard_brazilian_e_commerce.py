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