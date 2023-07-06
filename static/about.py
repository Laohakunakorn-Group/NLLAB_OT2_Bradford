import streamlit as st


def ABOUT_text(blurb_expander):


    

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
