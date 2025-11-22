import pandas as pd


def preview_dataset(df: pd.DataFrame, show: bool = True) -> None:
    if df is None: return

    if show:
        print(f"\nDataset shape: {df.shape}")
        print(f"\nColumn names: {list(df.columns)}")
        print("\nData types:")
        print(df.dtypes)
        print("\nDF HEAD:\n")
        print(df.head())
        print("\nDF TAIL:\n")
        print(df.tail())

def preview_features_target(X, y, show: bool = True) -> None:
    if X is None or y is None: return

    if show:
        print("\nFeatures\n")
        print(X)
        print("\nTARGET:\n")
        print(y)


