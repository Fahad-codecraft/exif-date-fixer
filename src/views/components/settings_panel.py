from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, QCheckBox, 
                             QSpinBox, QLabel, QDateTimeEdit, QPushButton, QHBoxLayout,
                             QLineEdit, QComboBox, QFileDialog)
from PyQt6.QtCore import QDateTime

class SettingsPanel(QWidget):
    """Panel for user-selectable rules and settings."""
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Rules Group
        rules_group = QGroupBox("Fixing Rules")
        rules_layout = QVBoxLayout()
        
        self.use_exif = QCheckBox("Use EXIF Date Taken (if available)")
        self.use_exif.setChecked(True)
        
        self.use_filename = QCheckBox("Use Date from Filename")
        self.use_filename.setChecked(True)
        
        self.use_earliest = QCheckBox("Use Earliest Available Date")
        
        rules_layout.addWidget(self.use_exif)
        rules_layout.addWidget(self.use_filename)
        rules_layout.addWidget(self.use_earliest)
        rules_group.setLayout(rules_layout)
        layout.addWidget(rules_group)
        
        # Advanced Group
        adv_group = QGroupBox("Advanced Options")
        adv_layout = QVBoxLayout()
        
        offset_layout = QHBoxLayout()
        offset_layout.addWidget(QLabel("Time Offset (Hours):"))
        self.offset_spin = QSpinBox()
        self.offset_spin.setRange(-24, 24)
        offset_layout.addWidget(self.offset_spin)
        adv_layout.addLayout(offset_layout)
        
        adv_layout.addWidget(QLabel("Manual Override Date:"))
        self.manual_date = QDateTimeEdit(QDateTime.currentDateTime())
        self.manual_date.setCalendarPopup(True)
        self.use_manual = QCheckBox("Enable Manual Override")
        adv_layout.addWidget(self.manual_date)
        adv_layout.addWidget(self.use_manual)
        
        adv_group.setLayout(adv_layout)
        layout.addWidget(adv_group)
        
        # Renaming Group
        rename_group = QGroupBox("File Renaming")
        rename_layout = QVBoxLayout()
        
        self.enable_rename = QCheckBox("Enable Renaming (Date-based)")
        rename_layout.addWidget(self.enable_rename)
        
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Date Format:"))
        self.date_format_combo = QComboBox()
        self.date_format_combo.addItems([
            "YYYYMMDD_HHMMSS",
            "YYYY-MM-DD_HH-MM-SS",
            "YYYYMMDD",
            "YYYY-MM-DD"
        ])
        format_layout.addWidget(self.date_format_combo)
        rename_layout.addLayout(format_layout)
        
        prefix_layout = QHBoxLayout()
        prefix_layout.addWidget(QLabel("Prefix:"))
        self.prefix_input = QLineEdit()
        prefix_layout.addWidget(self.prefix_input)
        rename_layout.addLayout(prefix_layout)
        
        suffix_layout = QHBoxLayout()
        suffix_layout.addWidget(QLabel("Suffix:"))
        self.suffix_input = QLineEdit()
        suffix_layout.addWidget(self.suffix_input)
        rename_layout.addLayout(suffix_layout)
        
        rename_group.setLayout(rename_layout)
        layout.addWidget(rename_group)
        
        # Output Group
        output_group = QGroupBox("Output (Optional)")
        output_layout = QVBoxLayout()
        
        self.output_dir_label = QLabel("No output folder selected (modifies inplace)")
        self.output_dir_label.setWordWrap(True)
        self.select_output_btn = QPushButton("Select Output Folder")
        self.select_output_btn.clicked.connect(self._select_output_folder)
        
        self.output_dir_path = ""
        
        output_layout.addWidget(self.output_dir_label)
        output_layout.addWidget(self.select_output_btn)
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)
        
        # Actions
        self.apply_rules_btn = QPushButton("Preview Changes")
        self.apply_rules_btn.setObjectName("secondaryButton")
        self.process_btn = QPushButton("Apply Fixes")
        
        layout.addWidget(self.apply_rules_btn)
        layout.addWidget(self.process_btn)
        layout.addStretch()

    def _select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_dir_path = folder
            self.output_dir_label.setText(f"Output: {folder}")

    def get_settings(self):
        return {
            'use_exif': self.use_exif.isChecked(),
            'use_filename': self.use_filename.isChecked(),
            'use_earliest': self.use_earliest.isChecked(),
            'offset_hours': self.offset_spin.value(),
            'manual_date': self.manual_date.dateTime().toPyDateTime() if self.use_manual.isChecked() else None,
            'enable_rename': self.enable_rename.isChecked(),
            'date_format': self.date_format_combo.currentText(),
            'prefix': self.prefix_input.text().strip(),
            'suffix': self.suffix_input.text().strip(),
            'output_dir': self.output_dir_path,
        }
