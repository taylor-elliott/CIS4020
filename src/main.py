from utils.file import get_dataframe
from utils.config import Config
from utils.info import preview_dataset

def main():
    c = Config()
    df = get_dataframe(c.processed_pima, c.processed_data_dir)
    preview_dataset(df, c.preview_full)

if __name__ == "__main__":
    main()
