from PyQt6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QPushButton
)
from PyQt6.QtCore import Qt


class FileListTable(QTableWidget):
    """Table widget to display files and their metadata status."""

    def __init__(self):
        super().__init__()

        self.setColumnCount(7)
        self.setHorizontalHeaderLabels([
            "Filename",
            "Current media Date",
            "Detected Date",
            "Proposed Date",
            "Proposed Name",
            "Status",
            "Action"
        ])

        # Stretch main columns
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        # Make Action column small
        self.horizontalHeader().setSectionResizeMode(
            6, QHeaderView.ResizeMode.ResizeToContents
        )

        self.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        self.setAlternatingRowColors(True)


    @staticmethod
    def _safe_datetime(value):
        if hasattr(value, "tzinfo") and value.tzinfo is not None:
            return value.replace(tzinfo=None)
        return value


    # ---------------------------------
    # Add row with red delete button
    # ---------------------------------
    def add_file_row(self, file_meta):
        row = self.rowCount()
        self.insertRow(row)

        filename_item = QTableWidgetItem(file_meta.filename)
        if hasattr(file_meta, "path"):
            filename_item.setData(Qt.ItemDataRole.UserRole, file_meta.path)
        self.setItem(row, 0, filename_item)

        orig_date = file_meta.file_system_modified # or file_meta.exif_date_taken
        orig_date = self._safe_datetime(orig_date) if orig_date else "None"
        self.setItem(row, 1, QTableWidgetItem(str(orig_date)))

        # Detected Date priority:
# EXIF Date Taken > Filename Date > None
        detected_date = (
            file_meta.exif_date_taken
            or file_meta.filename_date
        )

        if detected_date:
            detected_date = self._safe_datetime(detected_date)
        else:
            detected_date = "None"

        self.setItem(row, 2, QTableWidgetItem(str(detected_date)))


        prop_date = file_meta.proposed_date
        prop_date = self._safe_datetime(prop_date) if prop_date else "Pending"
        self.setItem(row, 3, QTableWidgetItem(str(prop_date)))

        prop_name = file_meta.proposed_filename if file_meta.proposed_filename else ""
        self.setItem(row, 4, QTableWidgetItem(prop_name))

        self.setItem(row, 5, QTableWidgetItem(file_meta.status))

        # ---- Red Delete Button ----
        delete_btn = QPushButton("Delete")
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.setFixedHeight(24)

        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #d9534f;
                color: white;
                border: none;
                padding: 2px 8px;
                border-radius: 4px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #c9302c;
            }
            QPushButton:pressed {
                background-color: #ac2925;
            }
        """)

        delete_btn.clicked.connect(self._delete_button_clicked)
        self.setCellWidget(row, 6, delete_btn)

    # ---------------------------------
    # Update row
    # ---------------------------------
    def update_row(self, row, file_meta):
        if 0 <= row < self.rowCount():

            # If file was successfully processed, reflect the new date in Original Date
            if file_meta.status == "Processed" and file_meta.proposed_date:
                new_orig = self._safe_datetime(file_meta.proposed_date)
                self.setItem(row, 1, QTableWidgetItem(str(new_orig)))

            # Normalize proposed date
            prop_date = file_meta.proposed_date
            prop_date = (
                self._safe_datetime(prop_date)
                if prop_date else "Pending"
            )

            self.setItem(row, 3, QTableWidgetItem(str(prop_date)))
            
            prop_name = file_meta.proposed_filename if file_meta.proposed_filename else ""
            self.setItem(row, 4, QTableWidgetItem(prop_name))
            
            self.setItem(row, 5, QTableWidgetItem(file_meta.status))
    # ---------------------------------
    # Handle delete button click
    # ---------------------------------
    def _delete_button_clicked(self):
        button = self.sender()
        if not button:
            return

        index = self.indexAt(button.pos())
        if index.isValid():
            self.removeRow(index.row())

    # ---------------------------------
    # Remove selected row (keyboard)
    # ---------------------------------
    def remove_selected_row(self):
        selected = self.selectionModel().selectedRows()
        for index in sorted(selected, key=lambda x: x.row(), reverse=True):
            self.removeRow(index.row())

    # ---------------------------------
    # Get all file paths
    # ---------------------------------
    def get_all_files(self) -> list[str]:
        files = []
        for row in range(self.rowCount()):
            item = self.item(row, 0)
            if item:
                path = item.data(Qt.ItemDataRole.UserRole)
                if path:
                    files.append(path)
        return files

    # ---------------------------------
    # Clear all
    # ---------------------------------
    def clear_all(self):
        self.setRowCount(0)

    # ---------------------------------
    # Delete key support
    # ---------------------------------
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            self.remove_selected_row()
        else:
            super().keyPressEvent(event)
