# Pakistan Renewable Energy Pipeline

An end-to-end data pipeline tracking Pakistan's clean energy transition — from raw data ingestion to an interactive dashboard.

**Live Dashboard:** https://pakistan-energy-pipeline-wueknqrf4en86jzaakjhuz.streamlit.app/

---

## Architecture
```
Data Sources (OWID, Ember API, IRENA)
        ↓
extract.py → data/raw/
        ↓
transform.py → data/processed/master.csv
        ↓
load.py → db/pakistan_energy.db (SQLite)
        ↓
Streamlit Dashboard (deployed on Streamlit Cloud)
```

## Data Sources

| Source | Data | Format |
|--------|------|--------|
| Our World in Data | Energy generation + consumption (1965–2024) | CSV download |
| Ember API | Generation mix + electricity demand (2000–2024) | REST API |
| IRENA | Installed renewable capacity in MW (2000–2024) | Excel download |

## Features

- Installed renewable capacity trend (2000–2024)
- Renewable generation mix by source (solar, wind, hydro, bioenergy)
- Share of each source in total generation (%)
- Electricity demand vs primary energy consumption
- Interactive year range filter

## Tech Stack

- Python, pandas, SQLAlchemy
- SQLite
- Streamlit, Plotly
- GitHub, Streamlit Cloud

## How to run locally
```bash
git clone https://github.com/your-username/pakistan-energy-pipeline
cd pakistan-energy-pipeline
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
streamlit run dashboard/app.py
```

## Project Structure
```
pakistan-energy-pipeline/
├── data/
│   ├── raw/          ← downloaded source files
│   └── processed/    ← cleaned CSVs + master table
├── pipeline/
│   ├── extract.py    ← data ingestion
│   ├── transform.py  ← cleaning + merging
│   └── load.py       ← database loading
├── dashboard/
│   └── app.py        ← Streamlit dashboard
├── db/
│   └── pakistan_energy.db
├── run.py            ← pipeline runner
└── README.md
```
