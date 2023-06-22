import pandas as pd


raw = pd.read_csv("calibration.csv")


print(raw)

sahan = pd.read_csv("sahan_cal.csv")

sahan = pd.melt(
        sahan,
        id_vars="Exp. Conc.",
        value_vars=["Abs 1",  "Abs 2",  "Abs 3",  "Abs 4"],
        var_name=None,
        value_name='Absorbance'
        )

sahan.rename({"Exp. Conc.": "Sample_Concentration_ug/ml"}, axis=1, inplace=True)
sahan["Sample_Concentration_ug/ml"] = sahan["Sample_Concentration_ug/ml"] *1000
sahan["Sample_Concentration_ug/ml"] = sahan["Sample_Concentration_ug/ml"].astype(int)
sahan["Maker"] = "Sahan Liyanagedera"
sahan["Bradford_Volume_µl"] = 250
sahan["Sample_Volume_µl"] = 5
sahan["Instrument"] = "BiotekH1"
sahan["Measurement"] = "Bradford:595"

sahan = sahan.sort_values(by=["Sample_Concentration_ug/ml"], ascending=False)

sahan = sahan.drop("variable", axis=1)
print(sahan.columns)

sahan = sahan.reset_index(drop=True)


raw = pd.concat([raw, sahan])
raw = raw.reset_index(drop=True)

print(raw)


#raw = raw.rename(columns={'Bradford_Volume_ul': 'Bradford_Volume_µl', 'Sample_Volume_ul': 'Sample_Volume_µl'})
#print(raw)
#raw = raw.drop("Unnamed: 0", axis = 1)

raw.to_csv("calibration.csv", index=None)

