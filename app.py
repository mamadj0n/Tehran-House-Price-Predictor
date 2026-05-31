import streamlit as st
import pandas as pd
import joblib
import time

# -------------------------
# Page Config
# -------------------------

st.set_page_config(
    page_title="Tehran House Price Predictor",
    page_icon="🏠",
    layout="wide"
)

# -------------------------
# Load Model
# -------------------------
with open("Punak Pardis West Ferdows.txt", "r") as f:
    addresses = [
        line.strip()
        for line in f.readlines()
        if line.strip()
    ] 
@st.cache_resource
def load_model():
    return joblib.load("house_price_catboost_2.pkl")

model = load_model()

# -------------------------
# Header
# -------------------------

st.title("🏠 Tehran House Price Predictor")

st.markdown(
    "Predict house prices using Machine Learning"
)


st.image("/home/modso/Pictures/Teharn.jpg", use_container_width=True)
# -------------------------
# Sidebar
# -------------------------

st.header("House Features")

area = st.slider(
    "Area (m²)",
    min_value=20,
    max_value=250,
    value=100
)

room = st.slider(
    "Rooms",
    min_value=1,
    max_value=10,
    value=2
)

parking = st.checkbox("Parking")

warehouse = st.checkbox("Warehouse")

elevator = st.checkbox("Elevator")

address = st.selectbox(
    "🔍 Neighborhood",
    sorted(addresses),
    index=None,
    placeholder="Search and select a neighborhood..."
)
# -------------------------
# Input DataFrame
# -------------------------

input_df = pd.DataFrame({
    "Area": [area],
    "Room": [room],
    "Parking": [int(parking)],
    "Warehouse": [int(warehouse)],
    "Elevator": [int(elevator)],
    "Address": [address]
})

st.subheader("Input Features")

st.dataframe(input_df)



# -------------------------
# Prediction
# -------------------------

if st.button("Predict Price"):

    if address is None:
        st.error("Please select a neighborhood.")
        st.stop()

    my_bar = st.progress(0)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1)

    prediction = model.predict(input_df)

    price = prediction[0]

    st.success("Prediction completed successfully!")

    st.metric(
        label="Estimated House Price",
        value=f"{price*3:,.0f} Toman"
    )