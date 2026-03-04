import streamlit as st
import joblib
import numpy as np

model = joblib.load("smart_building_model.pkl")

st.title("AI Smart Building Energy Predictor")

st.write("Predict building energy consumption using sensor data")

temperature = st.slider("Temperature (°C)", 15.0, 40.0, 25.0)
humidity = st.slider("Humidity (%)", 20.0, 90.0, 50.0)
occupancy = st.slider("Occupancy", 0, 100, 10)
co2 = st.slider("CO2 Level (ppm)", 300.0, 1500.0, 600.0)
light = st.slider("Light Intensity", 0.0, 1000.0, 400.0)
hvac = st.slider("HVAC Usage", 0.0, 1.0, 0.5)
health = st.slider("Equipment Health", 0.0, 1.0, 0.9)
hour = st.slider("Hour of Day", 0, 23, 12)

if st.button("Predict Energy Consumption"):

    features = np.array([[temperature, humidity, occupancy,
                          co2, light, hvac, health, hour]])

    prediction = model.predict(features)[0]

    st.success(f"Predicted Energy Consumption: {prediction:.2f} kWh")

st.markdown("---")
st.caption("AI Smart Building Infrastructure Project")