from PyQt6.QtWidgets import QFileDialog, QMessageBox
from ..utils.file_utils import FileUtils
from .processing_controller import ProcessingController

class MainController:
    """Main controller to handle UI events and coordinate with the processing engine."""
    
    def __init__(self, view):
        self.view = view
        self.processor = ProcessingController()
        self.files_metadata = []
        
        # Connect signals
        self.view.add_folder_btn.clicked.connect(self.add_folder)
        self.view.add_files_btn.clicked.connect(self.add_files)
        self.view.clear_btn.clicked.connect(self.clear_list)
        self.view.settings_panel.apply_rules_btn.clicked.connect(self.preview_changes)
        self.view.settings_panel.process_btn.clicked.connect(self.apply_fixes)

    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(self.view, "Select Folder")
        if folder:
            files = FileUtils.scan_folder(folder)
            self._add_files_to_list(files)

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self.view, "Select Files", "", 
            "Images/Videos (*.jpg *.jpeg *.png *.heic *.mp4 *.mov);;All Files (*)"
        )
        if files:
            self._add_files_to_list(files)

    def _add_files_to_list(self, file_paths):
        self.view.status_label.setText(f"Analyzing {len(file_paths)} files...")
        for path in file_paths:
            meta = self.processor.analyze_file(path)
            self.files_metadata.append(meta)
            self.view.file_table.add_file_row(meta)
        self.view.status_label.setText(f"Loaded {len(self.files_metadata)} files")

    def clear_list(self):
    # ── Ask to clear after processing ──
        clear_reply = QMessageBox.question(
            self.view, 'Clear List',
            "Processing complete. Do you want to clear the file list?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if clear_reply == QMessageBox.StandardButton.Yes:
            self.files_metadata = []
            self.view.file_table.clear_all()
            self.view.status_label.setText("Ready")

    def preview_changes(self):
        rules = self.view.settings_panel.get_settings()
        for i, meta in enumerate(self.files_metadata):
            self.processor.apply_rules(meta, rules)
            self.view.file_table.update_row(i, meta)
        self.view.status_label.setText("Preview updated based on rules")

    def apply_fixes(self):
        if not self.files_metadata:
            return
            
        reply = QMessageBox.question(
            self.view, 'Confirm Changes',
            f"Are you sure you want to apply changes to {len(self.files_metadata)} files?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.view.progress_bar.setVisible(True)
            self.view.progress_bar.setMaximum(len(self.files_metadata))
            
            rules = self.view.settings_panel.get_settings()
            processed_count = 0
            for i, meta in enumerate(self.files_metadata):
                if self.processor.process_file(meta, rules):
                    processed_count += 1
                self.view.file_table.update_row(i, meta)
                self.view.progress_bar.setValue(i + 1)
                
            self.view.status_label.setText(f"Processed {processed_count} files successfully")
            self.view.progress_bar.setVisible(False)

            QMessageBox.information(self.view, "Complete", f"Successfully processed {processed_count} files.")
