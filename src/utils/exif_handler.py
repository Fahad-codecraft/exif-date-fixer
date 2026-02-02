import os
import platform
from datetime import datetime
from pathlib import Path
from PIL import Image
import piexif

from .video_metadata import get_video_creation_time

# Windows-only imports
if platform.system() == "Windows":
    import pywintypes  #type: ignore
    import win32file   #type: ignore
    import win32con    #type: ignore


class ExifHandler:
    """
    Handles metadata extraction & filesystem updates.
    DateTimeOriginal (Date Taken) is READ-ONLY.
    """

    PHOTO_EXTENSIONS = [".jpg", ".jpeg", ".png", ".heic"]
    VIDEO_EXTENSIONS = [".mp4", ".mov", ".avi", ".mkv"]

    # -------------------------------------------------
    # READ METADATA
    # -------------------------------------------------
    @staticmethod
    def get_media_dates(file_path: str):
        file_path = Path(file_path)

        date_taken = None
        date_digitized = None
        date_modified = None

        # ---------- PHOTO EXIF ----------
        if file_path.suffix.lower() in ExifHandler.PHOTO_EXTENSIONS:
            try:
                img = Image.open(file_path)
                exif_bytes = img.info.get("exif")

                if exif_bytes:
                    exif = piexif.load(exif_bytes)

                    if piexif.ExifIFD.DateTimeOriginal in exif["Exif"]:
                        date_taken = ExifHandler._parse_exif(
                            exif["Exif"][piexif.ExifIFD.DateTimeOriginal]
                        )

                    if piexif.ExifIFD.DateTimeDigitized in exif["Exif"]:
                        date_digitized = ExifHandler._parse_exif(
                            exif["Exif"][piexif.ExifIFD.DateTimeDigitized]
                        )

                    if piexif.ImageIFD.DateTime in exif["0th"]:
                        date_modified = ExifHandler._parse_exif(
                            exif["0th"][piexif.ImageIFD.DateTime]
                        )
            except Exception:
                pass

        # ---------- FILESYSTEM ----------
        stat = os.stat(file_path)

        file_created = (
            datetime.fromtimestamp(stat.st_ctime)
            if os.name == "nt"
            else datetime.fromtimestamp(stat.st_mtime)
        )

        # ---------- VIDEO METADATA (REAL CREATION DATE) ----------
        if file_path.suffix.lower() in ExifHandler.VIDEO_EXTENSIONS:
            video_date = get_video_creation_time(str(file_path))
            if video_date:
                date_taken = video_date

        return {
            "date_taken": date_taken,               # READ ONLY
            "date_digitized": date_digitized,
            "date_modified": date_modified,
            "file_created": file_created,
            "file_modified": datetime.fromtimestamp(stat.st_mtime),
        }

    @staticmethod
    def _parse_exif(value):
        try:
            return datetime.strptime(value.decode(), "%Y:%m:%d %H:%M:%S")
        except Exception:
            return None

    # -------------------------------------------------
    # WRITE METADATA (NO DATE TAKEN)
    # -------------------------------------------------
    @staticmethod
    def update_metadata(file_path: str, new_date: datetime) -> bool:
        """
        Updates:
        ✔ DateTimeDigitized
        ✔ DateTime (EXIF modified)
        ✔ File modified/accessed
        ✔ File created (Windows only)
        """
        if not isinstance(new_date, datetime):
            return False

        date_str = new_date.strftime("%Y:%m:%d %H:%M:%S")
        ext = Path(file_path).suffix.lower()

        try:
            # ---------- EXIF WRITE (JPEG only) ----------
            if ext in [".jpg", ".jpeg"]:
                exif = piexif.load(file_path)

                exif["Exif"][piexif.ExifIFD.DateTimeDigitized] = date_str.encode()
                exif["0th"][piexif.ImageIFD.DateTime] = date_str.encode()

                piexif.insert(piexif.dump(exif), file_path)

            # ---------- FILESYSTEM ----------
            os.utime(file_path, (new_date.timestamp(), new_date.timestamp()))

            # ---------- WINDOWS CREATED DATE ----------
            if os.name == "nt":
                ExifHandler._set_windows_creation_time(file_path, new_date)

            return True

        except Exception as e:
            print("Metadata update failed:", e)
            return False

    # -------------------------------------------------
    # WINDOWS CREATION TIME
    # -------------------------------------------------
    @staticmethod
    def _set_windows_creation_time(file_path: str, new_date: datetime):
        handle = win32file.CreateFile(
            file_path,
            win32con.GENERIC_WRITE,
            win32con.FILE_SHARE_READ
            | win32con.FILE_SHARE_WRITE
            | win32con.FILE_SHARE_DELETE,
            None,
            win32con.OPEN_EXISTING,
            win32con.FILE_ATTRIBUTE_NORMAL,
            None,
        )

        win_time = pywintypes.Time(new_date)
        win32file.SetFileTime(handle, win_time, None, None)
        handle.close()
