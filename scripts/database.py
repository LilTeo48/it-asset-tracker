from pathlib import Path
import sqlite3

import pandas as pd

from clean_assets import load_assets, clean_assets
from generate_alerts import generate_alerts


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "assets.db"


def create_connection() -> sqlite3.Connection:
    """Create and return a connection to the SQLite database."""

    DATABASE_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    return connection


def prepare_assets_for_database(df: pd.DataFrame) -> pd.DataFrame:
    """Convert asset data into SQLite-friendly values."""

    df = df.copy()

    date_columns = [
        "purchase_date",
        "warranty_expiration",
        "last_seen",
    ]

    for column in date_columns:
        df[column] = df[column].dt.strftime("%Y-%m-%d")

    return df


def save_assets(
    connection: sqlite3.Connection,
    assets: pd.DataFrame,
) -> None:
    """Save cleaned asset inventory into SQLite."""

    assets.to_sql(
        "assets",
        connection,
        if_exists="replace",
        index=False,
    )


def save_alerts(
    connection: sqlite3.Connection,
    alerts: pd.DataFrame,
) -> None:
    """Save generated alerts into SQLite."""

    alerts.to_sql(
        "alerts",
        connection,
        if_exists="replace",
        index=False,
    )


def main() -> None:
    print("\n--- IT Asset Database Loader ---")

    assets = load_assets()
    assets = clean_assets(assets)

    alerts = generate_alerts(assets)

    database_assets = prepare_assets_for_database(assets)

    connection = create_connection()

    try:
        save_assets(connection, database_assets)
        save_alerts(connection, alerts)

        print(f"Database created: {DATABASE_PATH}")
        print(f"Assets stored: {len(database_assets)}")
        print(f"Alerts stored: {len(alerts)}")

    finally:
        connection.close()

    print("Database connection closed successfully.")


if __name__ == "__main__":
    main()