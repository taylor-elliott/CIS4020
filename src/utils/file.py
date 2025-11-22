import os
import pandas as pd
from typing import Optional, List


def load_csv(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError(f"File is empty: {path}")
    except pd.errors.ParserError:
        raise pd.errors.ParserError(f"Parsing error in file: {path}")


def get_dataframe(filename: str, dir: str) -> pd.DataFrame:
    """
    Load a specific CSV file from the specified directory.

    Args:
        filename: Name of the CSV file (e.g., 'data.csv')
        dir: Directory path where the file is located

    Returns:
        DataFrame containing the CSV data

    Raises:
        FileNotFoundError: If directory or file doesn't exist
        NotADirectoryError: If dir path is not a directory
    """
    if not os.path.exists(dir):
        raise FileNotFoundError(f"Directory not found: {dir}")

    if not os.path.isdir(dir):
        raise NotADirectoryError(f"Path is not a directory: {dir}")

    path = os.path.join(dir, filename)
    return load_csv(path)


def get_first_dataframe(dir: str) -> Optional[pd.DataFrame]:
    """
    Load the first CSV file found in the specified directory.

    Args:
        dir: Directory path to search for CSV files

    Returns:
        DataFrame from the first CSV file found, or None if no CSV exists

    Raises:
        FileNotFoundError: If directory doesn't exist
    """
    if not os.path.exists(dir):
        raise FileNotFoundError(f"Directory not found: {dir}")

    if not os.path.isdir(dir):
        raise NotADirectoryError(f"Path is not a directory: {dir}")

    for f in os.listdir(dir):
        if f.endswith(".csv"):
            path = os.path.join(dir, f)
            df = load_csv(path)
            return df

    return None


def get_all_dataframes(dir: str) -> List[pd.DataFrame]:
    """
    Load all CSV files from the specified directory.

    Args:
        dir: Directory path to search for CSV files

    Returns:
        List of DataFrames, one for each CSV file found

    Raises:
        FileNotFoundError: If directory doesn't exist
    """
    if not os.path.exists(dir):
        raise FileNotFoundError(f"Directory not found: {dir}")

    if not os.path.isdir(dir):
        raise NotADirectoryError(f"Path is not a directory: {dir}")

    dataframes = []
    for f in os.listdir(dir):
        if f.endswith(".csv"):
            path = os.path.join(dir, f)
            try:
                df = load_csv(path)
                dataframes.append(df)
            except Exception as e:
                print(f"Warning: Failed to load {f}: {e}")

    return dataframes


def combine_dataframes(
    dir: str, ignore_index: bool = True
) -> Optional[pd.DataFrame]:
    """
    Load and combine all CSV files from the directory into a single DataFrame.

    Args:
        dir: Directory path to search for CSV files
        ignore_index: Whether to reset index in combined DataFrame

    Returns:
        Combined DataFrame or None if no CSV files found

    Raises:
        FileNotFoundError: If directory doesn't exist
    """
    dataframes = get_all_dataframes(dir)

    if not dataframes:
        return None

    return pd.concat(dataframes, ignore_index=ignore_index)
