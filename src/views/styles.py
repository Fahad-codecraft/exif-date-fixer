MODERN_STYLE = """
QMainWindow {
    background-color: #f5f5f7;
}

QWidget {
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
    color: #333;
}

QGroupBox {
    font-weight: bold;
    border: 1px solid #d1d1d6;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 12px;
    background-color: white;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}

QPushButton {
    background-color: #007aff;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #0063cc;
}

QPushButton:pressed {
    background-color: #0051a8;
}

QPushButton#secondaryButton {
    background-color: #e5e5ea;
    color: #007aff;
}

QPushButton#secondaryButton:hover {
    background-color: #d1d1d6;
}

QTableWidget {
    border: 1px solid #d1d1d6;
    border-radius: 8px;
    background-color: white;
    gridline-color: #f2f2f7;
}

QHeaderView::section {
    background-color: #f2f2f7;
    padding: 6px;
    border: none;
    font-weight: bold;
}

QProgressBar {
    border: 1px solid #d1d1d6;
    border-radius: 4px;
    text-align: center;
    background-color: #e5e5ea;
}

QProgressBar::chunk {
    background-color: #34c759;
    border-radius: 3px;
}

QLineEdit, QComboBox, QDateTimeEdit {
    border: 1px solid #d1d1d6;
    border-radius: 4px;
    padding: 4px;
    background-color: white;
}

QStatusBar {
    background-color: #f2f2f7;
    color: #8e8e93;
}

QMessageBox {
    background-color: #f5f5f7;
}

QMessageBox QLabel {
    color: #333;
    font-size: 13px;
}

QMessageBox QPushButton {
    background-color: #007aff;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 6px 20px;
    font-weight: 600;
    min-width: 80px;
}

QMessageBox QPushButton:hover {
    background-color: #0063cc;
}

QMessageBox QPushButton:pressed {
    background-color: #0051a8;
}

"""
