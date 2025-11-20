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
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Run migrations and start server
```bash
python manage.py migrate
python manage.py runserver
```
   - The backend will run on http://127.0.0.1:8000/
### Web Frontend
	1.	Navigate to `frontend/`
  2.	Install dependencies:
     ```bash
    	npm install
    	```
  3.	Start development server:
     ```bash
    	npm start
    	```
     -	The web app will run on http://localhost:3000/
### Desktop App
  1.	Navigate to desktop/
  2.	Create a virtual environment and activate it
  3.	Install dependencies:
  ```bash
     pip install -r requirements.txt
   ```
	4.	Run the desktop app:
  ```bash
  python app.py
```
### Sample Data
	•	A sample CSV file is provided: sample_equipment_data.csv
	•	Use it to test the web and desktop apps.
### Notes
	•	Both Web and Desktop apps consume the same Django API backend
	•	Desktop app mirrors the Web UI for consistency
	•	PDF report includes summary stats and charts
