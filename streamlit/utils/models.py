import pandas as pd
import numpy as np
import streamlit as st


def wrangle_calibration_data(calibration_df):
    
    # pre process
    # initialise summary stats df
    summary_df = pd.DataFrame(
        columns = [
            "Sample_Concentration_ug/ml",
            "Mean",
            "SEM",
            "Number_of_Records"
            ]
            )

    # iterate over the columns, slice to get just records for each conc
    # produce new_record df containing summary stats and concat into summary_df
    for i, conc in enumerate(calibration_df["Sample_Concentration_ug/ml"].unique()):
        conc_slice = calibration_df[calibration_df["Sample_Concentration_ug/ml"] == conc]
        new_record = pd.DataFrame.from_dict(
                                            {
                                                    i:  [
                                                        conc,
                                                        conc_slice["Absorbance"].mean(),
                                                        conc_slice["Absorbance"].sem(),
                                                        conc_slice["Absorbance"].shape[0]
                                                        ]
                                            },
                                            orient="index",
                                            columns=[
                                                    "Sample_Concentration_ug/ml",
                                                    "Mean",
                                                    "SEM",
                                                    "Number_of_Records"
                                                    ]
                                            )
        summary_df = pd.concat([summary_df, new_record])

    return summary_df


def linear_model(summary_df):

    from sklearn.linear_model import LinearRegression
    import matplotlib.pyplot as plt
    import seaborn as sns

    ## set up vectors
    x = np.array(summary_df["Mean"]).reshape(-1,1)
    y = np.array(summary_df["Sample_Concentration_ug/ml"]).reshape(-1,1)

    model = LinearRegression()
    model.fit(x,y)

    # Calcµlate R2 score
    r2_score = round(model.score(x, y), 3)

    # Creating a Matplotlib figure and axes
    fig, ax = plt.subplots()

    # Creating a scatterplot using Seaborn
    sns.scatterplot(
        x = np.array(summary_df["Mean"]),
        y = np.array(summary_df["Sample_Concentration_ug/ml"]),
        ax = ax,
        label = "Data",
        color="blue"
        )
    
    # line of best fit
    x_line = np.array([summary_df["Mean"].min(), summary_df["Mean"].max()])
    y_line = np.squeeze(model.predict(x_line.reshape(-1, 1)))
    sns.lineplot(x = x_line, y = y_line, ax = ax, label = "Regression Line", color="red")

    # Setting labels and title
    ax.set_xlabel('Mean of Absorbances')
    ax.set_ylabel('Sample_Concentration_ug/ml')
    ax.set_title('Linear Model of Bradford Assay BSA Concentration vs Absorbance')

    ax.text((summary_df["Mean"].max()*0.99), 0.1, "r²: "+str(r2_score), fontsize=12, ha='right', va='bottom', color="red")


    return model, fig, r2_score



def linear_polynomial_model(summary_df, poly_features_selected):

    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import PolynomialFeatures
    import matplotlib.pyplot as plt
    import seaborn as sns


    ## set up vectors
    x = np.array(summary_df["Mean"]).reshape(-1,1)
    y = np.array(summary_df["Sample_Concentration_ug/ml"]).reshape(-1,1)

    # Transform for polynomial features
    poly = PolynomialFeatures(degree=poly_features_selected, include_bias=False)
    poly_features = poly.fit_transform(x)

    # fit
    model = LinearRegression()
    model.fit(poly_features,y)

    # Calcµlate R2 score
    r2_score = round(model.score(poly_features, y), 3)

    # Creating a Matplotlib figure and axes
    fig, ax = plt.subplots()

    # Creating a scatterplot using Seaborn
    sns.scatterplot(
        x = np.array(summary_df["Mean"]),
        y = np.array(summary_df["Sample_Concentration_ug/ml"]),
        ax = ax,
        label = "Data",
        color="blue"
        )
    
    # line of best fit
    X_ = np.arange(
            summary_df["Mean"].min(),
            summary_df["Mean"].max(),
            0.01
            )
    x_line = poly.fit_transform(
        X_.reshape(-1, 1)
            )
    y_line = np.squeeze(model.predict(x_line))
    sns.lineplot(x = X_, y = y_line, ax = ax, label = "Regression Line", color="red")

    # Setting labels and title
    ax.set_xlabel('Mean of Absorbances')
    ax.set_ylabel('Sample_Concentration_ug/ml')
    ax.set_title('Polynomial Linear Model of Bradford Assay BSA Concentration vs Absorbance')

    ax.text((summary_df["Mean"].max()*0.99), 0.1, "r²: "+str(r2_score), fontsize=12, ha='right', va='bottom', color="red")

    return model, fig, r2_score
