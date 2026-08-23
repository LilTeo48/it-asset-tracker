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


def add_health_status(
    assets: pd.DataFrame,
    alerts: pd.DataFrame,
) -> pd.DataFrame:
    """Assign an overall health status to each asset."""

    assets = assets.copy()

    severity_rank = {
        "High": 3,
        "Medium": 2,
        "Low": 1,
    }

    alert_health = alerts[
        [
            "asset_id",
            "severity",
        ]
    ].copy()

    alert_health["severity_rank"] = alert_health[
        "severity"
    ].map(severity_rank)

    highest_severity = (
        alert_health
        .sort_values(
            "severity_rank",
            ascending=False,
        )
        .drop_duplicates(
            subset="asset_id",
            keep="first",
        )
        [
            [
                "asset_id",
                "severity",
            ]
        ]
    )

    assets = assets.merge(
        highest_severity,
        on="asset_id",
        how="left",
    )

    health_map = {
        "High": "Critical",
        "Medium": "Warning",
        "Low": "Warning",
    }

    assets["health_status"] = (
        assets["severity"]
        .map(health_map)
        .fillna("Healthy")
    )

    assets = assets.drop(
        columns=["severity"]
    )

    return assets


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

    assets = add_health_status(
    assets,
    alerts,
)

    # ----------------------------
    # Filters
    # ----------------------------

    st.subheader("Filters")

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    department_options = [
        "All"
    ] + sorted(
        assets["department"]
        .dropna()
        .unique()
        .tolist()
    )

    status_options = [
        "All"
    ] + sorted(
        assets["status"]
        .dropna()
        .unique()
        .tolist()
    )

    severity_options = [
        "All",
        "High",
        "Medium",
        "Low",
    ]

    with filter_col1:
        selected_department = st.selectbox(
            "Department",
            department_options,
        )

    with filter_col2:
        selected_status = st.selectbox(
            "Status",
            status_options,
        )

    with filter_col3:
        selected_severity = st.selectbox(
            "Alert Severity",
            severity_options,
        )

    filtered_assets = assets.copy()

    if selected_department != "All":
        filtered_assets = filtered_assets[
            filtered_assets["department"]
            == selected_department
        ]

    if selected_status != "All":
        filtered_assets = filtered_assets[
            filtered_assets["status"]
            == selected_status
        ]

    filtered_alerts = alerts.copy()

    if selected_severity != "All":
        filtered_alerts = filtered_alerts[
            filtered_alerts["severity"]
            == selected_severity
        ]

    st.divider()

    # ----------------------------
    # Summary Metrics
    # ----------------------------

    total_assets = len(assets)

    active_assets = len(
        assets[
            assets["status"] == "Active"
        ]
    )

    total_alerts = len(alerts)

    high_severity_alerts = len(
        alerts[
            alerts["severity"] == "High"
        ]
    )

    critical_assets = len(
        assets[
            assets["health_status"] == "Critical"
        ]
    )

    warning_assets = len(
        assets[
            assets["health_status"] == "Warning"
        ]
    )

    healthy_assets = len(
        assets[
            assets["health_status"] == "Healthy"
        ]
    )

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric(
        "Total Assets",
        total_assets,
    )

    metric2.metric(
        "Active Assets",
        active_assets,
    )

    metric3.metric(
        "Total Alerts",
        total_alerts,
    )

    metric4.metric(
        "High Severity",
        high_severity_alerts,
    )

    health1, health2, health3 = st.columns(3)

    health1.metric(
        "Critical Assets",
        critical_assets,
    )

    health2.metric(
        "Warning Assets",
        warning_assets,
    )

    health3.metric(
        "Healthy Assets",
        healthy_assets,
    )

    st.divider()

    
    # ----------------------------
    # Needs Attention
    # ----------------------------

    st.subheader("Needs Attention")

    severity_rank = {
        "High": 3,
        "Medium": 2,
        "Low": 1,
    }

    attention = alerts[
        [
            "asset_id",
            "device_name",
            "severity",
        ]
    ].copy()

    attention["severity_rank"] = attention[
        "severity"
    ].map(severity_rank)

    attention = (
        attention
        .sort_values(
            "severity_rank",
            ascending=False,
        )
        .drop_duplicates(
            subset="asset_id",
            keep="first",
        )
    )

    high_attention = attention[
        attention["severity"] == "High"
    ]

    medium_attention = attention[
        attention["severity"] == "Medium"
    ]

    attention_col1, attention_col2 = st.columns(2)

    with attention_col1:
        st.markdown("#### High Priority")

        if high_attention.empty:
            st.success("No high-priority assets.")
        else:
            st.dataframe(
                high_attention[
                    [
                        "asset_id",
                        "device_name",
                        "severity",
                    ]
                ],
                width="stretch",
                hide_index=True,
            )

    with attention_col2:
        st.markdown("#### Medium Priority")

        if medium_attention.empty:
            st.success("No medium-priority assets.")
        else:
            st.dataframe(
                medium_attention[
                    [
                        "asset_id",
                        "device_name",
                        "severity",
                    ]
                ],
                width="stretch",
                hide_index=True,
            )

    st.divider()

    # ----------------------------
    # Inventory
    # ----------------------------

    st.subheader("Asset Inventory")

    inventory_columns = [
        "asset_id",
        "device_name",
        "device_type",
        "manufacturer",
        "model",
        "assigned_user",
        "department",
        "status",
        "health_status",
        "operating_system",
        "storage_free_gb",
    ]

    st.dataframe(
        filtered_assets[inventory_columns],
        width="stretch",
        hide_index=True,
    )

    with st.expander(
        "View Full Asset Details"
    ):
        st.dataframe(
            filtered_assets,
            width="stretch",
            hide_index=True,
        )

    st.divider()

    # ----------------------------
    # Alerts
    # ----------------------------

    st.subheader("Asset Alerts")

    if filtered_alerts.empty:
        st.success(
            "No alerts match the selected filters."
        )
    else:
        st.dataframe(
            filtered_alerts[
                [
                    "asset_id",
                    "device_name",
                    "alert_type",
                    "severity",
                    "message",
                ]
            ],
            width="stretch",
            hide_index=True,
        )

    st.divider()

    # ----------------------------
    # Charts
    # ----------------------------

    st.subheader("Alert Analytics")

    chart_col1, chart_col2 = st.columns(2)

    alert_type_summary = (
        alerts[
            "alert_type"
        ]
        .value_counts()
        .reset_index()
    )

    alert_type_summary.columns = [
        "Alert Type",
        "Count",
    ]

    severity_summary = (
        alerts[
            "severity"
        ]
        .value_counts()
        .reset_index()
    )

    severity_summary.columns = [
        "Severity",
        "Count",
    ]

    with chart_col1:
        st.markdown(
            "#### Alerts by Type"
        )

        st.bar_chart(
            alert_type_summary,
            x="Alert Type",
            y="Count",
        )

    with chart_col2:
        st.markdown(
            "#### Alerts by Severity"
        )

        st.bar_chart(
            severity_summary,
            x="Severity",
            y="Count",
        )


if __name__ == "__main__":
    main()