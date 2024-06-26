import pandas as pd
import numpy as np
import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from scipy import stats


from utils.models import linear_model, linear_polynomial_model, wrangle_calibration_data
from static.bradford_static import *


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
stored_calibration_df = read_dataframe("/src/datasets/calibration.csv")

# initial
st.session_state["instruments_in_calibration"] = list(stored_calibration_df["Instrument"].unique())
st.session_state["calibration_range_ug_ml_list"] = sorted(list(stored_calibration_df["Sample_Concentration_ug/ml"].unique()))
st.session_state["bradford_volumes_list"] = list(stored_calibration_df["Bradford_Volume_µl"].unique())
st.session_state["sample_volumes_list"] = list(stored_calibration_df["Sample_Volume_µl"].unique())

def filter_callback():
    st.session_state["instruments_in_calibration"] = list(calibration_df["Instrument"].unique())
    st.session_state["calibration_range_ug_ml_list"] = sorted(list(calibration_df["Sample_Concentration_ug/ml"].unique()))
    st.session_state["bradford_volumes_list"] = list(calibration_df["Bradford_Volume_µl"].unique())
    st.session_state["sample_volumes_list"] = list(calibration_df["Sample_Volume_µl"].unique())


st.sidebar.subheader("Filter Calibration Data:")

plate_reader_selected = st.sidebar.selectbox(
    "Select Plate Reader",
    st.session_state["instruments_in_calibration"],
    on_change=filter_callback
    )

bradford_volume_selected = st.sidebar.selectbox(
    "Bradford  Well Volume (µl)",
    st.session_state["bradford_volumes_list"],
    on_change=filter_callback
    )

sample_volume_selected = st.sidebar.selectbox(
    "Sample  Well Volume (µl)",
    st.session_state["sample_volumes_list"],
    on_change=filter_callback
    )


