import os
import logging
from datetime import datetime
import pandas as pd
from utils.file import get_dataframe
from utils.config import Config


def setup_logging(config: Config) -> logging.Logger:
    """
    Set up logging configuration from config.

    Args:
        config: Configuration object

    Returns:
        Configured logger instance
    """
    # Create log directory if it doesn't exist
    log_dir = config.log_dir
    os.makedirs(log_dir, exist_ok=True)

    # Create log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"processing_{timestamp}.log")

    # Set up handlers based on config
    handlers: list[logging.Handler] = []
    if config.file_output:
        handlers.append(logging.FileHandler(log_file))
    if config.console_output:
        handlers.append(logging.StreamHandler())

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, config.log_level),
        format=config.log_format,
        handlers=handlers,
        force=True,
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {log_file}")

    return logger


def standardize_columns(
    df: pd.DataFrame, config: Config, logger: logging.Logger
) -> pd.DataFrame:
    """
    Standardize dataset columns to match target schema from config.

    Args:
        df: Input DataFrame
        config: Configuration object
        logger: Logger instance

    Returns:
        DataFrame with standardized columns
    """
    # Create a copy to avoid modifying original
    df_processed = df.copy()

    # Drop columns specified in config
    columns_to_drop = config.columns_to_drop
    for col in columns_to_drop:
        if col in df_processed.columns:
            df_processed = df_processed.drop(col, axis=1)
            logger.info(f"  - Dropped '{col}' column")

    # Rename columns according to config mapping
    rename_map = config.column_rename_map
    if rename_map:
        df_processed = df_processed.rename(columns=rename_map)
        for old_name, new_name in rename_map.items():
            if old_name in df.columns:
                logger.info(f"  - Renamed '{old_name}' to '{new_name}'")

    # Get target columns from config
    target_columns = config.target_columns

    # Check if all required columns are present
    missing_columns = set(target_columns) - set(df_processed.columns)
    if missing_columns:
        error_msg = f"Missing required columns: {missing_columns}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Select and reorder columns to match target schema
    df_processed = df_processed[target_columns]

    return df_processed


def process_dataset(
    input_file: str, config: Config, logger: logging.Logger
) -> None:
    """
    Process a single dataset file and save to processed directory.

    Args:
        input_file: Name of the input CSV file
        config: Configuration object
        logger: Logger instance
    """
    logger.info(f"\nProcessing: {input_file}")

    try:
        # Load the dataset
        df = get_dataframe(input_file, config.raw_data_dir)
        logger.info(f"  Original shape: {df.shape}")
        logger.info(f"  Original columns: {list(df.columns)}")

        # Standardize columns
        df_processed = standardize_columns(df, config, logger)
        logger.info(f"  Processed shape: {df_processed.shape}")
        logger.info(f"  Processed columns: {list(df_processed.columns)}")

        # Create output directory if it doesn't exist
        os.makedirs(config.processed_data_dir, exist_ok=True)

        # Generate output filename
        output_file = f"{config.output_prefix}{input_file}"
        output_path = os.path.join(config.processed_data_dir, output_file)

        # Save processed dataset
        df_processed.to_csv(output_path, index=config.save_index)
        logger.info(f"  Saved to: {output_path}")

        # Display preview rows
        preview_text = (
            f"\nFirst {config.preview_rows} rows of processed data:"
        )
        logger.info(preview_text)
        logger.info(
            f"\n{df_processed.head(config.preview_rows).to_string()}"
        )

    except Exception as e:
        logger.error(
            f"Error processing {input_file}: {str(e)}", exc_info=True
        )
        if not config.continue_on_error:
            raise


def process_all_datasets(config: Config, logger: logging.Logger) -> None:
    """
    Process all CSV files in the input directory.

    Args:
        config: Configuration object
        logger: Logger instance
    """
    logger.info(f"Processing all datasets from: {config.raw_data_dir}")
    logger.info(f"Output directory: {config.processed_data_dir}")

    try:
        # Get all CSV files
        csv_files = [
            f for f in os.listdir(config.raw_data_dir) if f.endswith(".csv")
        ]

        if not csv_files:
            logger.warning(f"No CSV files found in {config.raw_data_dir}")
            return

        logger.info(f"Found {len(csv_files)} CSV file(s): {csv_files}")

        # Track success/failure
        successful = 0
        failed = 0

        # Process each file
        for csv_file in csv_files:
            try:
                process_dataset(csv_file, config, logger)
                successful += 1
            except Exception as e:
                error_msg = f"Failed to process {csv_file}: {str(e)}"
                logger.error(error_msg, exc_info=True)
                failed += 1
                if not config.continue_on_error:
                    raise

        logger.info("\n" + "=" * 60)
        summary = (
            f"Processing complete! Success: {successful}, Failed: {failed}"
        )
        logger.info(summary)

    except Exception as e:
        logger.error(
            f"Error during batch processing: {str(e)}", exc_info=True
        )
        if not config.continue_on_error:
            raise


def main():
    # Load configuration
    config = Config()

    # Set up logging
    logger = setup_logging(config)

    logger.info(f"Configuration loaded from: {config.config_path}")
    logger.info(f"Target columns: {config.target_columns}")

    # Process all datasets
    process_all_datasets(config, logger)

    logger.info(f"Log file saved in: {config.log_dir}")


if __name__ == "__main__":
    main()
