import pandas as pd
import numpy as np
import json
import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from utils.models import linear_model, linear_polynomial_model, wrangle_calibration_data
from scipy import stats



st.set_page_config(
    page_title="Bradford Assay",
    page_icon="🧮",
    #layout="wide",
    #initial_sidebar_state="expanded",
    menu_items={
        'About': "This app was built by Alex Perkins: https://www.github.com/aperkins19"
    }
)

if "data_submitted" not in st.session_state:
    st.session_state["data_submitted"] = False


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
    

st.sidebar.subheader("Prediction:")

st.session_state["Number_of_Dilutions"] = st.sidebar.number_input(
    label = "Number of Dilutions:",
    min_value = 1,
    value = 1,
    step = 1,
    help = ""
)

st.sidebar.write("Number of Technical Replicates for:")
for dilution in range(1, st.session_state["Number_of_Dilutions"]+1, 1):
    st.session_state["Dilution_"+str(dilution)] = dilution
    st.session_state["Dilution_"+str(dilution)+"_#techreps"] = st.sidebar.number_input(
                                                            label = "Dilution #"+str(dilution)+":",
                                                            min_value = 1,
                                                            value = 3,
                                                            step = 1,
                                                            help = ""
                                                            )






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



def data_input_callback():

    ## set session state for data_submitted
    st.session_state["data_submitted"] = True

    ###### Construct absorbance_data_dict

    absorbance_data_dict = {}

    for dilution_number in range(1, st.session_state["Number_of_Dilutions"]+1, 1):

        # list for storing the absorbances of tech reps - convert to array.
        # clear absorbance from session state
        absorbance_array = []
        for rep in range(1, st.session_state["Dilution_"+str(dilution_number)+"_#techreps"]+1,1):
            absorbance_array.append(st.session_state["dilution_number_" + str(dilution_number) + "_rep_"+str(rep)])
            del st.session_state["dilution_number_" + str(dilution_number) + "_rep_"+str(rep)]

        ## Add that record to the dict
        absorbance_data_dict[dilution_number] = {

            "Dilution_Factor" : st.session_state["dilution_number_" + str(dilution_number) + "_Dilution_Factor"],
            "Absorbance_Array" : np.array(absorbance_array)
        }

        ## Clear dilution factor from session state
        del st.session_state["dilution_number_" + str(dilution_number) + "_Dilution_Factor"]

    # add to session state
    st.session_state["Absorbance_Data_Dict"] = absorbance_data_dict

    



## Data Input expander
data_input_expander = st.expander("Predict:", expanded=True)

Sample_Input_Form = data_input_expander.form(key='Sample_Input_Form')

Sample_Input_Form.subheader("Data Input:")
Sample_Input_Form.write("Enter Absorbance Values for your technical replicates. Adjust the number on the sidebar:")

# set up columns
cols = Sample_Input_Form.columns(st.session_state["Number_of_Dilutions"])


for dilution_column, dilution_number in zip(cols, range(1, st.session_state["Number_of_Dilutions"]+1, 1)):

    # column title
    dilution_column.subheader("Dilution #"+str(dilution_number)+":")

    ## divider
    dilution_column.divider()

    ## Dilution Factor
    dilution_column.number_input(
            label = "Dilution Factor:",
            min_value = 0.,
            value = 1.,
            step = 0.01,
            help = "Values must be two decimal places.",
            key = ("dilution_number_" + str(dilution_number) + "_Dilution_Factor")
        )
    
    ## divider
    dilution_column.divider()

    for rep in range(1, st.session_state["Dilution_"+str(dilution_number)+"_#techreps"]+1,1):

        dilution_column.number_input(
            label = "Replicate #" +str(rep)+":",
            min_value = 0.,
            value = 0.,
            step = 0.01,
            help = "Values must be two decimal places.",
            key = ("dilution_number_" + str(dilution_number) + "_rep_"+str(rep))
        )

Sample_Input_Form.form_submit_button("Submit", on_click = data_input_callback)


## Data Overview expander
if st.session_state["data_submitted"]:

    data_overview_expander = st.expander("Absorbance Data Overview:", expanded=True)

    data_overview_expander.subheader("Summary Stats:")

    ### Absorbance Metrics
    # set up columns
    cols = data_overview_expander.columns(st.session_state["Number_of_Dilutions"])

    for dilution_column, dilution_number in zip(cols, range(1, st.session_state["Number_of_Dilutions"]+1, 1)):


        dilution_column.caption("Dilution #"+str(dilution_number)+":")

        #### Absorbance Metrics
        # Extract absorbance array
        absorbance_array = st.session_state["Absorbance_Data_Dict"][dilution_number]["Absorbance_Array"]

        # summary stats
        dilution_column.metric("Mean of Absorbances:", round(np.mean(absorbance_array, axis=0),2))

        # store mean
        st.session_state["Absorbance_Data_Dict"][dilution_number]["Mean"] = round(np.mean(absorbance_array, axis=0),2)

        # if tech reps less than 3 than can't do Standard Error
        if st.session_state["Dilution_"+str(dilution_number)+"_#techreps"] < 3:

            dilution_column.metric("Too few Reps to calculate Standard Error:", None)
            #  store sem
            st.session_state["Absorbance_Data_Dict"][dilution_number]["SEM"] = None
        else:
            dilution_column.metric("Standard Error of the Mean:", round(stats.sem(absorbance_array),2))
            #  store sem
            st.session_state["Absorbance_Data_Dict"][dilution_number]["SEM"] = round(stats.sem(absorbance_array),2)

    data_overview_expander.subheader("Summary Plots:")


    def generate_summary_plots(Absorbance_Data_Dict):

        import matplotlib.pyplot as plt
        import seaborn as sns

        data_overview_expander.divider()

        ## bar plot
        # generate the df
        Absorbance_Data_DF = pd.DataFrame.from_dict(Absorbance_Data_Dict).T
        # Creating a Matplotlib figure and axes
        fig1, ax1 = plt.subplots()

        # Creating a barplot using Seaborn
        sns.barplot(
            data = Absorbance_Data_DF,
            x = "Dilution_Factor",
            y = "Mean",
            ax = ax1,
            palette = "rocket"
            )

        # Setting labels and title
        ax1.set_xlabel('Dilution Factor')
        ax1.set_ylabel('Mean of Absorbances')
        ax1.set_title('Mean of absorbances for each Dilution Factor')

        data_overview_expander.pyplot(fig1)

        data_overview_expander.divider()

        ### heat map
        




    
    generate_summary_plots(st.session_state["Absorbance_Data_Dict"])