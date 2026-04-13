# Project Architecture

This project is structured as a modular analytics pipeline that supports retail demand forecasting, anomaly detection, inventory risk scoring, and KPI reporting. It is organised into the following layers:

## Data Layer
- `data/`: Raw input datasets (not included in the repository for size/licensing reasons). Expect transactional sales data, product metadata, and inventory snapshots.

## Processing & Features
- `src/`:
  - `demand_forecasting.py`: Forecasts future demand using time-series models (e.g. ARIMA, Prophet). (To be implemented or integrated from your existing work.)
  - `anomaly_detection.py`: Implements a rolling z-score method to flag unusual sales spikes or drops.
  - `inventory_risk.py`: Projects demand over a configurable lead time and computes a risk score based on available inventory.
  - `kpi_reporting.py`: Aggregates business KPIs such as total demand, anomaly rate, average inventory level, and stockout events.

## Reporting & Dashboard
- The reporting layer produces summary tables and dictionaries via `kpi_reporting.py`. These outputs can be fed into BI tools such as Power BI, Tableau, or Streamlit dashboards for interactive exploration.

## Documentation & Governance
- `README.md`: High-level overview, business context, and usage instructions.
- `docs/architecture.md`: Current document describing the system design, data flow, and module responsibilities.
- Additional docs can be added to the `docs/` folder for API references, dataset descriptions, or future enhancements.

## Future Enhancements
- Integrate a proper forecasting engine (e.g. prophet or neural time series).
- Build a Streamlit app or Jupyter dashboard for interactive KPI exploration.
- Add unit tests and continuous integration (CI) workflows.
- Extend the anomaly detection to include multivariate methods (e.g. isolation forest).