calibration_range_ug_ml_selected = st.sidebar.select_slider(
    "Select Calibration Range:",
    options = st.session_state["calibration_range_ug_ml_list"],
    value = [min(st.session_state["calibration_range_ug_ml_list"]), max(st.session_state["calibration_range_ug_ml_list"])]
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
    
st.title("Bradford Assay")

blurb_expander = st.expander("About:", expanded=False)
ABOUT_BRADFORD_text(blurb_expander)

st.subheader("Filtered Calibration Dataset:")

filtered_calibration_dataset_expander = st.expander("Filtered Calibration Dataset:", expanded=False)

# reimport stored calibration data
calibration_df = read_dataframe("/src/datasets/calibration.csv")

# filter based on side bar

# first the instrument
calibration_df = calibration_df[calibration_df["Instrument"] == plate_reader_selected]

# next the bradford volume
calibration_df = calibration_df[calibration_df["Bradford_Volume_µl"] == bradford_volume_selected]

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

# sort
calibration_df = calibration_df.sort_values(by="Sample_Concentration_ug/ml", ascending=False)


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

dilution_rows = st.session_state["Number_of_Dilutions"]

for dilution_number in range(1, dilution_rows+1,1):

    Sample_Input_Form.divider()

    Sample_Input_Form.subheader("Dilution #" +str(dilution_number)+":")

    # set up columns
    replicates_cols = Sample_Input_Form.columns(st.session_state["Dilution_"+str(dilution_number)+"_#techreps"]+1) # +1 for dilution factor

    for rep_column, rep_number in zip(replicates_cols,range(0, st.session_state["Dilution_"+str(dilution_number)+"_#techreps"]+1,1)):

        # check if first, if so then dilution factor
        if rep_number == 0:
            # Dilution Factor
            rep_column.number_input(
            label = "Dilution Factor:",
            min_value = 0.,
            value = 1.,
            step = 0.001,
            help = "",
            key = ("dilution_number_" + str(dilution_number) + "_Dilution_Factor")
            )

        else:
            rep_column.number_input(
                label = "Replicate #" +str(rep_number)+":",
                min_value = 0.,
                value = 0.,
                step = 0.001,
                help = "Values rounded to 3 decimal places.",
                key = ("dilution_number_" + str(dilution_number) + "_rep_"+str(rep_number))
                )

Sample_Input_Form.divider()
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
        st.session_state["Absorbance_Data_Dict"][dilution_number]["Mean Abs"] = round(np.mean(absorbance_array, axis=0),2)

        # if tech reps less than 3 than can't do Standard Error
        if st.session_state["Dilution_"+str(dilution_number)+"_#techreps"] < 3:

            dilution_column.metric("Too few Reps to calculate Standard Error:", None)
            #  store sem
            st.session_state["Absorbance_Data_Dict"][dilution_number]["SEM Abs"] = None
        else:
            dilution_column.metric("Standard Error of the Mean:", round(stats.sem(absorbance_array),2))
            #  store sem
            st.session_state["Absorbance_Data_Dict"][dilution_number]["SEM Abs"] = round(stats.sem(absorbance_array),2)

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
            y = "Mean Abs",
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



    
    #generate_summary_plots(st.session_state["Absorbance_Data_Dict"])

    prediction_expander = st.expander("Predicted Concentrations:", expanded=True)

    def predict_concentrations(Absorbance_Data_Dict, model):

        for dilution_number, dilution_subdict in Absorbance_Data_Dict.items():
            
            # convert X for model type
            if st.session_state["Model_Type"] == "Linear":
                abs_arr = dilution_subdict["Absorbance_Array"].reshape(-1, 1)

            elif st.session_state["Model_Type"] == "Polynomial":

                from sklearn.preprocessing import PolynomialFeatures

                poly = PolynomialFeatures(degree=poly_features_selected, include_bias=False)
                abs_arr = poly.fit_transform(dilution_subdict["Absorbance_Array"].reshape(-1, 1))
            

            # generate predictions
            st.session_state["Absorbance_Data_Dict"][dilution_number]["Uncorrected_Prediction_Array"] = np.squeeze(model.predict(abs_arr))

            # Correct for dilution
            st.session_state["Absorbance_Data_Dict"][dilution_number]["Corrected_Prediction_Array"] = st.session_state["Absorbance_Data_Dict"][dilution_number]["Dilution_Factor"] * st.session_state["Absorbance_Data_Dict"][dilution_number]["Uncorrected_Prediction_Array"]

            # Generate Mean and SEM in mg/ml
            st.session_state["Absorbance_Data_Dict"][dilution_number]["Mean mg/ml"] = round(np.mean(st.session_state["Absorbance_Data_Dict"][dilution_number]["Corrected_Prediction_Array"])/1000, 2)
            st.session_state["Absorbance_Data_Dict"][dilution_number]["SEM mg/ml"] = round(stats.sem(st.session_state["Absorbance_Data_Dict"][dilution_number]["Corrected_Prediction_Array"])/1000, 2)
    
    def display_results(Absorbance_Data_Dict):

        # set up columns
        cols = prediction_expander.columns(len(Absorbance_Data_Dict))
        
        # display metrics
        for dilution_column, dilution_number  in zip(cols, Absorbance_Data_Dict):

            dilution_column.subheader("Dilution "+str(dilution_number)+":")
            dilution_column.metric("Mean (mg/ml)", st.session_state["Absorbance_Data_Dict"][dilution_number]["Mean mg/ml"])
            dilution_column.metric("SEM (mg/ml)", st.session_state["Absorbance_Data_Dict"][dilution_number]["SEM mg/ml"])

        # end section
        prediction_expander.divider()

        ######################################### plots

        # initialise the results df
        results_df = pd.DataFrame()
        
        for dilution_number, dict in Absorbance_Data_Dict.items():
            row = pd.DataFrame(
                pd.Series({
                    "Dilution Factor": dict["Dilution_Factor"],
                    "Mean mg/ml": dict["Mean mg/ml"],
                    "SEM mg/ml": dict["SEM mg/ml"]
                    })).T

            results_df = pd.concat([results_df, row], axis=0)


        # bar plot
        import matplotlib.pyplot as plt
        import seaborn as sns

        # Creating a Matplotlib figure and axes
        fig3, ax3 = plt.subplots()

        # Creating a barplot using Seaborn
        sns.barplot(
            data = results_df,
            x = "Dilution Factor",
            y = "Mean mg/ml",
#            yerr = "SEM mg/ml",
            ax = ax3,
            palette = "rocket"
            )

        # Setting labels and title
        ax3.set_xlabel('Dilution Factor')
        ax3.set_ylabel('Mean mg/ml')
        ax3.set_title('Predicted Protein')

        prediction_expander.pyplot(fig3)

        prediction_expander.divider()

    # call results fuctions
    predict_concentrations(st.session_state["Absorbance_Data_Dict"], model)
    display_results(st.session_state["Absorbance_Data_Dict"])  
