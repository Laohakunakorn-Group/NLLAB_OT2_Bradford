import pandas as pd


raw = pd.read_csv("calibration.csv")

print(raw)

#raw = raw.rename(columns={'Bradford_Volume_ul': 'Bradford_Volume_µl', 'Sample_Volume_ul': 'Sample_Volume_µl'})
#print(raw)
#raw = raw.drop("Unnamed: 0", axis = 1)

raw.to_csv("calibration.csv", index=None)

