# Chemical Equipment Parameter Visualizer  
### Hybrid Web + Desktop Application

## Project Overview
The **Chemical Equipment Parameter Visualizer** is a hybrid application that works as:

- A **Web Application** (React.js + Chart.js)
- A **Desktop Application** (PyQt5 + Matplotlib)

Both applications communicate with the **same Django REST API backend**.

Users can upload CSV files containing chemical equipment data:
- Equipment Name  
- Type  
- Flowrate  
- Pressure  
- Temperature  

The backend processes the file, computes analytics, and returns:
- Total equipment count  
- Average flowrate  
- Average pressure  
- Average temperature  
- Equipment type distribution  

Both web and desktop apps display:
- Summary tables  
- Bar and pie charts  
- History of last 5 uploads  
- PDF report generation  

This ensures consistent visualization across platforms.

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend (Web) | React.js, Chart.js | UI + charts |
| Frontend (Desktop) | PyQt5, Matplotlib | Desktop UI + charts |
| Backend | Django, Django REST Framework | REST API |
| Data Processing | Pandas | CSV parsing + analytics |
| Database | SQLite | Store last 5 uploads |
| Version Control | Git + GitHub | Source management |

---

## Features

### **CSV Upload**
- Upload through Web or Desktop.
- Validates and parses CSV.

### **Data Analysis**
- Total equipment count
- Average flowrate
- Average pressure
- Average temperature
- Equipment type distribution (Pump, Valve, Heater, Cooler, etc.)

### **Charts**
- Bar chart for type distribution
- Pie chart for percentage distribution

### **History Management**
- Stores the last 5 uploads in SQLite
- Shows all analytics in a table

### **PDF Report Generation**
- Summary statistics
- Charts included
- Clean layout

### **Hybrid Consistency**
Web and Desktop mirror the same UI layout and functionality.

---

## Folder Structure

```
web_application_screening_task/
│
├── backend/               # Django backend API
│   ├── manage.py
│   ├── equipment_app/
│   └── db.sqlite3
│
├── frontend/              # React.js web frontend
│   ├── src/
│   └── package.json
│
├── desktop/               # PyQt5 desktop application
│   └── app.py
│
├── sample_equipment_data.csv
├── README.md
└── .gitignore
```

---

# Setup Instructions

## Backend Setup (Django REST API)

### Navigate to backend directory
```bash
cd backend
```

### Create virtual environment
```bash
python -m venv venv
```

### Activate environment
```bash
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run migrations and start the server
```bash
python manage.py migrate
python manage.py runserver
```

Backend runs at:
```
http://127.0.0.1:8000/
```

---

## Web Frontend Setup (React.js)

### Navigate to frontend folder
```bash
cd ../frontend
```

### Install dependencies
```bash
npm install
```

### Start Web App
```bash
npm start
```

Runs at:
```
http://localhost:3000/
```

---

## Desktop App Setup (PyQt5)

### Navigate to desktop folder
```bash
cd ../desktop
```

### Create virtual environment
```bash
python -m venv venv
```

### Activate environment
```bash
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run the desktop app
```bash
python app.py
```

---

# API Endpoints (Backend)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/equipment/` | Upload CSV + process data |
| GET | `/api/history/` | Get last 5 uploads |

---

# Sample Data

A test CSV file is included:
```
sample_equipment_data.csv
```

Use it to test:
- Upload functionality  
- Summary statistics  
- Charts  
- PDF generation  
- History tracking  

---

# Demo Steps (For Video Submission)

1. **Start Django backend** (`runserver`)
2. **Start web frontend** (`npm start`)
3. **Open browser → Upload sample CSV**
4. Show:
   - Summary table  
   - Bar + Pie charts  
   - History table  
   - PDF export  
5. **Run Desktop app**
6. Upload the same CSV again
7. Show:
   - Summary  
   - Charts  
   - History  
   - PDF export  
8. Explain hybrid nature (both share the same backend)

---

# Notes

- Backend must always be running for both apps to work.
- Desktop UI layout is intentionally designed to match the Web UI.
- History is synced based on database entries.
- PDF is stored locally and includes charts + summary.

