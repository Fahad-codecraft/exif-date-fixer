from datetime import datetime, timezone
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata


def get_video_creation_time(file_path: str):
    """
    Extract video creation time using Hachoir.
    Converts UTC → LOCAL system time.
    Returns naive local datetime or None.
    """
    try:
        parser = createParser(file_path)
        if not parser:
            return None

        with parser:
            metadata = extractMetadata(parser)
            if not metadata:
                return None

            creation_date = metadata.get("creation_date")
            if not creation_date:
                return None

            if isinstance(creation_date, datetime):
                # Treat Hachoir datetime as UTC
                utc_dt = creation_date.replace(tzinfo=timezone.utc)

                # Convert to local timezone
                local_dt = utc_dt.astimezone()

                # Return naive local datetime
                return local_dt.replace(tzinfo=None)

    except Exception:
        pass

    return None
