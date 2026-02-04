# EXIF Date Fixer

A powerful and modern Python desktop application designed to fix and normalize EXIF dates in images and video files. It intelligently analyzes file metadata from multiple sources (EXIF tags, filenames, file system attributes) to restore the correct creation dates.

## Features

- **Batch Processing**: Process individual files or entire folders at once.
- **Smart Date Detection**: Automatically detects the most reliable date from:
    - EXIF metadata (Date Taken, Date Digitized, Date Modified)
    - Filename patterns (e.g., `IMG_20230101_120000.jpg`)
    - File system creation/modification times
- **Broad File Support**: Supports common image and video formats:
    - Images: `.jpg`, `.jpeg`, `.png`, `.heic`
    - Videos: `.mp4`, `.mov`
- **Modern GUI**: Clean and user-friendly interface built with PyQt6.
- **Preview Changes**: View proposed date changes before applying them.
- **Progress Tracking**: Real-time progress bar for batch operations.

## Built With

- **Python 3**: Core programming language.
- **PyQt6**: For the graphical user interface.
- **Pillow (PIL)**: For image processing and EXIF manipulation.
- **piexif**: For EXIF data editing.
- **hachoir**: For video metadata extraction.
- **pywin32**: For Windows file system attribute handling.
- **python-dateutil**: For flexible date parsing.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd exif_date_fixer
    ```

2.  **Create a virtual environment (optional but recommended)**:
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the application**:
    ```bash
    python -m main
    ```

2.  **Add Files**:
    - Click **Add Folder** to scan a directory recursively.
    - Click **Add Files** to select specific images or videos.

3.  **Review and Process**:
    - The application will list all loaded files and their detected dates.
    - Select rules (if available in settings) or verify the proposed dates.
    - Click **Process** to apply the fixed dates to your files.

## Project Structure

```
exif_date_fixer/
├── main.py                 # Entry point
├── requirements.txt        # Project dependencies
└── src/
    ├── controllers/        # Application logic
    ├── models/             # Data structures
    ├── views/              # GUI components
    └── utils/              # Helper functions
```