import numpy as np
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
import streamlit as st
import plotly.graph_objects as go
import time

# Streamlit app title
st.title("Sensor Data Dashboard")

# Function to generate new sensor values
def generate_sensor_values():
    return (
        np.random.uniform(20, 30),
        np.random.uniform(5, 15),
        np.random.uniform(100, 500),
        np.random.uniform(0.1, 1.0),
    )

# Initialize session state for real-time updates
if 'temperatures' not in st.session_state:
    st.session_state.temperatures = []
    st.session_state.viscosities = []
    st.session_state.resistivities = []
    st.session_state.vibrations = []
    st.session_state.times = []

placeholder = st.empty()

while True:
    new_temp, new_visc, new_resist, new_vib = generate_sensor_values()
    st.session_state.temperatures.append(new_temp)
    st.session_state.viscosities.append(new_visc)
    st.session_state.resistivities.append(new_resist)
    st.session_state.vibrations.append(new_vib)
    st.session_state.times.append(datetime.datetime.now())

    # Keep only the last 24 points
    if len(st.session_state.times) > 24:
        st.session_state.temperatures.pop(0)
        st.session_state.viscosities.pop(0)
        st.session_state.resistivities.pop(0)
        st.session_state.vibrations.pop(0)
        st.session_state.times.pop(0)

    with placeholder.container():
        # Define layout structure
        st.markdown("---")

        # Gauge Meters in a Row
        st.subheader("Gauge Meters")
        col_g1, col_g2, col_g3, col_g4 = st.columns(4)

        gauge_values = [new_temp, new_visc, new_resist, new_vib]
        gauge_titles = ["Temperature (°C)", "Viscosity (cP)", "Resistivity (Ω·m)", "Vibration (g)"]
        gauge_ranges = [[20, 30], [5, 15], [100, 500], [0.1, 1.0]]

        gauge_cols = [col_g1, col_g2, col_g3, col_g4]
        for col, value, title, rng in zip(gauge_cols, gauge_values, gauge_titles, gauge_ranges):
            with col:
                fig_gauge = go.Figure()
                fig_gauge.add_trace(go.Indicator(
                    mode="gauge+number",
                    value=value,
                    title={'text': title},
                    gauge={'axis': {'range': rng}}
                ))
                st.plotly_chart(fig_gauge)

        # Sensor Readings Below Gauges
        st.subheader("Real-time Sensor Values")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Temperature (°C)", f"{new_temp:.2f}°C")
        with col2:
            st.metric("Viscosity (cP)", f"{new_visc:.2f} cP")
        with col3:
            st.metric("Resistivity (Ω·m)", f"{new_resist:.2f} Ω·m")
        with col4:
            st.metric("Vibration (g)", f"{new_vib:.2f} g")

        # Graphs Section
        st.subheader("Sensor Data Over Time")
        fig, ax = plt.subplots(4, 1, figsize=(10, 12), sharex=True)

        # Temperature plot
        ax[0].plot(st.session_state.times, st.session_state.temperatures, marker='o', linestyle='-', color='b', label='Temperature (°C)')
        ax[0].set_ylabel('Temperature (°C)')
        ax[0].legend()
        ax[0].grid()

        # Viscosity plot
        ax[1].plot(st.session_state.times, st.session_state.viscosities, marker='s', linestyle='-', color='r', label='Viscosity (cP)')
        ax[1].set_ylabel('Viscosity (cP)')
        ax[1].legend()
        ax[1].grid()

        # Resistivity plot
        ax[2].plot(st.session_state.times, st.session_state.resistivities, marker='^', linestyle='-', color='g', label='Resistivity (Ω·m)')
        ax[2].set_ylabel('Resistivity (Ω·m)')
        ax[2].legend()
        ax[2].grid()

        # Vibration plot
        ax[3].plot(st.session_state.times, st.session_state.vibrations, marker='d', linestyle='-', color='m', label='Vibration (g)')
        ax[3].set_ylabel('Vibration (g)')
        ax[3].set_xlabel('Time')
        ax[3].legend()
        ax[3].grid()

        # Formatting the time axis
        ax[3].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax[3].xaxis.set_major_locator(mdates.HourLocator(interval=2))
        plt.xticks(rotation=45)

        # Display the plot in Streamlit
        st.pyplot(fig)

        st.markdown("---")
    
    time.sleep(2)
