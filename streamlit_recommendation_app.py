
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

@st.cache_data
def load_data():
    products = pd.read_excel("Dropshipping_Recommendation_System_2024.xlsx", sheet_name="Products")
    customers = pd.read_excel("Dropshipping_Recommendation_System_2024.xlsx", sheet_name="Customers")
    orders = pd.read_excel("Dropshipping_Recommendation_System_2024.xlsx", sheet_name="Orders")
    similarity_matrix = pd.read_excel("Dropshipping_Recommendation_System_2024.xlsx", sheet_name="Customer Similarity", index_col=0)
    return products, customers, orders, similarity_matrix

products, customers, orders, similarity_matrix = load_data()

# إنشاء مصفوفة المستخدم-المنتج
user_product_matrix = orders.pivot_table(index="CustomerID", columns="ProductID", aggfunc="size", fill_value=0)

# تحديث واجهة التطبيق
st.title("🛍️ AI-Powered Product Recommendation System")
st.write("Welcome to the AI-driven recommendation system for Dropshipping stores!")

# اختيار رقم العميل
customer_id = st.selectbox("Select Customer ID:", customers["CustomerID"])

# عرض بيانات العميل
customer_info = customers[customers["CustomerID"] == customer_id]
st.write("### Customer Information")
st.write(customer_info)

# المنتجات التي اشتراها العميل
st.write("### Products Purchased by the Customer")
customer_orders = orders[orders["CustomerID"] == customer_id].merge(products, on="ProductID")
st.write(customer_orders[["ProductName", "Category", "Price", "OrderDate"]])

# إنشاء توصيات بناءً على تشابه العملاء
st.write("### Recommended Products for You")
if customer_id in similarity_matrix.index:
    similar_customers = similarity_matrix[customer_id].sort_values(ascending=False).index[1:6]  # أقرب 5 عملاء
    recommended_products = orders[orders["CustomerID"].isin(similar_customers)]["ProductID"].value_counts().index[:5]
    recommendations = products[products["ProductID"].isin(recommended_products)]
    st.write(recommendations[["ProductName", "Category", "Price"]])
else:
    st.write("No recommendations available for this customer.")

# المنتجات الأكثر مبيعًا
st.write("### Top Selling Products")
top_selling_products = orders["ProductID"].value_counts().index[:5]
top_products = products[products["ProductID"].isin(top_selling_products)]
st.write(top_products[["ProductName", "Category", "Price"]])
