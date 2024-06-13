import streamlit as st


def Intro_text(blurb_expander):

    blurb_expander.markdown("## Welcome!")

    blurb_expander.markdown("Welcome to our interactive lab dashboard! This platform centralises all our standard curves and calibration data, streamlining how you access, contribute to and retrieve the specific data you need to calibrate your experiments.")

    blurb_expander.markdown("Collaborative Contributions: Please play an active role in enriching our database by uploading new measurements directly through the dashboard. Your input helps us build the hive mind and makes us more efficient and collaborative. If you have a great standard curve - upload it so others can use it.")

    blurb_expander.markdown("In-House Modelling Tools: Leverage built-in tools to fit models to the calibration data that you select. These tools are designed for simplicity, allowing you to accurately calibrate raw measurements without extensive statistical background or python/excel.")

    blurb_expander.markdown("Effortless Export Options: If you wish you can also download calibrant data in multiple formats to conduct your own modelling or export graphics directly from the dashboard.")

    blurb_expander.markdown("Authors Note: I hope you find this system useful. Let me know if you have feedback or any ideas for features.")
    blurb_expander.markdown("Alex Perkins - June 2024")
