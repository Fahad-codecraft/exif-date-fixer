import re
from datetime import datetime
from dateutil import parser


class FilenameParser:
    """Automatically extracts date AND time from filenames."""

    @staticmethod
    def extract_date(filename: str):
        now_year = datetime.now().year + 1

        # -------------------------------------------------
        # 1️⃣ ISO-like patterns WITH optional time
        # -------------------------------------------------
        iso_patterns = [
            # YYYY-MM-DD HH-MM-SS / HH_MM_SS / HHMMSS
            r'(19\d{2}|20\d{2})[-_.](0[1-9]|1[0-2])[-_.](0[1-9]|[12]\d|3[01])'
            r'(?:[ T_.-]?(?:[01]\d|2[0-3])'
            r'[:_.-]?[0-5]\d'
            r'[:_.-]?[0-5]\d)?',

            # YYYYMMDD_HHMMSS
            r'(19\d{2}|20\d{2})(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])'
            r'(?:[_-]?(?:[01]\d|2[0-3])[0-5]\d[0-5]\d)?',
        ]

        for pattern in iso_patterns:
            match = re.search(pattern, filename)
            if match:
                try:
                    dt = parser.parse(
                        match.group(0),
                        yearfirst=True,
                        fuzzy=True
                    )
                    if 1970 <= dt.year <= now_year:
                        return dt
                except Exception:
                    pass

        # -------------------------------------------------
        # 2️⃣ DD-MM-YYYY with optional time
        # -------------------------------------------------
        dmy_patterns = [
            r'(0[1-9]|[12]\d|3[01])[-_.](0[1-9]|1[0-2])[-_.](19\d{2}|20\d{2})'
            r'(?:[ T_.-]?(?:[01]\d|2[0-3])'
            r'[:_.-]?[0-5]\d'
            r'[:_.-]?[0-5]\d)?'
        ]

        for pattern in dmy_patterns:
            match = re.search(pattern, filename)
            if match:
                try:
                    dt = parser.parse(
                        match.group(0),
                        dayfirst=True,
                        fuzzy=True
                    )
                    if 1970 <= dt.year <= now_year:
                        return dt
                except Exception:
                    pass

        return None
