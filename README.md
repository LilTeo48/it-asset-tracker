# IT Asset Tracker & Alert System

A Python-based IT asset tracking and alert system built with SQLite, Streamlit, and Pandas to monitor device inventory, evaluate asset health, and automatically flag potential IT issues.

## Live Demo

[Launch the IT Asset Tracker & Alert System](https://it-asset-tracker-fwvccbrgwlwmytyqbereqv.streamlit.app/)

## Features

- Track IT assets such as laptops, desktops, tablets, and other devices
- Clean and validate asset inventory data with Pandas
- Store processed asset inventory and alerts in SQLite
- Automatically detect:
  - Expired warranties
  - Low storage
  - Inactive devices
  - Devices not recently seen
  - Missing serial numbers
- Assign overall asset health statuses:
  - Critical
  - Warning
  - Healthy
- Filter assets by:
  - Department
  - Status
  - Alert severity
  - Health status
- View high-priority and medium-priority devices
- Display color-coded asset health indicators
- Analyze alert trends with interactive Streamlit charts
- View detailed asset information through an expandable dashboard section
- Automatically initialize the SQLite database when required
- Validate alert generation and health scoring with automated pytest tests

## Tech Stack

- Python
- Pandas
- SQLite
- Streamlit
- Pytest
- Git / GitHub
- Streamlit Community Cloud

## Project Architecture

```text
it-asset-tracker/
├── data/
│   └── assets.csv
├── database/
│   ├── .gitkeep
│   └── assets.db          # Generated locally and ignored by Git
├── scripts/
│   ├── clean_assets.py
│   ├── generate_alerts.py
│   └── database.py
├── screenshots/
│   ├── alert-analytics.png
│   ├── asset-inventory.png
│   ├── dashboard-overview.png
│   └── filtered-dashboard.png
├── tests/
│   ├── __init__.py
│   ├── test_alerts.py
│   └── test_health_status.py
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
