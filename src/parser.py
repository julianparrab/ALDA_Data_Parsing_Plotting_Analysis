import pandas as pd
import re
from sklearn.preprocessing import MinMaxScaler
from typing import Dict, List, Union, Optional

# Define the data types for each column
DTYPES = {
    "id": "int32",
    "plate_number": "string",
    "brand": "category",
    "model": "category",
    "year": "int16",
    "color": "category",
    "fuel_Type": "category",
    "transmission_type": "category",
    "odometer_reading": "float32",
    "insurance_provider": "category",
    "owner_name": "string",
    "owner_id": "string",
    "owner_address": "string",
    "city": "category",
    "department": "category",
    "vehicle_type": "category",
    "engine_size": "category",
    "wheel_drive": "category",
    "number_of_seats": "int8",
    "number_of_doors": "int8",
    "gps_installed": "boolean",
    "emission_standard": "category",
    "safety_rating": "category",
    "insurance_coverage_type": "category",
    "estimated_market_value": "float32",
    "vehicle_status": "category",
    "accident_history": "boolean",
}

def load_dataset(filepath):
    

    DATE_COLUMNS = ["registration_date", "insurance_expiration_date", "last_maintenance_date"]

    VALID_FUELS = {"Gasoline", "Electric", "Diesel", "Hybrid"}
    VALID_STATUS = {"IN_USE", "SELLING", "MAINTENANCE"}
    VALID_TRANSMISSION = {"Automatic", "Manual"}
    PLATE_PATTERN = re.compile(r"^[A-Z]{3}[0-9]{3}$")

    date_cols_to_parse = [col for col in DATE_COLUMNS if col in pd.read_csv(filepath, nrows=0).columns]

    # Read the CSV file
    df = pd.read_csv(filepath, index_col=0, encoding="utf-8", dtype=DTYPES, parse_dates=date_cols_to_parse )

    # Check if the DataFrame is empty
    if df.empty:
        print("The DataFrame is empty.")
        return df

    print("DataFrame loaded successfully.")

    # Initial cleaning
    df = _initial_cleaning(df)

    # Validaciones de datos
    df = _validate_data(df, PLATE_PATTERN, VALID_FUELS, VALID_STATUS, VALID_TRANSMISSION)

    # Procesamiento de columnas
    df = _process_columns(df)

    return df


def _initial_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """Performs initial cleaning of the DataFrame."""
    # Remove completely empty rows
    df.dropna(how="all", inplace=True)

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    return df


def _validate_data(
    df: pd.DataFrame, plate_pattern: re.Pattern, valid_fuels: set, valid_status: set, valid_transmission: set
) -> pd.DataFrame:
    """Validates and filters data according to specific criteria."""
    # Validate vehicle plates
    mask = df["plate_number"].str.match(plate_pattern, na=False)
    if not mask.all():
        print(f"Removing {len(df) - mask.sum()} records with invalid plates")
        df = df[mask]

    # Remove duplicate plates
    df = df.drop_duplicates(subset="plate_number")

    # Remove records without owner_id
    df = df.dropna(subset=["owner_id"])

    # Validate fuel types
    if "fuel_type" in df.columns:
        invalid_fuels = set(df["fuel_type"].unique()) - valid_fuels
        if invalid_fuels:
            print(f"Filtering {len(df[df['fuel_type'].isin(invalid_fuels)])} records with invalid fuels")
            df = df[df["fuel_type"].isin(valid_fuels)]

    # Validate vehicle status
    if "vehicle_status" in df.columns:
        df = df[df["vehicle_status"].isin(valid_status)]

    # Validate transmission types
    if "transmission_type" in df.columns:
        df = df[df["transmission_type"].isin(valid_transmission)]

    return df


def _process_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Processes and transforms specific columns."""
    # Convert engine size (e.g. "2.5L" -> 2.5)
    if "engine_size" in df.columns:
        df["engine_size"] = df["engine_size"].str.replace("L", "", regex=False).astype("float32")

    # Convert numeric columns
    numeric_cols = {
        "year": "int16",
        "odometer_reading": "float32",
        "estimated_market_value": "float32",
        "number_of_seats": "int8",
        "number_of_doors": "int8"
    }

    for col, dtype in numeric_cols.items():
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype(dtype)

    # Procesar fechas
    date_cols = ["registration_date", "insurance_expiration_date", "last_maintenance_date"]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df
