import streamlit as st
import joblib
import numpy as np
import plotly.graph_objects as go

# Load trained model
model = joblib.load("smart_building_model.pkl")

# Page configuration
st.set_page_config(
    page_title="Smart Building Energy Dashboard",
    page_icon="🏢",
    layout="wide"
)

# Title
st.title("🏢 AI Smart Building Energy Intelligence Dashboard")
st.markdown("### Real-time Energy Consumption Prediction & Building Efficiency Monitoring")

st.markdown("---")

# Sidebar for Inputs
st.sidebar.header("Building Sensor Inputs")

temperature = st.sidebar.slider("Temperature (°C)", 15.0, 40.0, 25.0)
humidity = st.sidebar.slider("Humidity (%)", 20.0, 90.0, 50.0)
occupancy = st.sidebar.slider("Occupancy", 0, 100, 10)
co2 = st.sidebar.slider("CO2 Level (ppm)", 300.0, 1500.0, 600.0)
light = st.sidebar.slider("Light Intensity", 0.0, 1000.0, 400.0)
hvac = st.sidebar.slider("HVAC Usage", 0.0, 1.0, 0.5)
health = st.sidebar.slider("Equipment Health", 0.0, 1.0, 0.9)
hour = st.sidebar.slider("Hour of Day", 0, 23, 12)

# Layout columns
col1, col2 = st.columns([1,1])

# Prediction
with col1:

    st.subheader("⚡ Energy Prediction")

    if st.button("Predict Energy Consumption"):

        features = np.array([[temperature, humidity, occupancy,
                              co2, light, hvac, health, hour]])

        prediction = model.predict(features)[0]

        st.success(f"Predicted Energy Consumption: {prediction:.2f} kWh")

        efficiency = max(0, 100 - (prediction/10))

        st.metric("Building Efficiency Score", f"{efficiency:.1f}%")

# 3D Building Visualization
with col2:

    st.subheader("🏢 Interactive Building Energy View")

    x = [0,0,1,1,0,0,1,1]
    y = [0,1,1,0,0,1,1,0]
    z = [0,0,0,0,1,1,1,1]

    fig = go.Figure(data=[
        go.Mesh3d(
            x=x,
            y=y,
            z=z,
            color='lightblue',
            opacity=0.50
        )
    ])

    fig.update_layout(
        title="3D Smart Building Model",
        scene=dict(
            xaxis_title='Width',
            yaxis_title='Length',
            zaxis_title='Height'
        )
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Energy Insights
st.subheader("📊 Energy Insights")

col3, col4, col5 = st.columns(3)

col3.metric("Temperature", f"{temperature} °C")
col4.metric("Humidity", f"{humidity} %")
col5.metric("CO2 Level", f"{co2} ppm")

st.markdown("---")

st.caption("AI Powered Smart Infrastructure Monitoring System")
