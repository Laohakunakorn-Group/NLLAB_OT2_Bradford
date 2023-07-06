import pandas as pd


raw = pd.read_csv("calibration.csv")



#print(raw)

new_curve = pd.read_csv("200_ugml_bradford_bsa_stnds.csv")

new_curve.rename({"Exp. Conc.": "Sample_Concentration_ug/ml"}, axis=1, inplace=True)

new_curve = pd.melt(
        new_curve,
        id_vars="Sample_Concentration_ug/ml",
        value_vars=["Abs 1", "Abs 2", "Abs 3"],
        var_name=None,
        value_name='Absorbance'
        )

new_curve = new_curve.drop("variable", axis=1)
new_curve["Maker"] = "Sahan Liyanagedera"
new_curve["Bradford_Volume_µl"] = 250
new_curve["Sample_Volume_µl"] = 5
new_curve["Instrument"] = "BiotekH1"
new_curve["Measurement"] = "Bradford:595"

new_curve = new_curve.sort_values(by=["Sample_Concentration_ug/ml"], ascending=False)
new_curve = new_curve.reset_index(drop=True)


new_curve = new_curve[new_curve["Sample_Concentration_ug/ml"]!=12.5]

new_curve["Sample_Concentration_ug/ml"] = new_curve["Sample_Concentration_ug/ml"].astype("int")
print(type(new_curve.loc[0,"Sample_Concentration_ug/ml"]))
print(type(raw.loc[0,"Sample_Concentration_ug/ml"]))


raw = pd.concat([raw, new_curve])
raw = raw.reset_index(drop=True)


raw = raw.sort_values(by=["Bradford_Volume_µl","Sample_Concentration_ug/ml"], ascending=False)
raw = raw.reset_index(drop=True)
print(raw)


raw.to_csv("calibration.csv", index=None)
