import pandas as pd
import numpy as np
import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from scipy import stats


from utils.models import linear_model, linear_polynomial_model, wrangle_calibration_data
from static.home_static import *


st.set_page_config(
    page_title="SBSG Standards Database",
    page_icon="🧮",
    #layout="wide",
    #initial_sidebar_state="expanded",
    menu_items={
        'About': "This app was built by Alex Perkins: https://www.github.com/aperkins19"
    }
)

    
st.title("Calibration Database 🚀")

blurb_expander = st.expander("About:", expanded=True)
Intro_text(blurb_expander)

