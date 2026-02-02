import os
from pathlib import Path

class FileUtils:
    """Utility functions for file and folder operations."""
    
    SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.heic', '.mp4', '.mov', '.mkv', '.avi'}

    @staticmethod
    def scan_folder(folder_path, recursive=False):
        """Scans a folder for supported image and video files."""
        files = []
        path = Path(folder_path)
        
        if not path.exists():
            return files
            
        pattern = '**/*' if recursive else '*'
        for p in path.glob(pattern):
            if p.is_file() and p.suffix.lower() in FileUtils.SUPPORTED_EXTENSIONS:
                files.append(str(p))
                
        return sorted(files)

    @staticmethod
    def get_safe_backup_path(file_path):
        """Generates a backup path for a file."""
        path = Path(file_path)
        return path.with_suffix(path.suffix + '.bak')
