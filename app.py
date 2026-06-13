import streamlit as st
import pandas as pd
import joblib
import time
import plotly.express as px


df = pd.read_csv('house.csv')
threshold = df["Price"].quantile(0.99)
df = df[df["Price"] <= threshold]
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
with open("Address.txt", "r") as f:
    addresses = [
        line.strip()
        for line in f.readlines()
        if line.strip()
    ] 
@st.cache_resource
def load_model():
    return joblib.load("pipeline_predict_churn.pkl")

model = load_model()

# -------------------------
# tabs
# -------------------------
tab1 , tab2 = st.tabs(['Home' , 'Chart'])


# -------------------------
# Header home page
# -------------------------
with tab1 :
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
        max_value=500,
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
            value=f"{price*4:,.0f} Toman"
        )


# -------------------------
# Header chart page
# -------------------------
with tab2:
    result = df.groupby("Address")["Price"].agg(["mean", "min", "max"]).reset_index()

    result = result.sort_values("mean", ascending=False).head(20)

    methods = {
        "Average Price": "mean",
        "Lowest Price": "min",
        "Highest Price": "max"
    }

    user_input = st.selectbox("Select metric", list(methods.keys()))

    fig = px.bar(
        result,
        x="Address",
        y=methods[user_input],  
        title=f"{user_input} House Price by Address"
    )

    st.plotly_chart(fig )
