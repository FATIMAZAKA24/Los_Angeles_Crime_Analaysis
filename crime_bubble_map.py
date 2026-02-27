# main_crime_analysis.py
import folium
import pandas as pd
# from turtle import pd
from LA_Crime_Cleaned_Data import clean_la_crime_data

# Run the cleaning function on the CSV
df_clean = clean_la_crime_data("LA_Crime_Data.csv")

import pandas as pd
import folium
from sklearn.preprocessing import MinMaxScaler

# Load your cleaned dataset
df = pd.read_csv("LA_Crime_Data.csv")

# Ensure no missing coordinates
df = df.dropna(subset=["LAT", "LON"])

# Filter night crimes (10PM – 3AM)
night_crimes = df_clean[
    (df_clean["Hour Occurred"] >= 22) | (df_clean["Hour Occurred"] <= 3)
]

# Group by area and calculate:
# - total night crimes
# - average coordinates (area center)
area_summary = (
    night_crimes
    .groupby("AREA NAME")
    .agg(
        Night_Crimes=("AREA NAME", "count"),
        LAT=("LAT", "mean"),
        LON=("LON", "mean")
    )
    .reset_index()
)

# Normalize crime counts for bubble sizing
scaler = MinMaxScaler()
area_summary["normalized"] = scaler.fit_transform(
    area_summary[["Night_Crimes"]]
)

# Create base map
m = folium.Map(
    location=[34.05, -118.24],
    zoom_start=10,
    tiles="OpenStreetMap"
)

# Add bubbles
for _, row in area_summary.iterrows():
    
    # Scale radius (adjust multiplier if needed)
    radius = 10 + (row["normalized"] * 30)
    
    # Color based on intensity
    if row["normalized"] < 0.33:
        color = "green"
    elif row["normalized"] < 0.67:
        color = "orange"
    else:
        color = "red"

    folium.CircleMarker(
        location=[row["LAT"], row["LON"]],
        radius=radius,
        popup=f"""
        <b>{row['AREA NAME']}</b><br>
        Night Crimes: {row['Night_Crimes']}
        """,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(m)

# Save map
m.save("night_crime_bubble_map.html")
import webbrowser
webbrowser.open('night_crime_bubble_map.html')