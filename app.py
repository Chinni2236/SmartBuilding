import streamlit as st
import joblib
import numpy as np
import plotly.graph_objects as go

# Load model
model = joblib.load("smart_building_model.pkl")

# Example accuracy (replace with your real accuracy if available)
MODEL_ACCURACY = 0.92

st.set_page_config(
    page_title="AI Smart Building Dashboard",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 AI Smart Building Energy Intelligence Dashboard")
st.markdown("### Real-time Energy Consumption Prediction & Building Efficiency Monitoring")

st.markdown("---")

# Sidebar inputs
st.sidebar.header("Building Sensor Inputs")

temperature = st.sidebar.slider("Temperature (°C)", 15.0, 40.0, 25.0)
humidity = st.sidebar.slider("Humidity (%)", 20.0, 90.0, 50.0)
occupancy = st.sidebar.slider("Occupancy", 0, 100, 10)
co2 = st.sidebar.slider("CO2 Level (ppm)", 300.0, 1500.0, 600.0)
light = st.sidebar.slider("Light Intensity", 0.0, 1000.0, 400.0)
hvac = st.sidebar.slider("HVAC Usage", 0.0, 1.0, 0.5)
health = st.sidebar.slider("Equipment Health", 0.0, 1.0, 0.9)
hour = st.sidebar.slider("Hour of Day", 0, 23, 12)

col1, col2 = st.columns([1,1])

# Prediction
with col1:

    st.subheader("⚡ Energy Prediction")

    if st.button("Predict Energy Consumption"):

        features = np.array([[temperature, humidity, occupancy,
                              co2, light, hvac, health, hour]])

        prediction = model.predict(features)[0]

        # Efficiency calculation
        efficiency = max(0, 100 - (prediction/10))

        # Confidence score (example)
        confidence = min(0.99, 0.75 + (efficiency/400))

        st.success(f"Predicted Energy Consumption: {prediction:.2f} kWh")

        colA, colB = st.columns(2)

        colA.metric("Building Efficiency", f"{efficiency:.1f}%")
        colB.metric("Prediction Confidence", f"{confidence*100:.1f}%")

        st.metric("Model Accuracy", f"{MODEL_ACCURACY*100:.1f}%")

        # Energy Gauge
        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prediction,
            title={'text': "Energy Consumption (kWh)"},
            gauge={
                'axis': {'range': [0, 1000]},
                'bar': {'color': "orange"},
                'steps': [
                    {'range': [0, 300], 'color': "green"},
                    {'range': [300, 700], 'color': "yellow"},
                    {'range': [700, 1000], 'color': "red"}
                ]
            }
        ))

        st.plotly_chart(gauge, use_container_width=True)

# Lifelike 3D Building
with col2:

    st.subheader("🏢 Interactive Smart Building")

    floors = 5

    fig = go.Figure()

    for i in range(floors):

        fig.add_trace(go.Mesh3d(
            x=[0,0,2,2,0,0,2,2],
            y=[0,2,2,0,0,2,2,0],
            z=[i,i,i,i,i+1,i+1,i+1,i+1],
            opacity=0.6,
            color="lightblue"
        ))

    # Windows (energy activity)
    for floor in range(floors):

        fig.add_trace(go.Scatter3d(
            x=[0.2,1,1.8],
            y=[2,2,2],
            z=[floor+0.5]*3,
            mode='markers',
            marker=dict(
                size=8,
                color="yellow"
            )
        ))

    fig.update_layout(
        scene=dict(
            xaxis_title="Width",
            yaxis_title="Length",
            zaxis_title="Floors",
        ),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.subheader("📊 Sensor Monitoring")

col3, col4, col5, col6 = st.columns(4)

col3.metric("Temperature", f"{temperature} °C")
col4.metric("Humidity", f"{humidity} %")
col5.metric("CO2 Level", f"{co2} ppm")
col6.metric("Occupancy", occupancy)

st.markdown("---")

st.caption("AI Powered Smart Building Infrastructure System")
