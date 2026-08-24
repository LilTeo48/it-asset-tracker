import pandas as pd

from scripts.generate_alerts import generate_alerts


def test_generate_alerts() -> None:
    assets = pd.DataFrame(
        [
            {
                "asset_id": "A1",
                "device_name": "LAPTOP-001",
                "serial_number": None,
                "warranty_expiration": pd.Timestamp("2025-01-01"),
                "storage_free_gb": 20,
                "status": "Inactive",
                "last_seen": pd.Timestamp("2025-01-01"),
            },
            {
                "asset_id": "A2",
                "device_name": "LAPTOP-002",
                "serial_number": "SN123",
                "warranty_expiration": pd.Timestamp("2030-01-01"),
                "storage_free_gb": 200,
                "status": "Active",
                "last_seen": pd.Timestamp.today(),
            },
        ]
    )

    alerts = generate_alerts(assets)

    a1_alert_types = set(
        alerts[
            alerts["asset_id"] == "A1"
        ]["alert_type"]
    )

    a2_alerts = alerts[
        alerts["asset_id"] == "A2"
    ]

    assert "Missing Serial Number" in a1_alert_types
    assert "Expired Warranty" in a1_alert_types
    assert "Low Storage" in a1_alert_types
    assert "Inactive Device" in a1_alert_types
    assert "Device Not Recently Seen" in a1_alert_types

    assert a2_alerts.empty