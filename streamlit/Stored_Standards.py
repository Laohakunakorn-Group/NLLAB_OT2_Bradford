import pandas as pd
import numpy as np
import json
import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from utils.models import linear_model, linear_polynomial_model, wrangle_calibration_data


if "Standard Curve DF cached" not in st.session_state:
    st.session_state["Standard Curve DF cached"] = False

if "Standard Curve" not in st.session_state:
    st.session_state["Standard Curve"] = False



@st.cache_data
def read_dataframe(path):
    df = pd.read_csv(path)
    return df


@st.cache_data
def cache_dataframe(imported_file):
    df = pd.DataFrame(imported_file)
    return df



# import stored calibration data
stored_calibration_df = read_dataframe("/src/streamlit/datasets/calibration.csv")

instruments_in_calibration = list(stored_calibration_df["Instrument"].unique())
calibration_range_ug_ml_list = list(stored_calibration_df["Sample_Concentration_ug/ml"].unique())
bradford_volumes_list = list(stored_calibration_df["Bradford_Volume_µl"].unique())
sample_volumes_list = list(stored_calibration_df["Sample_Volume_µl"].unique())



st.sidebar.subheader("Filter Calibration Data:")

plate_reader_selected = st.sidebar.selectbox(
    "Select Plate Reader",
    instruments_in_calibration
    )

bradford_volume_selected = st.sidebar.selectbox(
    "Bradford  Well Volume (µl)",
    bradford_volumes_list
    )

sample_volume_selected = st.sidebar.selectbox(
    "Sample  Well Volume (µl)",
    sample_volumes_list
    )


calibration_range_ug_ml_selected = st.sidebar.select_slider(
    "Select Calibration Range:",
    options = calibration_range_ug_ml_list,
    value = [min(calibration_range_ug_ml_list), max(calibration_range_ug_ml_list)]
)

st.sidebar.subheader("Configure Model:")

st.session_state["Model_Type"] = st.sidebar.radio(
    "Which model:",
    ("Linear", "Polynomial", "Bayesian_Linear"))

if st.session_state["Model_Type"] == "Polynomial":
    poly_features_selected = st.sidebar.number_input(
        label = 'Number of Features in the Polynomial Model:',
        min_value = 2,
        value = 2,
        step = 1,
        help = "dfg")






# reset button
if st.sidebar.button("Reset"):

    # cached dataframes
    cache_dataframe.clear()
    read_dataframe.clear()

    # session state
    for key in st.session_state.keys():
        del st.session_state[key]

    # reload the webpage (and hereby re initialising the session states)
    streamlit_js_eval(js_expressions="parent.window.location.reload()")
    


st.title("Calibration Database 🚀")

blurb_expander = st.expander("About:", expanded=False)
blurb_expander.markdown("## Intro")
blurb_expander.markdown("Choose the calibration data appropriate to your method, configure a suitable model, upload your raw sample data and get predictions for your sample concentrations.")
blurb_expander.markdown("## Usage")

blurb_expander.markdown("### 1. Filter the data using the side bar to match your method.")
blurb_expander.markdown("This database contains Bovine Serum Albumin Absorbance calibration data for a range of:")
blurb_expander.markdown("* Instruments")
blurb_expander.markdown("* Total Volumes (i.e. path lengths)")
blurb_expander.markdown("* Concentrations")


blurb_expander.markdown("#### Path-Length")
blurb_expander.markdown("The **Path-Length** of your sample must be the same as the calibrant data selected.")
blurb_expander.markdown("**Path-Length** = **Bradford Well Volume (µl)** + **Sample Well Volume (µl)**")
blurb_expander.markdown("**Bradford Well Volume (µl)** is the volume of Bradford Reagent that has been added to a 360 µL well of a 96 well, flat-bottomed, black Nunc plate.")
blurb_expander.markdown("**Sample Well Volume (µl)** is the volume of your *diluted sample* that has been added to a 360 µL well of a 96 well, flat-bottomed, black Nunc plate.")

blurb_expander.markdown("#### Concentration Range")
blurb_expander.markdown("The range of the slider is generated according the data available meeting the criteria selected. i.e. The server first filters the data by Instrument, then Bradford Volume, then Sample Volume, finally generating the slider according the remaining data.")
blurb_expander.markdown("You can adjust the range of the data to better straddle the raw absorbances of your samples. If you decide you want to discard the lower concentrations, the blank data points will be preserved.")
blurb_expander.markdown("The resulting dataset can reviewed under the *Filtered Calibration Dataset* Tab.")

blurb_expander.markdown("### 2. Build a Model.")
blurb_expander.markdown("Once you have filtered your data to your heart's content, you can build a model by selecting a model type in the side bar.")
blurb_expander.markdown("Implemented models:")
blurb_expander.markdown("* Linear Regression")
blurb_expander.markdown("* Polynomial Linear Regression")
blurb_expander.markdown("* Bayesian Linear Regression")

blurb_expander.markdown("Depending on the model type you select, additional parameters may become available. Be sure to check these carefully.")
blurb_expander.markdown("A plot or series of plots will automatically be generated from the model parameters and data you have selected. If you wish, save these like any other image by Right-Clicking your mouse and selecting *save image as:*")

st.subheader("Filtered Calibration Dataset:")

filtered_calibration_dataset_expander = st.expander("Filtered Calibration Dataset:", expanded=False)

# reimport stored calibration data
calibration_df = read_dataframe("/src/streamlit/datasets/calibration.csv")

# filter based on side bar

# first the instrument
calibration_df = calibration_df[calibration_df["Instrument"] == plate_reader_selected]

# next the bradford volume
calibration_df = calibration_df[calibration_df["Bradford_Volume_µl"] == bradford_volume_selected]

# next the sample volume
calibration_df = calibration_df[calibration_df["Sample_Volume_µl"] == sample_volume_selected]

# next the sample volume
calibration_df = calibration_df[calibration_df["Sample_Volume_µl"] == sample_volume_selected]

# calibration range

## store the 0 ug/ml
blank_wells = calibration_df[calibration_df["Sample_Concentration_ug/ml"] == 0]
## filter
calibration_df = calibration_df[calibration_df["Sample_Concentration_ug/ml"] >= calibration_range_ug_ml_selected[0]]
calibration_df =  calibration_df[calibration_df["Sample_Concentration_ug/ml"] <= calibration_range_ug_ml_selected[1]]
## reinsert 0 ug/ml
if not calibration_range_ug_ml_selected[0] == 0:
    calibration_df = pd.concat([blank_wells, calibration_df], ignore_index=True)


filtered_calibration_dataset_expander.write(calibration_df)


##################################################################

## Model expander

model_expander = st.expander("Model:", expanded=True)

# preprocess data
summary_df = wrangle_calibration_data(calibration_df)

if st.session_state["Model_Type"] == "Linear":
    # generate model
    model, fig, metric = linear_model(summary_df)
    # Displaying the resµlts
    model_expander.pyplot(fig)
    # metrics
    col1, col2 = model_expander.columns(2)
    col1.metric("Type:", st.session_state["Model_Type"])
    col2.metric("R Squared:", metric)

elif st.session_state["Model_Type"] == "Polynomial":
    # generate model
    model, fig, metric = linear_polynomial_model(summary_df, poly_features_selected)
    # Displaying the resµlts
    model_expander.pyplot(fig)
    # metrics
    col1, col2, col3 = model_expander.columns(3)
    col1.metric("Type:", st.session_state["Model_Type"])
    col2.metric("R Squared:", metric)
    col3.metric("Features:", poly_features_selected)


## Prediction expander
prediction_expander = st.expander("Predict:", expanded=True)