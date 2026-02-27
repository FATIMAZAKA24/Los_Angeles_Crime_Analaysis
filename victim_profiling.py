from LA_Crime_Cleaned_Data import clean_la_crime_data


import pandas as pd
import json

# Run the cleaning function on the CSV
df_clean = clean_la_crime_data("LA_Crime_Data.csv")


# Ensure datetime and age are clean
df_clean["Date Rptd"] = pd.to_datetime(df_clean["Date Rptd"], errors="coerce")
df_clean["DATE OCC"] = pd.to_datetime(df_clean["DATE OCC"], errors="coerce")
df_clean = df_clean.dropna(
    subset=["Date Rptd", "DATE OCC", "Vict Age", "AREA NAME", "Crm Cd Desc"]
)
df_clean["Reporting Delay (Days)"] = (
    df_clean["Date Rptd"] - df_clean["DATE OCC"]
).dt.days
df_clean = df_clean[df_clean["Reporting Delay (Days)"] >= 0]

# Define age bins
bins = [0, 12, 18, 25, 35, 50, 65, 100]
labels = ["Child", "Teen", "Young Adult", "Adult", "Middle-aged", "Senior", "Elderly"]
df_clean["Victim Age Group"] = pd.cut(
    df_clean["Vict Age"], bins=bins, labels=labels, right=False
)

# Extract hour in 24hr format
# df_clean["Hour Occurred"] = df_clean["DATE OCC"].dt.hour
# Ensure TIME OCC is zero-padded to 4 digits
df_clean["TIME OCC"] = df_clean["TIME OCC"].astype(str).str.zfill(4)
# Extract hour from TIME OCC
# Ensure TIME OCC is zero-padded to 4 digits
df_clean["TIME OCC"] = df_clean["TIME OCC"].astype(str).str.zfill(4)
# Extract hour from TIME OCC
df_clean["Hour Occurred"] = df_clean["TIME OCC"].str[:2].astype(int)

# Crime count per hour per crime type
hourly_data = (
    df_clean.groupby(["Hour Occurred", "Crm Cd Desc"]).size().reset_index(name="Count")
)


# Aggregate data for the dashboard
agg_data = (
    df_clean.groupby(["Victim Age Group", "Crm Cd Desc", "AREA NAME"])
    .agg(
        Count=("Crm Cd Desc", "size"), MedianDelay=("Reporting Delay (Days)", "median")
    )
    .reset_index()
)

# Hourly crime count per age group
hourly_data = (
    df_clean.groupby(["Victim Age Group", "Hour Occurred"])
    .size()
    .reset_index(name="Count")
)

# Export JSONs
agg_data.to_json("victim_profiles.json", orient="records")
hourly_data.to_json("victim_hourly.json", orient="records")

print("JSON files exported!")
