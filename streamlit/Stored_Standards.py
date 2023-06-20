import pandas as pd
import json
import streamlit as st
from streamlit_js_eval import streamlit_js_eval




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
bradford_volumes_list = list(stored_calibration_df["Bradford_Volume_ul"].unique())
sample_volumes_list = list(stored_calibration_df["Sample_Volume_ul"].unique())



st.sidebar.subheader("Filter Calibration Data:")

plate_reader_selected = st.sidebar.selectbox(
    "Select Plate Reader",
    instruments_in_calibration
    )

bradford_volume_selected = st.sidebar.selectbox(
    "Bradford  Well Volume (ul)",
    bradford_volumes_list
    )

sample_volume_selected = st.sidebar.selectbox(
    "Sample  Well Volume (ul)",
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
        value = 3,
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
    


st.title("Ciao")
st.write("intro")

st.subheader("Filtered Calibration Dataset:")

# reimport stored calibration data
calibration_df = read_dataframe("/src/streamlit/datasets/calibration.csv")

# filter based on side bar

# first the instrument
calibration_df = calibration_df[calibration_df["Instrument"] == plate_reader_selected]

# next the bradford volume
calibration_df = calibration_df[calibration_df["Bradford_Volume_ul"] == bradford_volume_selected]

# next the sample volume
calibration_df = calibration_df[calibration_df["Sample_Volume_ul"] == sample_volume_selected]

# next the sample volume
calibration_df = calibration_df[calibration_df["Sample_Volume_ul"] == sample_volume_selected]

# calibration range

## store the 0 ug/ml
blank_wells = calibration_df[calibration_df["Sample_Concentration_ug/ml"] == 0]
## filter
calibration_df = calibration_df[calibration_df["Sample_Concentration_ug/ml"] >= calibration_range_ug_ml_selected[0]]
calibration_df =  calibration_df[calibration_df["Sample_Concentration_ug/ml"] <= calibration_range_ug_ml_selected[1]]
## reinsert 0 ug/ml
if not calibration_range_ug_ml_selected[0] == 0:
    calibration_df = pd.concat([blank_wells, calibration_df], ignore_index=True)


st.write(calibration_df)


##################################################################

st.subheader("Model:")

st.metric("Type:", st.session_state["Model_Type"])

if st.session_state["Model_Type"] == "Polynomial":
    st.metric("Features:", poly_features_selected)



# pre process
for conc in calibration_df["Sample_Concentration_ug/ml"].unique():
    conc_slice = calibration_df[calibration_df["Sample_Concentration_ug/ml"] == conc]
    print(conc_slice)
st.write(calibration_df)


"""

# calibrant concs
calibrant_range_numerical = [float(ele) for ele in calibrant_range]
print(calibrant_range_numerical)



# fitc data in to array and reverse the order
x = np.array(calibrants_df_avg["Mean"]).reshape(-1,1)

# List of nM concs into array
y = np.array(calibrant_range_numerical).reshape(-1,1)


plt.scatter(x,y)


#x = x.reshape(-1,1)

# fit curves
#function for looping?

poly = PolynomialFeatures(degree=3, include_bias=False)

poly_features = poly.fit_transform(x)

model = LinearRegression()


# Fit
model.fit(poly_features,y)


print(model.intercept_, model.coef_)


y_predicted = model.predict(poly_features)
plt.plot(x, y_predicted, color='purple')

r_sq = model.score(poly_features, y)
print('coefficient of determination:', r_sq)


textstr ='r²: ' +str(round(r_sq,2))
plt.text(calibrants_df_avg["Mean"].min(), calibrant_range_numerical[-1], textstr, color='r', fontsize=10)

plt.title('Standard Curve')
plt.xlabel('Arbitrary Absorbance Units')
plt.ylabel('BSA μg/Ml')
plt.savefig("output/BSA_Standard_Curve.png")
plt.show()
"""