from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class FileMetadata:
    """Model representing the metadata state of a single file."""
    file_path: str
    filename: str
    extension: str
    
    # Original metadata
    exif_date_taken: Optional[datetime] = None
    exif_date_digitized: Optional[datetime] = None
    exif_date_modified: Optional[datetime] = None
    file_system_created: Optional[datetime] = None
    file_system_modified: Optional[datetime] = None
    filename_date: Optional[datetime] = None
    
    # Proposed/New metadata
    proposed_date: Optional[datetime] = None
    status: str = "Pending" # Pending, Processed, Error, Skipped
    message: str = ""

    @property
    def current_best_date(self) -> Optional[datetime]:
        """Returns the most reliable date currently available."""
        return self.exif_date_taken or self.filename_date or self.exif_date_digitized or self.file_system_created
