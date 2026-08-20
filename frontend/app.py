import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend - "backend" is the container name assigned when
# running the Docker container, resolved automatically via the shared Docker network
BACKEND_URL = "http://backend:7860"

# Streamlit UI for SuperKart Sales Prediction
st.title("SuperKart Sales Prediction App")
st.write("This app predicts the total sales revenue (`Product_Store_Sales_Total`) a product is expected to generate at a given store.")
st.write("Adjust the inputs below to get a prediction.")

# Collect user input using sliders for numerical features
Product_Weight = st.slider("Product Weight", 4.0, 22.0, 12.6, 0.1)
Product_Allocated_Area = st.slider("Product Allocated Area (share of store display area)", 0.004, 0.298, 0.069, 0.001)
Product_MRP = st.slider("Product MRP (maximum retail price)", 31.0, 266.0, 147.0, 0.5)
Store_Age = st.slider("Store Age (years since establishment)", 0, 22, 10, 1)

# Collect user input using select boxes for categorical features
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
Product_Type = st.selectbox(
    "Product Type",
    [
        "Fruits and Vegetables", "Snack Foods", "Frozen Foods", "Dairy", "Household",
        "Baking Goods", "Canned", "Health and Hygiene", "Meat", "Soft Drinks",
        "Breads", "Hard Drinks", "Others", "Starchy Foods", "Breakfast", "Seafood",
    ],
)
Store_Size = st.selectbox("Store Size", ["High", "Medium", "Small"])
Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox(
    "Store Type", ["Departmental Store", "Supermarket Type1", "Supermarket Type2", "Food Mart"]
)

# Create input dictionary matching the features expected by the backend API
input_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_Type": Product_Type,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Store_Age": Store_Age,
}

# Single Prediction
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/sales", json=input_data)
    if response.status_code == 200:
        result = response.json()
        predicted_sales = result["Predicted_Product_Store_Sales_Total"]
        st.success(f"🛒 Predicted Sales Revenue: **{predicted_sales:.2f}**")
    else:
        st.error("Unable to connect to the prediction API.")

# Batch Prediction
st.subheader("Batch Prediction")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file is not None:
    if st.button("Predict for Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/salesbatch", files={"file": uploaded_file})
        if response.status_code == 200:
            results = response.json()
            st.success("Predictions completed successfully!")
            st.dataframe(pd.DataFrame(results), use_container_width=True)
        else:
            st.error("Unable to connect to the prediction API.")
