import pandas as pd
from pandas import DataFrame
from typing import Optional, Dict, Any, BinaryIO

# Maximum allowed upload size for CSV files.
MAX_UPLOAD_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB

# Global in‑memory dataset
DATASET: Optional[DataFrame] = None


def format_bytes(size: int) -> str:
    """Convert a byte count into a human-readable string."""
    if size < 1024:
        return f"{size} bytes"
    for unit in ["KB", "MB", "GB"]:
        size /= 1024.0
        if size < 1024.0:
            return f"{size:.1f} {unit}"
    return f"{size:.1f} TB"


def get_file_size(file: BinaryIO) -> int:
    """Return the current size of a file-like object in bytes."""
    current_position = file.tell()
    file.seek(0, 2)
    size = file.tell()
    file.seek(current_position)
    return size


def validate_file_size(file: BinaryIO, max_size: int = MAX_UPLOAD_SIZE_BYTES) -> None:
    """Raise a ValueError if the uploaded file exceeds the allowed size."""
    size = get_file_size(file)
    if size > max_size:
        raise ValueError(
            f"File size {format_bytes(size)} exceeds maximum allowed size of {format_bytes(max_size)}."
        )

# Function to load a CSV file and return the DataFrame.
def load_csv(file) -> Dict[str, Any]:
    """
    Load a CSV file into memory and return basic metadata.
    Stores the DataFrame globally in DATASET.
    """
    global DATASET

    df = pd.read_csv(file)

    # Save dataset in memory
    DATASET = df

    return {
        "rows": len(df),
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
    }

# Function in order to load a CSV file into the global DATA variable. It reads the CSV file using pandas and stores it in DATA. The function returns a dictionary containing the number of rows, the list of column names, and the data types of each column in the loaded dataset.
def load_csv_and_get_info(file) -> Dict[str, Any]:
    """
    Load a CSV file and return metadata WITHOUT storing it globally.
    Useful for validation before saving.
    """
    df = pd.read_csv(file)

    return {
        "rows": len(df),
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
    }

# Function in order to get statistics about the loaded dataset. If no dataset has been loaded, it returns None. Otherwise, it returns a description of the dataset in the form of a dictionary.
def get_stats() -> Optional[Dict[str, Dict[str, float]]]:
    """
    Return numerical statistics for the loaded dataset.
    If no dataset is loaded, return None.
    """
    if DATASET is None:
        return None

    # describe() returns only numeric columns → correct for KK2
    stats = DATASET.describe().to_dict()

    return stats