# Chemical Equipment Parameter Visualizer (Hybrid Web + Desktop App)

## Project Overview
This project is a **Hybrid Application** that runs both as a **Web Application** (React.js) and a **Desktop Application** (PyQt5). It allows users to upload CSV files containing chemical equipment data (Name, Type, Flowrate, Pressure, Temperature), analyze it, display summaries, charts, and maintain history. Users can also generate PDF reports of the data.

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend (Web) | React.js + Chart.js | Display tables, bar and pie charts |
| Frontend (Desktop) | PyQt5 + Matplotlib | Same visualization as web |
| Backend | Python Django + Django REST Framework | API for data processing |
| Data Handling | Pandas | Read CSV & compute summary statistics |
| Database | SQLite | Store last 5 uploads |
| Version Control | Git & GitHub | Source code management |

---

## Features
- CSV Upload via Web and Desktop
- Summary statistics: total equipment, average flowrate, pressure, and temperature
- Bar and Pie charts showing equipment type distribution
- History table of last 5 uploaded datasets
- PDF report generation
- Consistent UI between Web and Desktop
- Uses a shared Django API backend

---

## Setup Instructions

### Backend
1. Navigate to `backend/`
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
