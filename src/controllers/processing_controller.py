from datetime import timedelta
from ..utils.exif_handler import ExifHandler
from ..utils.filename_parser import FilenameParser
from ..models.metadata_model import FileMetadata
import os
import shutil


class ProcessingController:
    """Engine for processing files and applying date fixing rules."""

    def __init__(self):
        self.exif_handler = ExifHandler()
        self.filename_parser = FilenameParser()

    def analyze_file(self, file_path: str) -> FileMetadata:
        filename = os.path.basename(file_path)
        ext = os.path.splitext(filename)[1].lower()

        meta = self.exif_handler.get_media_dates(file_path)
        fn_date = self.filename_parser.extract_date(filename)

        return FileMetadata(
            file_path=file_path,
            filename=filename,
            extension=ext,

            exif_date_taken=meta["date_taken"],
            exif_date_digitized=meta["date_digitized"],
            exif_date_modified=meta["date_modified"],

            file_system_created=meta["file_created"],
            file_system_modified=meta["file_modified"],

            filename_date=fn_date,
        )

    def apply_rules(self, file_meta: FileMetadata, rules: dict):
        proposed = None

        if rules.get("manual_date"):
            proposed = rules["manual_date"].replace(microsecond=0)

        elif rules.get("use_exif") and file_meta.exif_date_taken:
            proposed = file_meta.exif_date_taken

        elif rules.get("use_filename") and file_meta.filename_date:
            proposed = file_meta.filename_date

        elif rules.get("use_earliest"):
            dates = [
                file_meta.exif_date_taken,
                file_meta.filename_date,
                file_meta.file_system_created,
            ]
            dates = [d for d in dates if d]
            if dates:
                proposed = min(dates)

        if proposed and rules.get("offset_hours"):
            proposed += timedelta(hours=rules["offset_hours"])

        file_meta.proposed_date = proposed
        
        if rules.get("enable_rename") and proposed:
            date_str = proposed.strftime(self._get_strftime_format(rules.get("date_format", "YYYYMMDD_HHMMSS")))
            prefix = rules.get("prefix", "")
            suffix = rules.get("suffix", "")
            new_name = f"{prefix}{date_str}{suffix}{file_meta.extension}"
            file_meta.proposed_filename = new_name
        else:
            file_meta.proposed_filename = None

        return proposed

    def _get_strftime_format(self, format_str: str) -> str:
        mapping = {
            "YYYYMMDD_HHMMSS": "%Y%m%d_%H%M%S",
            "YYYY-MM-DD_HH-MM-SS": "%Y-%m-%d_%H-%M-%S",
            "YYYYMMDD": "%Y%m%d",
            "YYYY-MM-DD": "%Y-%m-%d"
        }
        return mapping.get(format_str, "%Y%m%d_%H%M%S")

    def process_file(self, file_meta: FileMetadata, rules: dict, dry_run=False) -> bool:
        if not file_meta.proposed_date:
            file_meta.status = "Skipped"
            file_meta.message = "No proposed date"
            return False

        if dry_run:
            file_meta.status = "Dry Run"
            file_meta.message = f"Would set date to {file_meta.proposed_date}"
            return True

        original_path = file_meta.file_path
        target_dir = rules.get("output_dir")
        if not target_dir:
            target_dir = os.path.dirname(original_path)
            
        target_name = file_meta.proposed_filename if file_meta.proposed_filename else file_meta.filename
        target_path = os.path.join(target_dir, target_name)

        if target_path != original_path:
            try:
                if rules.get("output_dir"):
                    shutil.copy2(original_path, target_path)
                else:
                    os.rename(original_path, target_path)
                
                file_meta.file_path = target_path
                file_meta.filename = target_name
            except Exception as e:
                file_meta.status = "Error"
                file_meta.message = f"File operation failed: {str(e)}"
                return False

        success = self.exif_handler.update_metadata(
            file_meta.file_path,
            file_meta.proposed_date,
        )

        if success:
            file_meta.status = "Processed"
            file_meta.message = f"Date set to {file_meta.proposed_date}"
            file_meta.exif_date_taken = file_meta.proposed_date
        else:
            file_meta.status = "Error"
            file_meta.message = "Failed to update metadata"

        return success
