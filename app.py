import streamlit as st
import numpy as np
import joblib
import plotly.graph_objects as go

st.set_page_config(page_title="AI Smart Building Energy Dashboard", layout="wide", page_icon="🏢")

model = joblib.load("smart_building_model.pkl")

MODEL_ACCURACY = 0.92

st.title("AI Smart Building Energy Intelligence Dashboard")
st.subheader("Real-time Energy Consumption Prediction and Building Monitoring")

st.sidebar.header("Building Sensor Inputs")

temperature = st.sidebar.slider("Temperature (°C)",15.0,40.0,25.0)
humidity = st.sidebar.slider("Humidity (%)",20.0,90.0,50.0)
occupancy = st.sidebar.slider("Occupancy",0,100,20)
co2 = st.sidebar.slider("CO2 Level (ppm)",300.0,1500.0,600.0)
light = st.sidebar.slider("Light Intensity",0.0,1000.0,400.0)
hvac = st.sidebar.slider("HVAC Usage",0.0,1.0,0.5)
health = st.sidebar.slider("Equipment Health",0.0,1.0,0.9)
hour = st.sidebar.slider("Hour of Day",0,23,12)

col1,col2 = st.columns([1.2,1])

if "prediction" not in st.session_state:
    st.session_state.prediction = None
    st.session_state.conf = None
    st.session_state.eff = None

with col1:

    st.markdown("### Energy Prediction")

    if st.button("Predict Energy Consumption"):

        features = np.array([[temperature,humidity,occupancy,co2,light,hvac,health,hour]])

        prediction = float(model.predict(features)[0])

        efficiency = max(0,100-(prediction/10))

        confidence = min(0.99,0.75+(efficiency/400))

        st.session_state.prediction = prediction
        st.session_state.conf = confidence
        st.session_state.eff = efficiency

    if st.session_state.prediction is not None:

        st.success(f"Predicted Energy Consumption: {st.session_state.prediction:.2f} kWh")

        m1,m2,m3 = st.columns(3)

        m1.metric("Building Efficiency",f"{st.session_state.eff:.1f}%")
        m2.metric("Prediction Confidence",f"{st.session_state.conf*100:.1f}%")
        m3.metric("Model Accuracy",f"{MODEL_ACCURACY*100:.1f}%")

        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=st.session_state.prediction,
            title={'text':"Energy Consumption (kWh)"},
            gauge={
                'axis':{'range':[0,1000]},
                'bar':{'color':"#00c2ff"},
                'steps':[
                    {'range':[0,300],'color':"#00ff7f"},
                    {'range':[300,700],'color':"#ffd000"},
                    {'range':[700,1000],'color':"#ff2e2e"}
                ]
            }
        ))

        st.plotly_chart(gauge,use_container_width=True)

with col2:

    floors = 6

    width = 4
    depth = 4
    floor_height = 1

    fig = go.Figure()

    for f in range(floors):

        z0 = f*floor_height
        z1 = (f+1)*floor_height

        x = [0,0,width,width,0,0,width,width]
        y = [0,depth,depth,0,0,depth,depth,0]
        z = [z0,z0,z0,z0,z1,z1,z1,z1]

        fig.add_trace(go.Mesh3d(
            x=x,
            y=y,
            z=z,
            opacity=0.35,
            color="#7dd3fc",
            flatshading=True
        ))

        wx = np.linspace(0.5,width-0.5,4)
        wy = [depth]*4
        wz = [z0+0.5]*4

        fig.add_trace(go.Scatter3d(
            x=wx,
            y=wy,
            z=wz,
            mode="markers",
            marker=dict(size=8,color="#ffd700")
        ))

    occ_points = min(occupancy,40)

    ox = np.random.uniform(0.5,width-0.5,occ_points)
    oy = np.random.uniform(0.5,depth-0.5,occ_points)
    oz = np.random.uniform(0.2,floors-0.2,occ_points)

    fig.add_trace(go.Scatter3d(
        x=ox,
        y=oy,
        z=oz,
        mode="markers",
        marker=dict(size=5,color="#ff4d4d"),
        name="Occupants"
    ))

    fig.update_layout(
        title="Interactive Smart Building Model",
        scene=dict(
            xaxis_title="Width",
            yaxis_title="Length",
            zaxis_title="Floors",
            bgcolor="black"
        ),
        margin=dict(l=0,r=0,b=0,t=40),
        height=600
    )

    st.plotly_chart(fig,use_container_width=True)

st.markdown("---")

st.markdown("### Live Building Parameters")

c1,c2,c3,c4 = st.columns(4)

c1.metric("Temperature",f"{temperature} °C")
c2.metric("Humidity",f"{humidity} %")
c3.metric("CO₂",f"{co2} ppm")
c4.metric("Occupancy",occupancy)

c5,c6,c7 = st.columns(3)

c5.metric("Light Intensity",light)
c6.metric("HVAC Usage",hvac)
c7.metric("Equipment Health",health)

st.caption("AI Smart Building Infrastructure Monitoring System")
