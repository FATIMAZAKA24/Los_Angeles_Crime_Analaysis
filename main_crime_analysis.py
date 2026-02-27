# main_crime_analysis.py
import pandas as pd
import numpy as np

# from turtle import pd
from LA_Crime_Cleaned_Data import clean_la_crime_data
import crime_bubble_map


# Run the cleaning function on the CSV
df_clean = clean_la_crime_data("LA_Crime_Data.csv")
# Now df_clean is fully cleaned and ready for analysis
# print(df_clean.head())

##1.## Which area has the largest frequency of night crimes (crimes committed between 10pm and 3:59am)? Save as a string variable called peak_night_crime_location.
# approach used: group by time the crime occured (10 pm to 3:59 pm) and  then group by location and count the number of crimes in each location; then sort the values in descending order and get the top location
df_clean["Hour Occurred"] = df_clean["TIME OCC 12hr"].str.extract(r"(\d+):")
df_clean["Hour Occurred"] = df_clean["Hour Occurred"].astype(int)
night_crimes = df_clean[
    (df_clean["Hour Occurred"] >= 22) | (df_clean["Hour Occurred"] <= 3)
]
night_crimes_by_area = night_crimes.groupby("AREA NAME").size()
peak_night_crime_area = night_crimes_by_area.idxmax()
print(
    f"The area with the largest frequency of night crimes is: {peak_night_crime_area}"
)
# arange the areas with highest to lowest crime w/ correspondance to area name and visualizeit using a bar chart (top 10)
night_crimes_by_area_sorted = night_crimes_by_area.sort_values(ascending=False)
top_10_areas = night_crimes_by_area_sorted.head(10)
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
top_10_areas.plot(kind="bar", color="#921F72")
plt.title("Frequency of Night Crimes by Area (Top 10)", color="white")
plt.xlabel("Area", color="white")
plt.ylabel("Number of Night Crimes", color="black")
plt.xticks(rotation=45, ha="right", color="black")
plt.tight_layout()
plt.show()

# ##2.##Where are night crimes geographically concentrated?
import webbrowser

webbrowser.open("night_crime_bubble_map.html")


##3.##For those top 10 areas, which crime type is most frequent? That’s a grouped frequency problem.
# Ensure both columns are datetime
df_clean["Date Rptd"] = pd.to_datetime(df_clean["Date Rptd"], errors="coerce")
df_clean["DATE OCC"] = pd.to_datetime(df_clean["DATE OCC"], errors="coerce")
top_10_areas = df_clean["AREA NAME"].value_counts().head(10).index
top_areas_df = df_clean[df_clean["AREA NAME"].isin(top_10_areas)]
crime_by_area = (
    top_areas_df.groupby(["AREA NAME", "Crm Cd Desc"])
    .size()
    .reset_index(name="Crime Count")
)
top_crime_per_area = (
    crime_by_area.sort_values(["AREA NAME", "Crime Count"], ascending=[True, False])
    .groupby("AREA NAME")
    .head(1)
)
top_crime_per_area = top_crime_per_area.sort_values("Crime Count", ascending=False)

print(top_crime_per_area)
import seaborn as sns

plt.figure(figsize=(12, 6))
sns.barplot(data=top_crime_per_area, x="AREA NAME", y="Crime Count", hue="Crm Cd Desc")
plt.xticks(rotation=45)
plt.show()

# #####Which hour has the highest frequency of crimes? Store as an integer variable called peak_crime_hour with AM/PM.
# Strip minutes and keep only the hour + AM/PM
df_clean["Hour 12hr"] = (
    df_clean["TIME OCC 12hr"].str.split(":").str[0]
    + " "
    + df_clean["TIME OCC 12hr"].str.split(" ").str[1]
)
# Count frequency of each hour
hourly_crime_counts = df_clean["Hour 12hr"].value_counts()
# Get the hour with the highest crime frequency
peak_crime_hour_12hr = hourly_crime_counts.idxmax()
print(f"The hour with the highest frequency of crimes is: {peak_crime_hour_12hr}")


# #####Which crime types exhibit long victim reporting delays?
# Calculate delay
df_clean["Reporting Delay (Days)"] = (
    df_clean["Date Rptd"] - df_clean["DATE OCC"]
).dt.days

# Remove negative delays (data inconsistencies)
df_clean = df_clean[df_clean["Reporting Delay (Days)"] >= 0]
# Aggregate mean and median for each crime type (only consider crimes with >=100 reports)
crime_delay_summary = (
    df_clean.groupby("Crm Cd Desc")
    .agg(
        Median_Delay=("Reporting Delay (Days)", "median"),
        Mean_Delay=("Reporting Delay (Days)", "mean"),
        Count=("Reporting Delay (Days)", "size"),
    )
    .reset_index()
)
crime_delay_summary = crime_delay_summary[crime_delay_summary["Count"] >= 100]

