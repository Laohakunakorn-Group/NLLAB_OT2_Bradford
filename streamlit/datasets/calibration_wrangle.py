import pandas as pd


raw = pd.read_csv("calibration.csv")


#print(raw)

new_curve = pd.read_csv("new_calibration_curve_biotek_310ul.csv", header=None)

print(new_curve)


new_curve = pd.melt(
        new_curve,
        id_vars=0,
        value_vars=[1,  2,  3,  4, 5],
        var_name=None,
        value_name='Absorbance'
        )

new_curve = new_curve.drop("variable", axis=1)
new_curve.rename({0: "Sample_Concentration_ug/ml"}, axis=1, inplace=True)

new_curve["Sample_Concentration_ug/ml"] = new_curve["Sample_Concentration_ug/ml"].astype(int)
new_curve["Maker"] = "Alex Perkins"
new_curve["Bradford_Volume_µl"] = 300
new_curve["Sample_Volume_µl"] = 10
new_curve["Instrument"] = "BiotekH1"
new_curve["Measurement"] = "Bradford:595"

new_curve = new_curve.sort_values(by=["Sample_Concentration_ug/ml"], ascending=False)
new_curve = new_curve.reset_index(drop=True)


raw = pd.concat([raw, new_curve])
raw = raw.reset_index(drop=True)

print(raw)


raw.to_csv("calibration.csv", index=None)
