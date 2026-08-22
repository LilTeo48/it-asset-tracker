from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "assets.csv"


def load_assets() -> pd.DataFrame:
    """Load asset inventory data from CSV."""

    df = pd.read_csv(DATA_FILE)

    return df


def clean_assets(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize asset inventory data."""

    # Remove accidental spaces from column names.
    df.columns = df.columns.str.strip()

    # Remove leading/trailing whitespace from text columns.
    text_columns = df.select_dtypes(include=["object", "str"]).columns

    for column in text_columns:
        df[column] = df[column].apply(
            lambda value: value.strip() if isinstance(value, str) else value
        )

    # Convert date columns into datetime values.
    date_columns = [
        "purchase_date",
        "warranty_expiration",
        "last_seen",
    ]

    for column in date_columns:
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce",
        )

    # Convert storage columns into numeric values.
    numeric_columns = [
        "storage_total_gb",
        "storage_free_gb",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    # Standardize status formatting.
    df["status"] = df["status"].str.title()

    return df


def validate_assets(df: pd.DataFrame) -> None:
    """Print basic data-quality checks."""

    print("\n--- IT Asset Data Quality Report ---")

    print(f"Total assets: {len(df)}")

    missing_serials = df["serial_number"].isna().sum()

    print(f"Missing serial numbers: {missing_serials}")

    duplicate_assets = df["asset_id"].duplicated().sum()

    print(f"Duplicate asset IDs: {duplicate_assets}")

    missing_users = df["assigned_user"].isna().sum()

    print(f"Assets without assigned users: {missing_users}")


def main() -> None:
    df = load_assets()

    df = clean_assets(df)

    validate_assets(df)

    print("\nCleaned asset preview:")
    print(df.head())


if __name__ == "__main__":
    main()