from pathlib import Path
import sqlite3

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "database" / "assets.db"


def load_table(table_name: str) -> pd.DataFrame:
    """Load a table from the SQLite database."""

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        df = pd.read_sql_query(
            f"SELECT * FROM {table_name}",
            connection,
        )
    finally:
        connection.close()

    return df


def main() -> None:
    st.set_page_config(
        page_title="IT Asset Tracker",
        page_icon="💻",
        layout="wide",
    )

    st.title("IT Asset Tracker & Alert System")
    st.caption(
        "Monitor device inventory, asset health, and automated IT alerts."
    )

    assets = load_table("assets")
    alerts = load_table("alerts")

    total_assets = len(assets)

    active_assets = len(
        assets[assets["status"] == "Active"]
    )

    total_alerts = len(alerts)

    high_severity_alerts = len(
        alerts[alerts["severity"] == "High"]
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Assets", total_assets)
    col2.metric("Active Assets", active_assets)
    col3.metric("Total Alerts", total_alerts)
    col4.metric("High Severity", high_severity_alerts)

    st.divider()

    st.subheader("Asset Inventory")

    department_filter = st.selectbox(
        "Filter by Department",
        ["All"] + sorted(assets["department"].dropna().unique().tolist()),
    )

    if department_filter != "All":
        filtered_assets = assets[
            assets["department"] == department_filter
        ]
    else:
        filtered_assets = assets

    st.dataframe(
        filtered_assets,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("Asset Alerts")

    severity_filter = st.selectbox(
        "Filter by Severity",
        ["All", "High", "Medium", "Low"],
    )

    if severity_filter != "All":
        filtered_alerts = alerts[
            alerts["severity"] == severity_filter
        ]
    else:
        filtered_alerts = alerts

    st.dataframe(
        filtered_alerts,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("Alerts by Type")

    alert_summary = (
        alerts["alert_type"]
        .value_counts()
        .reset_index()
    )

    alert_summary.columns = [
        "Alert Type",
        "Count",
    ]

    st.bar_chart(
        alert_summary,
        x="Alert Type",
        y="Count",
    )


if __name__ == "__main__":
    main()