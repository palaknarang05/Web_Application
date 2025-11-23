import sys, os, json
import pandas as pd
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QFileDialog, QScrollArea, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
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
        self.height = 900
        self.csv_file = None
        self.summary = None
        self._build_ui()

    def _build_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, self.width, self.height)

        # Outer layout contains single scroll area (whole-page scroller)
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0,0,0,0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        container = QWidget()
        self.layout = QVBoxLayout(container)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(18,18,18,18)
        self.layout.setSpacing(12)

        # Header
        header = QLabel("Chemical Equipment Parameter Visualizer")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet(
            """
            QLabel { color: white; padding: 14px; font-size: 20px; font-weight: 600;
                      border-radius: 10px; background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #007bff, stop:1 #6610f2); }
            """
        )
        self.layout.addWidget(header)

        # File row
        file_row = QHBoxLayout()
        file_row.setSpacing(10)
        self.btn_select = QPushButton("Select CSV File")
        self.btn_select.clicked.connect(self.select_csv)
        self.btn_select.setFixedHeight(36)

        self.lbl_file = QLabel("No file selected")
        self.lbl_file.setStyleSheet("color:#5a646f;")
        self.lbl_file.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.btn_upload = QPushButton("Upload CSV")
        self.btn_upload.clicked.connect(self.process_csv)
        self.btn_upload.setFixedHeight(36)
        self.btn_upload.setStyleSheet("background-color:#007bff; color:white; border-radius:6px;")

        file_row.addWidget(self.btn_select)
        file_row.addWidget(self.lbl_file)
        file_row.addWidget(self.btn_upload)
        self.layout.addLayout(file_row)

        # Message
        self.lbl_message = QLabel("")
        self.lbl_message.setStyleSheet("color: green;")
        self.layout.addWidget(self.lbl_message)

        # Summary card
        summary_card = QFrame()
        summary_card.setStyleSheet("background: white; border-radius: 10px; padding: 12px; border: 1px solid rgba(0,0,0,0.06);")
        summary_layout = QVBoxLayout()
        summary_layout.setSpacing(8)
        summary_card.setLayout(summary_layout)
        self.layout.addWidget(summary_card)

        title = QLabel("Summary Statistics")
        title.setStyleSheet("font-size:16px; font-weight:600; color:#343a40;")
        title.setAlignment(Qt.AlignLeft)
        summary_layout.addWidget(title)

        # Summary table
        self.table_summary = QTableWidget(4,2)
        self.table_summary.setMinimumHeight(260)
        self.table_summary.setHorizontalHeaderLabels(["Metric","Value"])
        self.table_summary.verticalHeader().setVisible(False)
        self.table_summary.horizontalHeader().setStretchLastSection(True)
        self.table_summary.setFixedHeight(140)
        self.table_summary.setColumnWidth(0,300)
        summary_layout.addWidget(self.table_summary)

        # Charts area: bar on top, pie below
        charts_frame = QFrame()
        charts_frame.setStyleSheet("background: #fafafa; border-radius: 10px; padding: 14px;")
        charts_layout = QVBoxLayout()
        charts_layout.setSpacing(18)
        charts_frame.setLayout(charts_layout)
        self.layout.addWidget(charts_frame)

        # Bar chart
        self.bar_fig = Figure(figsize=(6,3), tight_layout=True)
        self.bar_canvas = FigureCanvas(self.bar_fig)
        self.bar_ax = self.bar_fig.add_subplot(111)
        self.bar_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.bar_canvas.setFixedHeight(320)
        charts_layout.addWidget(self.bar_canvas)

        # Pie chart (below bar)
        self.pie_fig = Figure(figsize=(6,3), tight_layout=True)
        self.pie_canvas = FigureCanvas(self.pie_fig)
        self.pie_ax = self.pie_fig.add_subplot(111)
        self.pie_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.pie_canvas.setFixedHeight(300)
        charts_layout.addWidget(self.pie_canvas)

        # Controls row
        controls_row = QHBoxLayout()
        self.btn_refresh = QPushButton("Refresh History")
        self.btn_refresh.clicked.connect(self.update_history_table)
        self.btn_refresh.setFixedHeight(36)
        self.btn_refresh.setStyleSheet("background-color:#6c757d; color:white; border-radius:6px;")

        self.btn_pdf = QPushButton("Download PDF Report")
        self.btn_pdf.clicked.connect(self.export_pdf)
        self.btn_pdf.setFixedHeight(36)
        self.btn_pdf.setStyleSheet("background-color:#28a745; color:white; border-radius:6px;")

        controls_row.addWidget(self.btn_refresh)
        controls_row.addStretch()
        controls_row.addWidget(self.btn_pdf)
        self.layout.addLayout(controls_row)

        # History
        history_label = QLabel("Last 5 Uploads")
        history_label.setStyleSheet("font-size:16px; font-weight:600; color:#343a40;")
        self.layout.addWidget(history_label)

        self.table_history = QTableWidget(0,6)
        self.table_history.setMinimumHeight(260)
        self.table_history.setHorizontalHeaderLabels(["Filename","Upload Time","Total","Flowrate","Pressure","Temperature"])
        self.table_history.horizontalHeader().setStretchLastSection(True)
        self.table_history.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.table_history)

        # put container inside scroll area, add scroll to outer layout
        scroll.setWidget(container)
        outer_layout.addWidget(scroll)

        # initial history load
        try:
            self.update_history_table()
        except Exception:
            pass

    def select_csv(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select CSV file", "", "CSV files (*.csv)")
        if path:
            self.lbl_file.setText(os.path.basename(path))
            self.csv_file = path

    def process_csv(self):
        if not hasattr(self, "csv_file") or not self.csv_file:
            self.lbl_message.setText("Please select a CSV file first!")
            return
        df = pd.read_csv(self.csv_file)
        if df.empty:
            self.lbl_message.setText("CSV is empty!")
            return

        self.summary = {
            "total_equipment": len(df),
            "average_flowrate": df["Flowrate"].mean(),
            "average_pressure": df["Pressure"].mean(),
            "average_temperature": df["Temperature"].mean(),
            "type_distribution": df["Type"].value_counts().to_dict()
        }

        # populate summary table
        rows = [
            ("Total Equipment", str(self.summary["total_equipment"])),
            ("Avg Flowrate", f"{self.summary['average_flowrate']:.2f}"),
            ("Avg Pressure", f"{self.summary['average_pressure']:.2f}"),
            ("Avg Temperature", f"{self.summary['average_temperature']:.2f}")
        ]
        self.table_summary.setRowCount(len(rows))
        for r,(k,v) in enumerate(rows):
            item_k = QTableWidgetItem(k)
            item_k.setFlags(Qt.ItemIsEnabled)
            item_v = QTableWidgetItem(v)
            item_v.setFlags(Qt.ItemIsEnabled)
            item_v.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table_summary.setItem(r,0,item_k)
            self.table_summary.setItem(r,1,item_v)

        # update charts
        self.update_charts()

        # update history file
        global history
        history.insert(0, {"filename": os.path.basename(self.csv_file), "upload_time": datetime.now(), **self.summary})
        history = history[:5]
        with open(HISTORY_FILE, "w") as f:
            json.dump([{**h, "upload_time": h["upload_time"].isoformat()} for h in history], f, indent=2)

        self.update_history_table()
        self.lbl_message.setText("File uploaded successfully!")

    def update_charts(self):
        if not self.summary:
            self.bar_ax.clear(); self.pie_ax.clear(); self.bar_canvas.draw(); self.pie_canvas.draw(); return
        dist = self.summary.get("type_distribution", {})
        items = list(dist.items())
        if not items:
            self.bar_ax.clear(); self.pie_ax.clear(); self.bar_canvas.draw(); self.pie_canvas.draw(); return
        labels, counts = zip(*items)
        colors = ["#007bff","#6610f2","#ff8a8a","#20c998","#ffc107","#dc3545"]

        # Bar
        self.bar_ax.clear()
        self.bar_ax.bar(labels, counts, color=colors[:len(labels)], edgecolor='white', width=0.45)
        self.bar_ax.margins(x=0.15)
        self.bar_ax.set_title("Equipment Type Distribution (Bar)")
        self.bar_ax.tick_params(axis='x', rotation=25)
        self.bar_fig.tight_layout()
        self.bar_canvas.draw()

        # Pie
        self.pie_ax.clear()
        wedges, texts, autotexts = self.pie_ax.pie(counts, labels=labels, autopct="%1.1f%%", colors=colors[:len(labels)])
        self.pie_ax.axis('equal')
        self.pie_ax.set_title("Equipment Type Distribution (Pie)")
        self.pie_fig.tight_layout()
        self.pie_canvas.draw()

    def update_history_table(self):
        h = history or []
        self.table_history.setRowCount(len(h))
        for r,item in enumerate(h):
            self.table_history.setItem(r,0,QTableWidgetItem(item.get('filename','')))
            ut = item.get('upload_time')
            ut_str = ut.strftime('%d/%m/%Y %H:%M:%S') if hasattr(ut, 'strftime') else str(ut)
            self.table_history.setItem(r,1,QTableWidgetItem(ut_str))
            self.table_history.setItem(r,2,QTableWidgetItem(str(item.get('total_equipment',''))))
            self.table_history.setItem(r,3,QTableWidgetItem(f"{item.get('average_flowrate',0):.2f}"))
            self.table_history.setItem(r,4,QTableWidgetItem(f"{item.get('average_pressure',0):.2f}"))
            self.table_history.setItem(r,5,QTableWidgetItem(f"{item.get('average_temperature',0):.2f}"))
        self.table_history.resizeColumnsToContents()
        self.table_history.horizontalHeader().setStretchLastSection(True)

    def export_pdf(self):
        if not self.summary:
            self.lbl_message.setText('No data to export!')
            return
        pdf_file, _ = QFileDialog.getSaveFileName(self, 'Save PDF', 'equipment_report.pdf', 'PDF Files (*.pdf)')
        if not pdf_file:
            return
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial','B',16)
        pdf.cell(0,10,'Chemical Equipment Report',ln=True,align='C')
        pdf.ln(8)
        pdf.set_font('Arial','',12)
        for k,v in [('Total Equipment', self.summary['total_equipment']), ('Avg Flowrate', f"{self.summary['average_flowrate']:.2f}"), ('Avg Pressure', f"{self.summary['average_pressure']:.2f}"), ('Avg Temperature', f"{self.summary['average_temperature']:.2f}")]:
            pdf.cell(0,8,f"{k}: {v}",ln=True)
        # Save charts to temp files and add
        bar_tmp = 'bar_tmp.png'
        pie_tmp = 'pie_tmp.png'
        self.bar_fig.savefig(bar_tmp, bbox_inches='tight')
        self.pie_fig.savefig(pie_tmp, bbox_inches='tight')
        pdf.image(bar_tmp, x=10, w=pdf.w-20)
        pdf.ln(4)
        pdf.image(pie_tmp, x=10, w=pdf.w-20)
        try:
            os.remove(bar_tmp); os.remove(pie_tmp)
        except Exception:
            pass
        pdf.output(pdf_file)
        self.lbl_message.setText(f'PDF exported: {pdf_file}')

if __name__=='__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
