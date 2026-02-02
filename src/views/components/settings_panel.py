from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, QCheckBox, 
                             QSpinBox, QLabel, QDateTimeEdit, QPushButton, QHBoxLayout)
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
        
        # Actions
        self.apply_rules_btn = QPushButton("Preview Changes")
        self.apply_rules_btn.setObjectName("secondaryButton")
        self.process_btn = QPushButton("Apply Fixes")
        
        layout.addWidget(self.apply_rules_btn)
        layout.addWidget(self.process_btn)
        layout.addStretch()

    def get_settings(self):
        return {
            'use_exif': self.use_exif.isChecked(),
            'use_filename': self.use_filename.isChecked(),
            'use_earliest': self.use_earliest.isChecked(),
            'offset_hours': self.offset_spin.value(),
            'manual_date': self.manual_date.dateTime().toPyDateTime() if self.use_manual.isChecked() else None
        }
