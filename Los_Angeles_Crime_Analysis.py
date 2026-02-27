import pandas as pd

df = pd.read_csv("LA_Crime_Data.csv")
print(df.shape)
print(df.head())
print(df.duplicated().sum())  # No Duplicates
print(df.isnull().sum())

## Dropping unnecessary columns
df = df.drop("DR_NO", axis=1)
df = df.drop("Part 1-2", axis=1)
df = df.drop("Mocodes", axis=1)
df = df.drop("Crm Cd 1", axis=1)
df = df.drop("Crm Cd 2", axis=1)
df = df.drop("Crm Cd 3", axis=1)
df = df.drop("Crm Cd 4", axis=1)
df = df.drop("Cross Street", axis=1)
print(df.head())

## checking for data types
print(df.dtypes)
df["Date Rptd"] = pd.to_datetime(df["Date Rptd"]).dt.date
df["DATE OCC"] = pd.to_datetime(df["DATE OCC"]).dt.date
df["TIME OCC 12hr"] = pd.to_datetime(
    df["TIME OCC"].astype(str).str.zfill(4), format="%H%M"
).dt.strftime("%I:%M %p")
df["Premis Cd"] = df["Premis Cd"].astype("Int64")
df["Weapon Used Cd"] = df["Weapon Used Cd"].astype("Int64")
print(df.dtypes)

## Filling Null VAlues
df["Vict Descent"] = df["Vict Descent"].fillna("Not Recorded")
df["Weapon Desc"] = df["Weapon Desc"].fillna("Not Recorded")
# premis code and desc have very less missing vlaues; will drop them
df = df.dropna(subset=["Premis Cd", "Premis Desc"])
print(df.isnull().sum())

##Feature Engineering
# print(df["Vict Descent"].unique())
# creating column for adding victim descent description
# Map codes to descriptive text
victim_descent_map = {
    "A": "Other Asian",
    "B": "Black",
    "C": "Chinese",
    "D": "Cambodian",
    "F": "Filipino",
    "G": "Guamanian",
    "H": "Hispanic/Latino",
    "I": "American Indian/Alaska Native",
    "J": "Japanese",
    "K": "Korean",
    "L": "Laotian",
    "O": "Other",
    "P": "Pacific Islander",
    "S": "Samoan",
    "U": "Hawaiian",
    "V": "Vietnamese",
    "W": "White",
    "X": "Unknown",
    "Z": "Other/Unknown",
    "-": "Not Recorded",
    "Not Recorded": "Not Recorded",
}
df["Vict Descent Description"] = df["Vict Descent"].map(victim_descent_map)
df["Vict Descent Description"] = df["Vict Descent Description"].astype(object)
df[["Vict Descent", "Vict Descent Description"]].head(10)

# extract month and year in seperate columns; from the column data incident occured
df["Month Occurred"] = pd.to_datetime(df["DATE OCC"]).dt.month
df["Year Occurred"] = pd.to_datetime(df["DATE OCC"]).dt.year
df["Hour Occurred"] = pd.to_datetime(df["DATE OCC"]).dt.hour
print(df.head())
