import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

# Load model
model = joblib.load("final_ada_model.pkl")

# Label encoder (global for consistency)
le = LabelEncoder()

# Feature engineering
def preprocess_input(df):
    df['Demand_Supply_Ratio'] = df['Number_of_Riders'] / (df['Number_of_Drivers'] + 1)
    df['Ride_Experience_Level'] = pd.cut(df['Number_of_Past_Rides'], bins=[-1, 5, 20, 50, 1000], labels=['New', 'Low', 'Medium', 'High'])
    df['Rating_Level'] = pd.cut(df['Average_Ratings'], bins=[0, 3, 4, 5], labels=['Low', 'Medium', 'High'])

    # Label encoding
    for col in df.columns:
        if df[col].dtype == 'object' or df[col].dtype.name == 'category':
            df[col] = le.fit_transform(df[col].astype(str))

    return df

# Dynamic pricing
def dynamic_pricing_adjusted(row):
    row_for_prediction = pd.DataFrame([row])
    
    # Tambahkan kolom yang hilang
    for col in model.feature_names_in_:
        if col not in row_for_prediction.columns:
            row_for_prediction[col] = 0

    row_for_prediction = row_for_prediction[model.feature_names_in_]
    
    base_price = model.predict(row_for_prediction)[0]

    if row['Expected_Ride_Duration'] < 15:
        base_price *= 0.9
    elif row['Expected_Ride_Duration'] > 45:
        base_price *= 1.2

    if row['Time_of_Booking'] == 1:  # evening
        base_price *= 1.15
    elif row['Time_of_Booking'] == 2:  # night
        base_price *= 1.25

    if row['Vehicle_Type'] == 2:  # premium
        base_price *= 1.10

    return round(base_price, 2)

# --- Streamlit UI ---
st.title("🚖 Dynamic Pricing Estimator")

with st.form("ride_input_form"):
    st.subheader("Isi Data Ride")

    riders = st.number_input("Number of Riders", min_value=0)
    drivers = st.number_input("Number of Drivers", min_value=0)
    location = st.selectbox("Location Category", ["Urban", "Suburban", "Rural"])
    loyalty = st.selectbox("Customer Loyalty Status", ["Regular", "Silver", "Gold"])
    past_rides = st.number_input("Number of Past Rides", min_value=0)
    rating = st.slider("Average Ratings", min_value=0.0, max_value=5.0, step=0.01)
    time_booking = st.selectbox("Time of Booking", ["Morning", "Evening", "Night"])  # mapping nanti
    vehicle = st.selectbox("Vehicle Type", ["Economy", "Premium"])
    duration = st.number_input("Expected Ride Duration (minutes)", min_value=0)
    cost = st.number_input("Historical Cost of Ride", min_value=0.0)

    submitted = st.form_submit_button("Predict Price")

if submitted:
    # Mapping kategori
    time_map = {"Morning": 0, "Evening": 1, "Night": 2}
    vehicle_map = {"Economy": 1, "Premium": 2}  # agar sesuai logic dynamic price

    input_dict = {
        "Number_of_Riders": riders,
        "Number_of_Drivers": drivers,
        "Location_Category": location,
        "Customer_Loyalty_Status": loyalty,
        "Number_of_Past_Rides": past_rides,
        "Average_Ratings": rating,
        "Time_of_Booking": time_map[time_booking],
        "Vehicle_Type": vehicle_map[vehicle],
        "Expected_Ride_Duration": duration,
        "Historical_Cost_of_Ride": cost
    }

    df_input = pd.DataFrame([input_dict])
    df_processed = preprocess_input(df_input)
    price = dynamic_pricing_adjusted(df_processed.iloc[0])

    st.success(f"💰 Estimated Dynamic Price: **${price}**")