# Take top 10 crime types by median delay
top10 = crime_delay_summary.sort_values("Median_Delay", ascending=False).head(10)

# Plot side-by-side comparison
plt.figure(figsize=(12, 8))
sns.barplot(
    data=top10.melt(
        id_vars="Crm Cd Desc",
        value_vars=["Median_Delay", "Mean_Delay"],
        var_name="Metric",
        value_name="Days",
    ),
    y="Crm Cd Desc",
    x="Days",
    hue="Metric",
)
plt.title("Top 10 Crime Types: Median vs Mean Reporting Delay")
plt.xlabel("Reporting Delay (Days)")
plt.ylabel("Crime Type")
plt.tight_layout()
plt.show()
# crime_delay_summary = (
#     df_clean.groupby("Crm Cd Desc")
#     .agg(
#         Median_Delay=("Reporting Delay (Days)", "median"),
#         Mean_Delay=("Reporting Delay (Days)", "mean"),
#         Count=("Reporting Delay (Days)", "size")
#     )
#     .reset_index()
# )
# crime_delay_summary = crime_delay_summary[
#     crime_delay_summary["Count"] >= 100
# ]
# crime_delay_sorted = crime_delay_summary.sort_values(
#     "Median_Delay", ascending=False
# )
# top10 = crime_delay_sorted.head(10)

# plt.figure(figsize=(12, 8))

# sns.barplot(
#     data=top10,
#     y="Crm Cd Desc",
#     x="Median_Delay"
# )

# plt.title("Top 10 Crime Types with Longest Victim Reporting Delay (Median)")
# plt.xlabel("Median Reporting Delay (Days)")
# plt.ylabel("Crime Type")
# plt.tight_layout()
# plt.show()

###4. ## Profiling
# import webbrowser
# import os
# import victim_profiling

# # Get the full path of the HTML file
# file_path = os.path.abspath("victim_dashboard.html")

# # Open in the default web browser
# webbrowser.open(f"file://{file_path}")
# main.py
# main.py
from LA_Crime_Cleaned_Data import clean_la_crime_data
import pandas as pd
import threading
import http.server
import socketserver
import webbrowser
import os

# -------------------------
# Step 1: Load and preprocess data
# -------------------------
df_clean = clean_la_crime_data("LA_Crime_Data.csv")

# Clean datetime and age
df_clean["Date Rptd"] = pd.to_datetime(df_clean["Date Rptd"], errors="coerce")
df_clean["DATE OCC"] = pd.to_datetime(df_clean["DATE OCC"], errors="coerce")
df_clean = df_clean.dropna(
    subset=["Date Rptd", "DATE OCC", "Vict Age", "AREA NAME", "Crm Cd Desc"]
)
df_clean["Reporting Delay (Days)"] = (
    df_clean["Date Rptd"] - df_clean["DATE OCC"]
).dt.days
df_clean = df_clean[df_clean["Reporting Delay (Days)"] >= 0]

# Age bins
bins = [0, 12, 18, 25, 35, 50, 65, 100]
labels = ["Child", "Teen", "Young Adult", "Adult", "Middle-aged", "Senior", "Elderly"]
df_clean["Victim Age Group"] = pd.cut(
    df_clean["Vict Age"], bins=bins, labels=labels, right=False
)

# Hour column
# Ensure TIME OCC is 4 digits (e.g. 30 → 0030)
df_clean["TIME OCC"] = df_clean["TIME OCC"].astype(str).str.zfill(4)
# Extract hour (first 2 digits)
df_clean["Hour Occurred"] = df_clean["TIME OCC"].str[:2].astype(int)

# Aggregate for dashboard
agg_data = (
    df_clean.groupby(["Victim Age Group", "Crm Cd Desc", "AREA NAME"])
    .agg(
        Count=("Crm Cd Desc", "size"), MedianDelay=("Reporting Delay (Days)", "median")
    )
    .reset_index()
)
agg_data.to_json("victim_profiles.json", orient="records")

hourly_data = (
    df_clean.groupby(["Victim Age Group", "Hour Occurred"])
    .size()
    .reset_index(name="Count")
)
hourly_data.to_json("victim_hourly.json", orient="records")

print("JSON files exported!")

# -------------------------
# Step 2: Start local HTTP server
# -------------------------
PORT = 8000
DIRECTORY = os.path.abspath(".")  # folder with HTML & JSON


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)


def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()


# Start server in a separate thread
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True
server_thread.start()

# -------------------------
# Step 3: Open dashboard in browser
# -------------------------
html_file = "victim_dashboard.html"
webbrowser.open(f"http://localhost:{PORT}/{html_file}")

# -------------------------
# Step 4: Keep server running
# -------------------------
input("Press Enter to stop server and exit...\n")
