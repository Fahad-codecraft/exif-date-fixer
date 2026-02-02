# EXIF Date Fixer

## Project Description

EXIF Date Fixer is a production-ready Python desktop application designed to analyze image and video files and intelligently fix incorrect or missing date metadata (Date Taken, Date Created, Date Modified) using EXIF data, filenames, and filesystem information. This application is built with a modular, clean, and scalable architecture using PyQt6 for the user interface.

## Core Functionalities

1.  **File & Folder Handling**: Supports selecting single files or entire folders, recursive scanning, and drag & drop. It handles common image formats (JPG, JPEG, PNG, HEIC) and video formats (MP4, MOV).
2.  **EXIF & Metadata Reading**: Reads EXIF fields like `DateTimeOriginal`, `DateTimeDigitized`, and `DateTime`. It detects missing, invalid, or corrupted dates and provides a metadata preview.
3.  **Date Fixing Rules**: Users can select rules to fix dates, including using EXIF Date Taken, date found in filenames, the earliest valid date available, or filesystem timestamps as a fallback.
4.  **Filename Date Detection**: Automatically detects dates in various formats within filenames (e.g., `IMG_20230115_142233.jpg`, `2022-12-05 Vacation.jpg`).
5.  **Batch Processing**: Applies rules to multiple files with a progress bar, optional skipping of valid files, and a dry-run mode.
6.  **Safety & Recovery**: Includes features for backing up original metadata, undoing the last operation, and logging all changes.

## Technical Stack

*   **Language**: Python 3.11+
*   **UI Framework**: PyQt6
*   **Architecture**: Modular (MVC - Model-View-Controller)
*   **Metadata Handling**: Pillow (for image loading) and piexif (for EXIF read/write)
*   **Other Modules**: `os`, `pathlib`, `datetime`, `re`

## Installation Instructions

1.  **Clone the repository (or download the source code)**:
    ```bash
    git clone <repository_url>
    cd exif_date_fixer
    ```
    (Note: Replace `<repository_url>` with the actual repository URL if available, otherwise assume the user has the files locally.)

2.  **Create a virtual environment (recommended)**:
    ```bash
    python3.11 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies**: The required packages are listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

## How to Run the Application

After installation, you can run the application from the root directory:

```bash
python main.py
```

## Instructions to Build a Standalone EXE using PyInstaller

1.  **Ensure PyInstaller is installed**: It's included in `requirements.txt`, but you can install it separately if needed:
    ```bash
    pip install pyinstaller
    ```

2.  **Navigate to the project root directory** (`exif_date_fixer`).

3.  **Run PyInstaller**: To create a single executable file, use the following command:
    ```bash
    pyinstaller --onefile --windowed main.py
    ```
    *   `--onefile`: Packages everything into a single executable file.
    *   `--windowed`: Prevents a console window from appearing when the application runs (for GUI applications).

    The executable will be found in the `dist/` directory.

## Explanation of Filename Date Detection

The `src/utils/filename_parser.py` module is responsible for intelligently detecting dates within filenames. It uses a series of regular expressions (`PATTERNS`) to match common date and time formats. The patterns are ordered from most specific (including time) to less specific (date only) to prioritize more detailed date information.

When `extract_date(filename)` is called, it iterates through these patterns, attempting to find a match. If a match is found, it tries to parse the matched string into a `datetime` object. A validation step ensures the year is within a reasonable range (1970 to current year + 1) to prevent parsing irrelevant numbers as dates.

Supported formats include:
*   `YYYYMMDD_HHMMSS` (e.g., `IMG_20230115_142233`)
*   `YYYY-MM-DD HH.MM.SS`
*   `YYYYMMDD`
*   `YYYY-MM-DD`
*   `DD-MM-YYYY`

If multiple dates are found, the current implementation prioritizes the first successful match based on the order of `PATTERNS`.

## Notes on Extending the App in Future

*   **Additional Metadata Libraries**: For more robust video metadata handling, consider integrating `hachoir` or `ffmpeg` bindings.
*   **Database for History/Settings**: Implement SQLite or a JSON file to persist user settings, processing history, and custom rules.
*   **Advanced EXIF Editor**: Expand the `ExifHandler` to allow direct editing of arbitrary EXIF tags for advanced users.
*   **Timezone Correction**: Implement a feature to adjust dates based on timezone differences, potentially using `pytz`.
*   **Drag & Drop Enhancements**: Improve the drag & drop functionality to visually indicate drop zones and provide immediate feedback.
*   **Internationalization (i18n)**: Add support for multiple languages.
*   **Unit and Integration Tests**: Develop a comprehensive test suite for all modules to ensure reliability and prevent regressions.
