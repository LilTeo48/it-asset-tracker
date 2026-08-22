from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

from clean_assets import clean_assets, load_assets


LOW_STORAGE_THRESHOLD_GB = 50
STALE_DEVICE_DAYS = 30


def generate_alerts(df: pd.DataFrame) -> pd.DataFrame:
    """Generate alerts for IT assets that need attention."""

    today = pd.Timestamp(datetime.now().date())
    stale_cutoff = today - timedelta(days=STALE_DEVICE_DAYS)

    alerts = []

    for _, asset in df.iterrows():
        asset_id = asset["asset_id"]
        device_name = asset["device_name"]

        if pd.isna(asset["serial_number"]) or str(asset["serial_number"]).strip() == "":
            alerts.append(
                {
                    "asset_id": asset_id,
                    "device_name": device_name,
                    "alert_type": "Missing Serial Number",
                    "severity": "High",
                    "message": "Device does not have a recorded serial number.",
                }
            )

        if (
            pd.notna(asset["warranty_expiration"])
            and asset["warranty_expiration"] < today
        ):
            alerts.append(
                {
                    "asset_id": asset_id,
                    "device_name": device_name,
                    "alert_type": "Expired Warranty",
                    "severity": "Medium",
                    "message": "Device warranty has expired.",
                }
            )

        if (
            pd.notna(asset["storage_free_gb"])
            and asset["storage_free_gb"] < LOW_STORAGE_THRESHOLD_GB
        ):
            alerts.append(
                {
                    "asset_id": asset_id,
                    "device_name": device_name,
                    "alert_type": "Low Storage",
                    "severity": "High",
                    "message": (
                        f"Only {asset['storage_free_gb']} GB of storage remains."
                    ),
                }
            )

        if asset["status"] == "Inactive":
            alerts.append(
                {
                    "asset_id": asset_id,
                    "device_name": device_name,
                    "alert_type": "Inactive Device",
                    "severity": "Medium",
                    "message": "Device is currently marked as inactive.",
                }
            )

        if pd.notna(asset["last_seen"]) and asset["last_seen"] < stale_cutoff:
            alerts.append(
                {
                    "asset_id": asset_id,
                    "device_name": device_name,
                    "alert_type": "Device Not Recently Seen",
                    "severity": "High",
                    "message": (
                        f"Device has not checked in since "
                        f"{asset['last_seen'].date()}."
                    ),
                }
            )

    return pd.DataFrame(alerts)


def main() -> None:
    assets = load_assets()
    assets = clean_assets(assets)

    alerts = generate_alerts(assets)

    print("\n--- IT Asset Alert Report ---")
    print(f"Total alerts: {len(alerts)}")

    if alerts.empty:
        print("No alerts found.")
        return

    print("\nAlerts:")
    print(
        alerts[
            [
                "asset_id",
                "device_name",
                "alert_type",
                "severity",
                "message",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()