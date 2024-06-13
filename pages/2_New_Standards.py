import numpy as np

import json
import plotly.io as pio 

import streamlit as st



st.title("frequentist")



st.sidebar.subheader("Defining a Classical Orbit")

ecc_val = st.sidebar.slider(
    "Eccentricity",
    min_value = float(0),
    max_value = float(1),
    value = float(0),
    step=0.01,
    on_change = None,
    format=None,
    disabled=False,
)

inc_val = st.sidebar.slider(
    "Inclination °",
    min_value = int(0),
    max_value = int(90),
    value = int(0),
    step=1,
    on_change = None,
    format=None,
    disabled=False,
)

raan_val = st.sidebar.slider(
    "Right ascension of the ascending node°",
    min_value = int(0),
    max_value = int(360),
    value = int(0),
    step=1,
    on_change = None,
    format=None,
    disabled=False,
)

argp_val = st.sidebar.slider(
    "Argument of perigee°",
    min_value = int(0),
    max_value = int(360),
    value = int(0),
    step=1,
    on_change = None,
    format=None,
    disabled=False,
)

nu_val = st.sidebar.slider(
    "True Anomaly°",
    min_value = int(0),
    max_value = int(360),
    value = int(0),
    step=1,
    on_change = None,
    format=None,
    disabled=False,
)


