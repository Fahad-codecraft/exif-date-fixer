from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
QPushButton, QFileDialog, QProgressBar, QLabel, QSplitter)
from PyQt6.QtCore import Qt
from .components.file_list import FileListTable
from .components.settings_panel import SettingsPanel
from .styles import MODERN_STYLE

class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EXIF Date Fixer")
        self.resize(1200, 800)
        self.setStyleSheet(MODERN_STYLE)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Top Toolbar
        toolbar_layout = QHBoxLayout()
        self.add_folder_btn = QPushButton("Add Folder")
        self.add_files_btn = QPushButton("Add Files")
        self.add_files_btn.setObjectName("secondaryButton")
        self.clear_btn = QPushButton("Clear List")
        self.clear_btn.setObjectName("secondaryButton")
        
        toolbar_layout.addWidget(self.add_folder_btn)
        toolbar_layout.addWidget(self.add_files_btn)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.clear_btn)
        main_layout.addLayout(toolbar_layout)
        
        # Main Content Splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left Side: File List
        self.file_table = FileListTable()
        splitter.addWidget(self.file_table)
        
        # Right Side: Settings
        self.settings_panel = SettingsPanel()
        splitter.addWidget(self.settings_panel)
        
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        main_layout.addWidget(splitter)
        
        # Bottom Status
        status_layout = QVBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        status_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Ready")
        self.statusBar().addPermanentWidget(self.status_label)
        
        main_layout.addLayout(status_layout)

    # -------------------------------------------------
    # PROGRESS / DONE
    # -------------------------------------------------
    def update_progress(self, current, total):
        percent = int((current / total) * 100)
        self.progress_bar.setValue(percent)

    def processing_done(self):
        self.progress_bar.setValue(100)
        self.status_label.setText("Done ✅")
        self.file_table.show_clear_button()
