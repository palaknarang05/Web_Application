import sys, os, json
import pandas as pd
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QFileDialog, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from fpdf import FPDF

HISTORY_FILE = "history.json"

# Load history
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)
        for item in history:
            item["upload_time"] = datetime.fromisoformat(item["upload_time"])
else:
    history = []

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Chemical Equipment Parameter Visualizer"
        self.width = 1100
        self.height = 950
        self.csv_file = None
        self.summary = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, self.width, self.height)

        # Scroll area for full content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        self.layout = QVBoxLayout(container)
        self.layout.setAlignment(Qt.AlignTop)

        # Header
        header = QLabel("Chemical Equipment Parameter Visualizer")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet(
            """
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #007bff, stop:1 #6610f2);
            color: white;
            padding: 18px;
            border-radius: 10px;
            font-size: 28px;
            font-weight: bold;
            """
        )
        self.layout.addWidget(header)

        # File selection & buttons
        file_layout = QHBoxLayout()
        self.select_label = QLabel("No file selected")
        self.select_label.setFont(QFont("Arial", 12))
        file_layout.addWidget(self.select_label)
        btn_select = QPushButton("Choose CSV")
        btn_select.setStyleSheet(self.button_style("#007bff"))
        btn_select.clicked.connect(self.select_csv)
        file_layout.addWidget(btn_select)
        btn_upload = QPushButton("Upload CSV")
        btn_upload.setStyleSheet(self.button_style("#007bff"))
        btn_upload.clicked.connect(self.process_csv)
        file_layout.addWidget(btn_upload)
        btn_pdf = QPushButton("Download PDF")
        btn_pdf.setStyleSheet(self.button_style("#28a745"))
        btn_pdf.clicked.connect(self.export_pdf)
        file_layout.addWidget(btn_pdf)
        self.layout.addLayout(file_layout)

        # Message label
        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.message_label)

        # Summary Table
        self.summary_title = QLabel("Summary Statistics")
        self.summary_title.setAlignment(Qt.AlignCenter)
        self.summary_title.setFont(QFont("Arial", 20, QFont.Bold))
        self.layout.addWidget(self.summary_title)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Charts
        self.chart_title = QLabel("Equipment Type Distribution")
        self.chart_title.setAlignment(Qt.AlignCenter)
        self.chart_title.setFont(QFont("Arial", 20, QFont.Bold))
        self.layout.addWidget(self.chart_title)

        self.figure = Figure(figsize=(10, 9))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        # History section
        self.history_title = QLabel("Last 5 Uploads")
        self.history_title.setFont(QFont("Arial", 18, QFont.Bold))
        self.layout.addWidget(self.history_title)

        btn_refresh = QPushButton("Refresh History")
        btn_refresh.setStyleSheet(self.button_style("#6c757d"))
        btn_refresh.clicked.connect(self.update_history_table)
        self.layout.addWidget(btn_refresh)

        self.history_table = QTableWidget()
        self.layout.addWidget(self.history_table)

        scroll.setWidget(container)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)

    def button_style(self, color):
        return f"""
        QPushButton {{
            background-color: {color};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 15px;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: #555555;
        }}
        """

    def select_csv(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        if filename:
            self.csv_file = filename
            self.select_label.setText(os.path.basename(filename))

    def process_csv(self):
        if not self.csv_file:
            self.show_message("Please select a CSV file first!", "red")
            return
        df = pd.read_csv(self.csv_file)
        if df.empty:
            self.show_message("CSV is empty!", "red")
            return

        # Summary stats
        self.summary = {
            "total_equipment": len(df),
            "average_flowrate": df["Flowrate"].mean(),
            "average_pressure": df["Pressure"].mean(),
            "average_temperature": df["Temperature"].mean(),
            "type_distribution": df["Type"].value_counts().to_dict()
        }

        # Update summary table
        self.table.setRowCount(4)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Parameter","Value"])
        self.table.verticalHeader().setVisible(False)
        summary_data = [
            ("Total Equipment", self.summary["total_equipment"]),
            ("Avg Flowrate", f"{self.summary['average_flowrate']:.2f}"),
            ("Avg Pressure", f"{self.summary['average_pressure']:.2f}"),
            ("Avg Temperature", f"{self.summary['average_temperature']:.2f}")
        ]
        for i,(k,v) in enumerate(summary_data):
            self.table.setItem(i,0,QTableWidgetItem(str(k)))
            self.table.setItem(i,1,QTableWidgetItem(str(v)))
        self.table.horizontalHeader().setStretchLastSection(True)

        # Plot charts
        self.plot_charts(self.summary["type_distribution"])

        # Update history
        global history
        history.insert(0,{
            "filename": os.path.basename(self.csv_file),
            "upload_time": datetime.now(),
            **self.summary
        })
        history = history[:5]
        with open(HISTORY_FILE,"w") as f:
            json.dump([ {**h,"upload_time":h["upload_time"].isoformat()} for h in history],f, indent=4)

        self.update_history_table()
        self.show_message("File uploaded successfully!", "green")

    def show_message(self, msg, color):
        self.message_label.setText(msg)
        self.message_label.setStyleSheet(f"color: {color}; font-weight:bold;")

    def plot_charts(self,type_dist):
        self.figure.clear()
        ax1 = self.figure.add_subplot(121)
        ax2 = self.figure.add_subplot(122)

        colors = ["#007bff","#6610f2","#ff8a8a","#20c998","#ffc107","#dc3545"]

        ax1.bar(type_dist.keys(), type_dist.values(), color=colors[:len(type_dist)])
        ax1.set_title("Equipment Type Distribution (Bar)")
        ax1.set_xticklabels(type_dist.keys(), rotation=35, ha="right")

        ax2.pie(type_dist.values(), labels=type_dist.keys(), autopct="%1.1f%%", colors=colors[:len(type_dist)])
        ax2.set_title("Equipment Type Distribution (Pie)")

        self.canvas.draw()

    def update_history_table(self):
        self.history_table.setRowCount(len(history))
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels([
            "Filename","Upload Time","Total","Flowrate","Pressure","Temperature"
        ])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        for i,item in enumerate(history):
            self.history_table.setItem(i,0,QTableWidgetItem(item["filename"]))
            self.history_table.setItem(i,1,QTableWidgetItem(item["upload_time"].strftime("%d/%m/%Y %H:%M:%S")))
            self.history_table.setItem(i,2,QTableWidgetItem(str(item["total_equipment"])))
            self.history_table.setItem(i,3,QTableWidgetItem(f"{item['average_flowrate']:.2f}"))
            self.history_table.setItem(i,4,QTableWidgetItem(f"{item['average_pressure']:.2f}"))
            self.history_table.setItem(i,5,QTableWidgetItem(f"{item['average_temperature']:.2f}"))

    def export_pdf(self):
        if not self.summary:
            self.show_message("No data to export!", "red")
            return
        pdf_file, _ = QFileDialog.getSaveFileName(self,"Save PDF","equipment_report.pdf","PDF Files (*.pdf)")
        if not pdf_file:
            return
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial","B",16)
        pdf.cell(0,10,"Chemical Equipment Report",ln=True,align="C")
        pdf.ln(10)
        pdf.set_font("Arial","",12)
        for k,v in [
            ("Total Equipment", self.summary["total_equipment"]),
            ("Avg Flowrate", f"{self.summary['average_flowrate']:.2f}"),
            ("Avg Pressure", f"{self.summary['average_pressure']:.2f}"),
            ("Avg Temperature", f"{self.summary['average_temperature']:.2f}")
        ]:
            pdf.cell(0,8,f"{k}: {v}",ln=True)

        # Save chart
        plot_file = "temp_plot.png"
        self.figure.savefig(plot_file,bbox_inches="tight")
        pdf.image(plot_file,x=10,w=pdf.w-20)
        os.remove(plot_file)

        pdf.output(pdf_file)
        self.show_message(f"PDF exported as {pdf_file}", "green")

if __name__=="__main__":
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())