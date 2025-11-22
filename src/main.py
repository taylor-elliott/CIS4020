from utils.file import get_dataframe
from utils.config import Config


def main():
    config = Config()

    print(f"Configuration from: {config.config_path}")
    print(f"Processed directory: {config.processed_data_dir}")
    print(f"Target columns: {config.target_columns}")
    print()
    df = get_dataframe(
        "processed_pima_diabetes.csv", config.processed_data_dir
    )
    print("Loaded DataFrame:")
    print(df)
    print(f"\nShape: {df.shape}")


if __name__ == "__main__":
    main()
