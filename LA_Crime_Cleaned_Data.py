# cleaning.py
import pandas as pd


def clean_la_crime_data(file_path, verbose=False):
    """
    Reads the LA Crime CSV file and performs:
    - Drops unnecessary columns
    - Converts date/time columns
    - Handles missing values
    - Converts data types
    - Adds victim descent description
    - Adds Year and Month features
    Returns a cleaned DataFrame ready for analysis.
    """

    # -------------------------
    # Step 1: Load Data
    # -------------------------
    df = pd.read_csv(file_path)

    if verbose:
        print(f"Original shape: {df.shape}")
        print(f"Duplicates: {df.duplicated().sum()}")
        print(f"Missing values before cleaning:\n{df.isnull().sum()}\n")

    # -------------------------
    # Step 2: Drop unnecessary columns
    # -------------------------
    drop_cols = [
        "DR_NO",
        "Part 1-2",
        "Mocodes",
        "Crm Cd 1",
        "Crm Cd 2",
        "Crm Cd 3",
        "Crm Cd 4",
        "Cross Street",
    ]
    df = df.drop(columns=drop_cols, errors="ignore")

    # -------------------------
    # Step 3: Convert date/time columns
    # -------------------------
    df["Date Rptd"] = pd.to_datetime(df["Date Rptd"], errors="coerce").dt.date
    df["DATE OCC"] = pd.to_datetime(df["DATE OCC"], errors="coerce").dt.date

    # TIME OCC to 12-hour format with AM/PM
    df["TIME OCC 12hr"] = pd.to_datetime(
        df["TIME OCC"].astype(str).str.zfill(4), format="%H%M", errors="coerce"
    ).dt.strftime("%I:%M %p")

    # -------------------------
    # Step 4: Fix data types
    # -------------------------
    df["Premis Cd"] = df["Premis Cd"].astype("Int64")  # nullable integer
    df["Weapon Used Cd"] = df["Weapon Used Cd"].astype("Int64")

    # -------------------------
    # Step 5: Fill missing values
    # -------------------------
    df["Vict Descent"] = df["Vict Descent"].fillna("Not Recorded")
    df["Weapon Desc"] = df["Weapon Desc"].fillna("Not Recorded")

    # Drop rows where Premis Cd or Premis Desc are missing (very few)
    df = df.dropna(subset=["Premis Cd", "Premis Desc"])

    # -------------------------
    # Step 6: Feature engineering
    # -------------------------
    # Victim Descent Description
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
    df["Vict Descent Description"] = (
        df["Vict Descent"].map(victim_descent_map).astype(object)
    )

    # Extract Year and Month from DATE OCC
    df["DATE OCC"] = pd.to_datetime(df["DATE OCC"], errors="coerce")  # ensure datetime
    df["Month Occurred"] = df["DATE OCC"].dt.month
    df["Year Occurred"] = df["DATE OCC"].dt.year
    df["Hour Occurred"] = df["DATE OCC"].dt.hour

    # -------------------------
    # Step 7: Final info
    # -------------------------
    print(f"Shape after cleaning: {df.shape}")
    print(f"Missing values after cleaning:\n{df.isnull().sum()}\n")

    return df
