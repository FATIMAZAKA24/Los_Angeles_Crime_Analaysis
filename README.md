# Los_Angeles_Crime_Analaysis
Cracking the Code on LA Crime:A modular Python framework for crime data engineering, victim profiling, and interactive spatial analysis.


**🕵️‍♀️ LA Crime Pattern Analysis**
A Complete Data Cleaning Pipeline + Exploratory Crime Pattern Study

**📌 Project Overview**
This project analyzes crime patterns in Los Angeles using the public dataset from Kaggle. The objective was not only to perform exploratory analysis, but to:

•	Build a structured and reusable preprocessing pipeline
•	Make principled decisions about missing data
•	Engineer meaningful features
•	Modularize the workflow into reusable Python files
•	Extract actionable crime insights

This repository reflects a full data science workflow — from raw dataset to analysis-ready insights.

**📂 Dataset**
Source: Kaggle – Los Angeles Crime Dataset

Data includes:
•	Crime codes and descriptions
•	Victim demographics
•	Geographic information (Area, LAT, LON)
•	Weapon information
•	Date and time of occurrence
•	Case status

**🏗 Project Architecture**

Los_Angeles_Crime_Analysis/
│
├── LA_Crime_Cleaned_Data.py      # Reusable preprocessing pipeline
├── main_crime_analysis.py        # Main analysis file
├── crime_bubble_map.py           # Geospatial visualization
├── victim_profiling.py           # Victim segmentation analysis
│
├── outputs/
│   ├── night_crime_bubble_map.html
│   ├── victim_hourly.json
│   ├── victim_dashboard.html
│   ├── victim_profiles.json
│
└── README.md

**🧹 Data Cleaning & Preprocessing Strategy**
Raw datasets are rarely analysis-ready. Significant preprocessing was performed:

**🔹 Columns Dropped**
| Column         | Reason                                  |
| -------------- | --------------------------------------- |
| DR_NO          | Case ID only; no analytical value       |
| Part 1-2       | Ambiguous                               |
| Mocodes        | 14% missing + multiple values per row   |
| Crm Cd 2, 3, 4 | High missing values                     |
| Cross Street   | Sparse and not useful for this analysis |

**🔹 Missing Data Handling**
**Vict Sex (14% missing)**
Kept column for profiling purposes.

Handled via:
•	Filling with "Unknown" for exploration
•	Option to test predictive imputation

**Weapon Used (65% missing)**
**When missing values exceed 50%, traditional imputation becomes risky.*

Instead of:
•	Mode imputation (biased)
•	Predictive imputation (unstable)

Missing values were treated as a meaningful "Unknown" category.

**🔹 Date & Time Transformations**

•	Converted Date Occurred and Date Reported to proper datetime format
•	Removed meaningless time components from date-only entries
•	Extracted month from occurrence date
•	Converted 24-hour military time into standard 12-hour format


**🔹 Feature Engineering**

•	Created age group segmentation
•	Added descriptive column for Vict Descent codes
•	Extracted month for seasonal pattern analysis
•	Preserved encoded AREA column for ML compatibility


**🧠 Key Analytical Questions**

The project answers:

•	Which hour has the highest crime frequency?
•	Which area has the most night crimes?
•	Which age groups are targeted most frequently?
•	What is the relationship between crime type and location?
•	Which crimes show long reporting delays?


**📍 Geospatial Analysis**

A bubble map visualization was created using LAT and LON coordinates and exported as an interactive .html file.







