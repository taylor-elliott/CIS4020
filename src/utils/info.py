import pandas as pd


def preview_dataset(df: pd.DataFrame, show_preview: bool = True) -> None:
    """
    Display preview information about a dataset.

    Args:
        df: DataFrame to preview
        show_preview: Whether to show the preview
    """
    if not show_preview:
        return

    print(f"\nDataset shape: {df.shape}")
    print(f"\nColumn names: {list(df.columns)}")
    print("\nFirst few rows:")
    print(df.head())
    print("\nData types:")
    print(df.dtypes)
    print("\nBasic statistics:")
    print(df.describe())
