import pandas as pd

from app import add_health_status


def test_add_health_status() -> None:
    assets = pd.DataFrame(
        [
            {
                "asset_id": "A1",
                "device_name": "LAPTOP-001",
            },
            {
                "asset_id": "A2",
                "device_name": "LAPTOP-002",
            },
            {
                "asset_id": "A3",
                "device_name": "LAPTOP-003",
            },
        ]
    )

    alerts = pd.DataFrame(
        [
            {
                "asset_id": "A1",
                "severity": "High",
            },
            {
                "asset_id": "A2",
                "severity": "Medium",
            },
        ]
    )

    result = add_health_status(
        assets,
        alerts,
    )

    health_by_asset = dict(
        zip(
            result["asset_id"],
            result["health_status"],
        )
    )

    assert health_by_asset["A1"] == "Critical"
    assert health_by_asset["A2"] == "Warning"
    assert health_by_asset["A3"] == "Healthy"