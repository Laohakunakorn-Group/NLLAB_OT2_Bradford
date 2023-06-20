import pandas as pd


raw = pd.read_csv("calibration.csv")

print(raw)

#raw = raw.drop("Unnamed: 0", axis = 1)

raw.to_csv("calibration.csv", index=None)

