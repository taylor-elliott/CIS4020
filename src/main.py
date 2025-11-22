from utils.file import get_dataframe
from utils.config import Config
from utils.info import preview_dataset, preview_features_target
from utils.processing import get_features_target


def main():
    c = Config()
    df = get_dataframe(c.processed_pima_path, c.processed_data_dir)
    preview_dataset(
        df,
        show=c.show_preview_dataset
    )

    X, y = get_features_target(df)

    preview_features_target(X, y, show=c.show_features_target)


if __name__ == "__main__":
    main()
